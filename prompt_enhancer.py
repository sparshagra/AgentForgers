from llm_api import call_llm  # Fixed import

def run_prompt_enhancer(user_prompt: str):
    system_msg = (
        "You are an expert creative strategist. "
        "Enhance and reframe the user's idea into a clear creative brief "
        "including goal, audience, tone, and content type."
    )
    result = call_llm(
        "meta-llama/Llama-3.2-1B-Instruct", 
        user_prompt, 
        system_prompt=system_msg,
        max_tokens=450,  # Higher for creative brief (main content piece)
        temperature=0.3
    )
    return {"agent": "PromptEnhancer", "output": result.strip()}