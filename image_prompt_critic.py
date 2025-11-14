from llama_api import call_llm

def run_image_prompt_critic(image_prompt: str):
    system_msg = (
        "You are an image prompt critic and expert. Provide concise, actionable suggestions to make the prompt "
        "clearer, more imaginative, and tailored to advertising appeal. Consider composition, clarity, style cues, "
        "and visual impact for a Stable Diffusion AI model. Also make sure that the generated prompt mentions about no distortion being there in the image"
    )
    prompt = f"IMAGE PROMPT:\n{image_prompt.strip()}"
    result = call_llm(
        "meta-llama/Llama-3.2-3B-Instruct",
        prompt,
        system_prompt=system_msg
    )
    return {"agent": "ImagePromptCritic", "output": result.strip()}
