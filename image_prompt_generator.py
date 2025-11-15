from llm_api import call_llm, call_llm_2  # Fixed import

def run_image_prompt_generator(outline: str, feedback: str = None):
    system_msg = (
        "You are an expert at crafting concise, creative prompts for AI image generation. "
        "Given an ad campaign outline, generate a detailed, vivid prompt suitable for Stable Diffusion. "
        "Focus on scene, style, mood, and key visual elements relevant for the campaign."
        "Also mention to the llm detail by detail on what the image should contain and avoid any distortions"
        "Avoid any distortions in generating hands, foots and face. Avoid any human anatomy issues"
    )
    prompt = f"CAMPAIGN OUTLINE:\n{outline.strip()}"
    if feedback:
        prompt += f"\n\nFEEDBACK:\n{feedback.strip()}\n\nRevise the image prompt based on this feedback:"
    else:
        prompt += "\n\nGenerate image prompt:"
    
    result = call_llm(
        "meta-llama/Llama-3.2-3B-Instruct",
        prompt,
        system_prompt=system_msg,
        max_tokens=300,  # Moderate for image prompts (descriptive but not too long)
        temperature=0.3
    )

    return {"agent": "ImagePromptGenerator", "output": result.strip()}
