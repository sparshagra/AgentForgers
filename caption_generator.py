# from llm_api import call_llm, call_llm_2  # Fixed import

# def run_caption_generator(outline: str, feedback: str = None):
#     system_msg = "You are a social media copywriter. Create engaging captions with hashtags."
    
#     prompt = f"""Given this social media campaign outline, generate a descreption for a instagram post:
#     make sure to not make it excessively lengthy and keep the caption and description around 30 words and include these:
#         - A catchy caption
#         - A short engaging description
#         - 5 relevant hashtags
#         Make sure the output is of the above format only consisting of those 3 things.
#         Outline:
#         {outline}
#         """
    
#     if feedback:
#         prompt += f"\n\nCritic Feedback:\n{feedback}\n\nRevise the caption based on this feedback:"
    
#     result = call_llm_2(
#         "meta-llama/Llama-3.2-3B-Instruct", 
#         prompt,
#         system_prompt=system_msg,
#         max_tokens=150,  # Moderate for captions (shorter content)
#         temperature=0.4
#     )
#     return {"agent": "CaptionGenerator", "output": result.strip()}


from llm_api import call_llm, call_llm_2  # Fixed import
import json
import re

def run_caption_generator(outline: str, feedback: str = None):
    system_msg = (
        "You are a social media copywriter. "
        "You must ALWAYS respond ONLY in valid JSON with keys: "
        "'caption', 'description', 'hashtags'. "
        "Hashtags must be a list of exactly 5 items. "
        "No extra text outside JSON."
    )

    prompt = f"""
You are given an outline for a social media post.

Generate THREE things:
1. A catchy *caption* (max 12–15 words)
2. A short *description* (max 20–25 words)
3. *Exactly 5* relevant hashtags (list format)

Rules:
- Total text should NOT exceed 30–35 words combined.
- Keep it crisp, engaging, and Instagram-friendly.
- RETURN STRICTLY IN THIS JSON FORMAT (NO EXTRA TEXT):

{{
  "caption": "...",
  "description": "...",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"]
}}

Outline:
{outline}
"""

    if feedback:
        prompt += f"\nCritic Feedback: {feedback}\nRevise the output accordingly."

    # Call the LLM
    result = call_llm_2(
        "meta-llama/Llama-3.2-3B-Instruct",
        prompt,
        system_prompt=system_msg,
        max_tokens=200,
        temperature=0.4
    )

    raw_output = result.strip()

    # Fallback JSON extraction (LLMs sometimes wrap JSON in markdown)
    try:
        # Find JSON block
        json_str = re.search(r"\{[\s\S]*\}", raw_output).group(0)
        parsed = json.loads(json_str)
    except Exception:
        # As a fallback, return raw text
        parsed = {
            "caption": "",
            "description": "",
            "hashtags": [],
            "raw_output": raw_output
        }

    return {
        "agent": "CaptionGenerator",
        "output": parsed
    }
