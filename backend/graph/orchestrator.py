
import json
from langgraph.graph import StateGraph, END
from backend.graph.nodes import LANGRAPH_AGENT_HANDLERS
from backend.core.llm_api import call_llm, call_llm_3
from backend.core.agent_memory import AgentMemory

state_schema = dict

AGENT_DEPENDENCIES = {
    "WriterAgent": ["userprompt"],
    "Outliner": ["enhanced"],
    "Captioner": ["outline"],
    "Designer": ["outline"],
    "ImageGenerator": ["image_prompt"],
   
}

def get_available_agents(state):
    available = []
    for agent, deps in AGENT_DEPENDENCIES.items():
        if all(dep in state for dep in deps):
            available.append(agent)
    return available

def should_halt_compliance(state):
    reason_raw = state.get("compliance_reason", "")
    try:
        reason_json_str = reason_raw.replace("```", "")

        reason_json = json.loads(reason_json_str)
        allowed = reason_json.get("allowed", True)  
    except Exception:
        allowed = True  
    return not allowed

def decision_node(state):
    # Only halt if compliance_blocked is True AND compliance says not allowed
    if state.get("compliance_blocked") and should_halt_compliance(state):
        print("Compliance agent stopped the workflow.")
        print(f" Stage : {state.get('compliance_stage')}")
        print(f" Reason: {state.get('compliance_reason')}")
        state["next_agent"] = "STOP"
        return state

    executed_agents = state.get("executed_agents", [])
    available_agents = get_available_agents(state)
    all_agents = list(LANGRAPH_AGENT_HANDLERS.keys())

    remaining_agents = [a for a in available_agents if a not in executed_agents]

    if not remaining_agents:
        print("🧭 Decision node: No remaining valid agents. Stopping workflow.")
        state["next_agent"] = "STOP"
        return state
    if len(remaining_agents) == 1:
        chosen = remaining_agents[0]
        print(f"🧭 Decision node (auto) selected → {chosen}")
        if isinstance(chosen, list):
            executed_agents.extend(chosen)
        else:
            executed_agents.append(chosen)
        state["executed_agents"] = executed_agents
        state["next_agent"] = chosen
        return state

    prompt = (
        "You are the controller for a creative multi-agent workflow.\n"
        f"Agents already executed: {', '.join(str(x) for x in executed_agents) if executed_agents else 'None'}\n"
        f"Available agents whose dependencies are satisfied: {', '.join(remaining_agents)}\n\n"
        f"Current workflow state keys: {list(state.keys())}\n"
        "Choose ONE of the available agents to run next logically.\n"
        "Do NOT select agents that have already completed their role.\n"
        "If everything looks done, respond with STOP.\n"
        "Respond ONLY with one of the available agent names or STOP."
    )

    next_agent = call_llm_3(
        model_id="meta-llama/Llama-3.2-3B-Instruct",
        prompt=prompt,
        system_prompt="You are coordinating creative AI agents logically and sequentially.",
        max_tokens=40,
    ).strip()

    if next_agent.upper() == "STOP" or next_agent not in remaining_agents:
        if next_agent not in remaining_agents:
            print(f"⚠️ Decision node: Invalid or repeated agent '{next_agent}', stopping workflow.")
        state["next_agent"] = "STOP"
    else:
        executed_agents.append(next_agent)
        state["executed_agents"] = executed_agents
        state["next_agent"] = next_agent

    print(f"🧭 Decision node selected next agent → {state['next_agent']}")

    loop_count = state.get("loop_count", 0) + 1
    state["loop_count"] = loop_count
    if loop_count > 15:
        print("🧨 Loop safeguard triggered. Force stopping workflow.")
        state["next_agent"] = "STOP"
    return state

def route_decision(state):
    next_agent = state.get("next_agent", "STOP")
    if next_agent == "STOP":
        return END
    return next_agent

def build_graph(context=None):
    memory = AgentMemory(user_id=context["user_id"] if context and "user_id" in context else "default_user")
    g = StateGraph(dict)
    for name, fn in LANGRAPH_AGENT_HANDLERS.items():
        g.add_node(name, lambda state, fn=fn: fn(state, memory))
    g.add_node("Decision", decision_node)
    for name in LANGRAPH_AGENT_HANDLERS:
        g.add_edge(name, "Decision")
    g.add_conditional_edges(
        "Decision",
        route_decision,
        {agent: agent for agent in LANGRAPH_AGENT_HANDLERS} | {END: END},
    )
    g.set_entry_point("WriterAgent")
    g.add_edge("WriterAgent", "Decision")
    print("✅ Dynamic LangGraph built successfully (Critic loops handled internally).")
    return g.compile()

def orchestrate_workflow(user_prompt, context=None):
    graph = build_graph(context=context)
    output = graph.invoke({"userprompt": user_prompt})
    return output

# --------------------------------------------------------------------------
# NEW: Streaming helper for SSE timeline
# --------------------------------------------------------------------------

def stream_workflow(user_prompt, context=None):
    """
    Stream the workflow step-by-step using LangGraph's .stream(),
    yielding intermediate states per agent.

    This is used by the FastAPI /run_workflow_stream SSE endpoint.
    """
    graph = build_graph(context=context)

    # Initial state for the graph
    initial_state = {"userprompt": user_prompt}
    if context and isinstance(context, dict):
        if "logo_path" in context:
            initial_state["logo_path"] = context["logo_path"]

    # LangGraph .stream yields a sequence of events, each a mapping
    # like { "WriterAgent": { ...state... } } etc.
    for event in graph.stream(initial_state):
        yield event
