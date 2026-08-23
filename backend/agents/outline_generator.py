from backend.core.llm_api import call_llm, call_llm_2  # Fixed import

def run_outline_generator(enhanced_prompt: str, feedback: str = None):
    system_msg = (
        "You are a content planner AI. Generate a structured outline for a social media campaign. "
        "Include: 1) main message, 2) key post ideas, 3) tone/style, 4) image suggestions."
    )
    prompt = f"Enhanced Prompt:\n{enhanced_prompt}"
    if feedback:
        prompt += f"\n\nCritic Feedback:\n{feedback}\n\nRevise the outline based on this feedback:"
    else:
        prompt += "\n\nOutline:"
    
    result = call_llm_2(
        "meta-llama/Llama-3.2-1B-Instruct", 
        prompt, 
        system_prompt=system_msg,
        max_tokens=400,  # Higher for detailed outline (key deliverable)
        temperature=0.3
    )
    return {"agent": "OutlineGenerator", "output": result.strip()}
