# # from agent_memory import AgentMemory
# # from langchain_core.tools import tool

# # @tool
# # def enhance_prompt_tool(userprompt: str, memory: AgentMemory = None) -> str:
# #     """Enhance a marketing prompt for a campaign."""
# #     from prompt_enhancer import run_prompt_enhancer
# #     output = run_prompt_enhancer(userprompt)
# #     if memory:
# #         memory.remember({"tool": "enhance_prompt", "input": userprompt, "output": output})
# #     return output

# # @tool
# # def outline_generator_tool(enhanced: str, feedback: str = None, memory: AgentMemory = None) -> str:
# #     """Generate a creative outline for a campaign given an enhanced prompt."""
# #     from outline_generator import run_outline_generator
# #     output = run_outline_generator(enhanced, feedback)
# #     if memory:
# #         memory.remember({"tool": "outline_generator", "input": enhanced, "feedback": feedback, "output": output})
# #     return output

# # @tool
# # def critic_tool(outline: str, memory: AgentMemory = None) -> str:
# #     """Critique an outline and provide improvements."""
# #     from critic_agent import run_critic
# #     output = run_critic(outline)
# #     if memory:
# #         memory.remember({"tool": "critic", "input": outline, "output": output})
# #     return output

# # @tool
# # def caption_generator_tool(outline: str, memory: AgentMemory = None) -> str:
# #     """Generate a campaign caption from the outline."""
# #     from caption_generator import run_caption_generator
# #     output = run_caption_generator(outline)
# #     if memory:
# #         memory.remember({"tool": "caption_generator", "input": outline, "output": output})
# #     return output

# # @tool
# # def image_prompt_tool(outline: str, feedback: str = None, memory: AgentMemory = None) -> str:
# #     """Generate an image prompt for the campaign from the outline."""
# #     from image_prompt_generator import run_image_prompt_generator
# #     output = run_image_prompt_generator(outline, feedback)
# #     if memory:
# #         memory.remember({"tool": "image_prompt", "input": outline, "feedback": feedback, "output": output})
# #     return output

# # @tool
# # def image_prompt_critic_tool(image_prompt: str, memory: AgentMemory = None) -> str:
# #     """Critique a generated image prompt."""
# #     from image_prompt_critic import run_image_prompt_critic
# #     output = run_image_prompt_critic(image_prompt)
# #     if memory:
# #         memory.remember({"tool": "image_prompt_critic", "input": image_prompt, "output": output})
# #     return output

# # @tool
# # def image_generation_tool(prompt: str, memory: AgentMemory = None) -> str:
# #     """Generate an image from a prompt with Stable Diffusion or equivalent."""
# #     from image_generator import generate_image_sd
# #     output = generate_image_sd(prompt)
# #     if memory:
# #         memory.remember({"tool": "image_generation", "input": prompt, "output": output})
# #     return output

# # @tool
# # def image_critic_tool(image_desc: str, outline: str, memory: AgentMemory = None) -> str:
# #     """Critique an image for alignment with a campaign outline."""
# #     from image_critic import run_image_critic
# #     output = run_image_critic(image_desc, outline)
# #     if memory:
# #         memory.remember({"tool": "image_critic", "input": image_desc, "outline": outline, "output": output})
# #     return output

# # ALL_TOOLS = [
# #     enhance_prompt_tool,
# #     outline_generator_tool,
# #     critic_tool,
# #     caption_generator_tool,
# #     image_prompt_tool,
# #     image_prompt_critic_tool,
# #     image_generation_tool,
# #     image_critic_tool,
# # ]
# from agent_memory import AgentMemory
# from langchain_core.tools import tool

# @tool
# def enhance_prompt_tool(userprompt: str, memory: AgentMemory = None) -> str:
#     """Enhance a marketing prompt for a campaign."""
#     from prompt_enhancer import run_prompt_enhancer
#     output = run_prompt_enhancer(userprompt)
    
#     # DEBUG: Check what type output is
#     print(f"🔍 enhance_prompt_tool output type: {type(output)}")
#     print(f"🔍 enhance_prompt_tool output: {output[:200] if isinstance(output, str) else output}")
    
#     if memory:
#         memory.remember({"tool": "enhance_prompt", "input": userprompt, "output": output})
#     return output

# @tool
# def outline_generator_tool(enhanced: str, feedback: str = None, memory: AgentMemory = None) -> str:
#     """Generate a creative outline for a campaign given an enhanced prompt."""
#     from outline_generator import run_outline_generator
#     output = run_outline_generator(enhanced, feedback)
    
#     # DEBUG: Check what type output is
#     print(f"🔍 outline_generator_tool output type: {type(output)}")
#     print(f"🔍 outline_generator_tool output: {output[:200] if isinstance(output, str) else output}")
    
#     if memory:
#         memory.remember({"tool": "outline_generator", "input": enhanced, "feedback": feedback, "output": output})
#     return output

# @tool
# def critic_tool(outline: str, memory: AgentMemory = None) -> str:
#     """Critique an outline and provide improvements."""
#     from critic_agent import run_critic
#     output = run_critic(outline)
#     if memory:
#         memory.remember({"tool": "critic", "input": outline, "output": output})
#     return output

# @tool
# def caption_generator_tool(outline: str, memory: AgentMemory = None) -> str:
#     """Generate a campaign caption from the outline."""
#     from caption_generator import run_caption_generator
#     output = run_caption_generator(outline)
#     if memory:
#         memory.remember({"tool": "caption_generator", "input": outline, "output": output})
#     return output

# @tool
# def image_prompt_tool(outline: str, feedback: str = None, memory: AgentMemory = None) -> str:
#     """Generate an image prompt for the campaign from the outline."""
#     from image_prompt_generator import run_image_prompt_generator
#     output = run_image_prompt_generator(outline, feedback)
#     if memory:
#         memory.remember({"tool": "image_prompt", "input": outline, "feedback": feedback, "output": output})
#     return output

# @tool
# def image_prompt_critic_tool(image_prompt: str, memory: AgentMemory = None) -> str:
#     """Critique a generated image prompt."""
#     from image_prompt_critic import run_image_prompt_critic
#     output = run_image_prompt_critic(image_prompt)
#     if memory:
#         memory.remember({"tool": "image_prompt_critic", "input": image_prompt, "output": output})
#     return output

# @tool
# def image_generation_tool(prompt: str, memory: AgentMemory = None) -> str:
#     """Generate an image from a prompt with Stable Diffusion or equivalent."""
#     from image_generator import generate_image_sd
#     output = generate_image_sd(prompt)
#     if memory:
#         memory.remember({"tool": "image_generation", "input": prompt, "output": output})
#     return output

# @tool
# def image_critic_tool(image_desc: str, outline: str, memory: AgentMemory = None) -> str:
#     """Critique an image for alignment with a campaign outline."""
#     from image_critic import run_image_critic
#     output = run_image_critic(image_desc, outline)
#     if memory:
#         memory.remember({"tool": "image_critic", "input": image_desc, "outline": outline, "output": output})
#     return output

# ALL_TOOLS = [
#     enhance_prompt_tool,
#     outline_generator_tool,
#     critic_tool,
#     caption_generator_tool,
#     image_prompt_tool,
#     image_prompt_critic_tool,
#     image_generation_tool,
#     image_critic_tool,
# ]

from agent_memory import AgentMemory
from langchain_core.tools import tool

@tool
def enhance_prompt_tool(userprompt: str, memory: AgentMemory = None) -> str:
    """Enhance a marketing prompt for a campaign."""
    from prompt_enhancer import run_prompt_enhancer
    output = run_prompt_enhancer(userprompt)
    
    print(f"🔍 enhance_prompt_tool output type: {type(output)}")
    
    if memory:
        memory.remember({"tool": "enhance_prompt", "input": userprompt, "output": output})
    return output

@tool
def outline_generator_tool(enhanced: str, feedback: str = None, memory: AgentMemory = None) -> str:
    """Generate a creative outline for a campaign given an enhanced prompt."""
    from outline_generator import run_outline_generator
    output = run_outline_generator(enhanced, feedback)
    
    print(f"🔍 outline_generator_tool output type: {type(output)}")
    
    if memory:
        memory.remember({"tool": "outline_generator", "input": enhanced, "feedback": feedback, "output": output})
    return output

@tool
def critic_tool(outline: str, memory: AgentMemory = None) -> str:
    """Critique an outline and provide improvements."""
    from critic_agent import run_critic
    output = run_critic(outline)
    if memory:
        memory.remember({"tool": "critic", "input": outline, "output": output})
    return output

@tool
def caption_generator_tool(outline: str, memory: AgentMemory = None) -> str:
    """Generate a campaign caption from the outline."""
    from caption_generator import run_caption_generator
    output = run_caption_generator(outline)
    if memory:
        memory.remember({"tool": "caption_generator", "input": outline, "output": output})
    return output

@tool
def image_prompt_tool(outline: str, feedback: str = None, memory: AgentMemory = None) -> str:
    """Generate an image prompt for the campaign from the outline."""
    from image_prompt_generator import run_image_prompt_generator
    output = run_image_prompt_generator(outline, feedback)
    if memory:
        memory.remember({"tool": "image_prompt", "input": outline, "feedback": feedback, "output": output})
    return output

@tool
def image_prompt_critic_tool(image_prompt: str, memory: AgentMemory = None) -> str:
    """Critique a generated image prompt."""
    from image_prompt_critic import run_image_prompt_critic
    output = run_image_prompt_critic(image_prompt)
    if memory:
        memory.remember({"tool": "image_prompt_critic", "input": image_prompt, "output": output})
    return output

@tool
def image_generation_tool(image_prompt: str, memory: AgentMemory = None) -> str:
    """
    Generate an actual image from the image prompt using Stable Diffusion XL.
    Returns the filepath where the image is saved.
    """
    from image_api import generate_image_from_prompt
    
    print(f"🎨 Generating image from prompt...")
    filepath = generate_image_from_prompt(image_prompt)
    
    if memory:
        memory.remember({
            "tool": "image_generation", 
            "input": image_prompt, 
            "output": filepath
        })
    
    return filepath

@tool
def image_critic_tool(image_desc: str, outline: str, memory: AgentMemory = None) -> str:
    """Critique an image for alignment with a campaign outline."""
    from image_critic import run_image_critic
    output = run_image_critic(image_desc, outline)
    if memory:
        memory.remember({"tool": "image_critic", "input": image_desc, "outline": outline, "output": output})
    return output

# tools.py

# def instagram_post_formatter_tool(enhanced, outline, caption):
#     description = ""
#     if enhanced and outline:
#         description = f"{enhanced.strip()} | {outline.strip()[:80]}..."
#     elif enhanced:
#         description = enhanced.strip()
#     elif outline:
#         description = outline.strip()
#     hashtags = "#branding #creativity #instapost"  # Add LLM logic as needed
#     ig_post = {
#         "description": description,
#         "caption": caption or description,
#         "hashtags": hashtags,
#         "insta_post_snippet": f"{description}\n\n{caption or ''}\n{hashtags}"
#     }
#     return ig_post



ALL_TOOLS = [
    enhance_prompt_tool,
    outline_generator_tool,
    critic_tool,
    caption_generator_tool,
    image_prompt_tool,
    image_prompt_critic_tool,
    image_generation_tool,
    image_critic_tool,
]