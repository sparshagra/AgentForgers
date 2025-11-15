
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

import prompt_enhancer, outline_generator, critic_agent
import image_prompt_generator, image_prompt_critic, image_generator, image_critic, caption_generator
from rich import print

class FlowState(BaseModel):
    userprompt: str
    enhanced: str = None
    outline: str = None
    feedback: str = None
    round: int = 1
    image_prompt: str = None
    image_prompt_feedback: str = None
    improved_image_prompt: str = None
    image_path: str = None
    image_critic_feedback: str = None
    caption: str = None

sg = StateGraph(FlowState)

# --- TEXT PROCESSING ---
def enhance_node(state: FlowState):
    res = prompt_enhancer.run_prompt_enhancer(state.userprompt)
    print("[bold blue]--- Enhanced Prompt ---[/bold blue]\n", res["output"])
    return {"enhanced": res["output"]}

def outline_node(state: FlowState):
    res = outline_generator.run_outline_generator(state.enhanced, feedback=state.feedback)
    print("[bold yellow]--- Outline Draft ---[/bold yellow]\n", res["output"])
    return {"outline": res["output"]}

def critic_node(state: FlowState):
    res = critic_agent.run_critic(state.outline)
    print("[bold red]--- Critic Feedback ---[/bold red]\n", res["output"])
    round_val = state.round
    if ("improve" in res["output"].lower() or "suggest" in res["output"].lower()) and round_val < 2:
        round_val += 1
    return {"feedback": res["output"], "round": round_val}

# --- IMAGE BRANCH ---
def image_prompt_node(state: FlowState):
    res = image_prompt_generator.run_image_prompt_generator(state.outline)
    print("[bold magenta]--- Image Prompt ---[/bold magenta]\n", res["output"])
    return {"image_prompt": res["output"]}

def image_prompt_critic_node(state: FlowState):
    res = image_prompt_critic.run_image_prompt_critic(state.image_prompt)
    print("[bold green]--- Image Prompt Critique ---[/bold green]\n", res["output"])
    res2 = image_prompt_generator.run_image_prompt_generator(state.outline, feedback=res["output"])
    print("[bold cyan]--- Improved Image Prompt ---[/bold cyan]\n", res2["output"])
    return {"image_prompt_feedback": res["output"], "improved_image_prompt": res2["output"]}

def image_generation_node(state: FlowState):
    image_path = image_generator.generate_image_sd(state.improved_image_prompt)
    print(f"[bold white]Image saved at {image_path}[/bold white]")
    return {"image_path": image_path}

def image_critic_node(state: FlowState):
    res = image_critic.run_image_critic(state.improved_image_prompt, state.outline)
    print("[bold red]--- Image Critic Feedback ---[/bold red]\n", res["output"])
    return {"image_critic_feedback": res["output"]}

# --- CAPTION BRANCH ---
def caption_generation_node(state: FlowState):
    res = caption_generator.run_caption_generator(state.outline)
    print("[bold blue]--- Caption Generation ---[/bold blue]", res["output"])
    return {"caption": res["output"]}

# --- BRANCHING NODE ---
def branching_node(state: FlowState):
    # just a fork, does not update
    return {}

# node registration
sg.add_node("enhance", enhance_node)
sg.add_node("outline", outline_node)
sg.add_node("critic", critic_node)
sg.add_node("branch", branching_node)
sg.add_node("image_prompt", image_prompt_node)
sg.add_node("image_prompt_critic", image_prompt_critic_node)
sg.add_node("image_generation", image_generation_node)
sg.add_node("image_critic", image_critic_node)
sg.add_node("caption_generation", caption_generation_node)

# Edges for main linear flow
sg.set_entry_point("enhance")
sg.add_edge("enhance", "outline")
sg.add_edge("outline", "critic")

def after_critic_conditional(state):
    # If after first round, and feedback calls for more changes, go back to outline
    if ("improve" in state.feedback.lower() or "suggest" in state.feedback.lower()) and state.round < 2:
        return "outline"
    # If rounds are exhausted, branch to downstream work
    return "branch"

sg.add_conditional_edges("critic", after_critic_conditional, {
    "branch": "branch",
    "outline": "outline",
})

sg.add_edge("branch", "image_prompt")
sg.add_edge("branch", "caption_generation")

sg.add_edge("image_prompt", "image_prompt_critic")
sg.add_edge("image_prompt_critic", "image_generation")
sg.add_edge("image_generation", "image_critic")

graph = sg.compile()
