# critic_agent.py
from llm_api import call_llm

def run_critic(previous_output: str):
    """
    Provide structured, constructive feedback on the previous agent's output
    without rewriting or enhancing it.
    """
    system_msg = (
        "You are a constructive AI critic. "
        "Your task is to provide specific, actionable feedback on the text below. "
        "Do NOT rewrite or improve the text yourself - only critique it."
    )

    prompt = f"""
    Review the following output and provide concise feedback.

    Output:
    ---
    {previous_output}
    ---

    Respond only in this format:
    - Strengths:
    - Weaknesses:
    - Suggestions for improvement:
    """

    result = call_llm(
        "meta-llama/Llama-3.2-3B-Instruct",
        prompt,
        system_prompt=system_msg,
        max_tokens=120,  # Reduced for budget: enough for structured feedback
        temperature=0.4
    )

    return {"agent": "CriticAgent", "output": result.strip()}
