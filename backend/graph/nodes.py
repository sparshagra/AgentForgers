
from backend.graph.tools import (
    enhance_prompt_tool, outline_generator_tool, critic_tool, caption_generator_tool,
    image_prompt_tool, image_generation_tool
)
from backend.agents.compliance_agent import run_text_compliance, run_image_compliance
import os
import json

# --------------------------------------------------------------------------
# Utility: Extract tool output
# --------------------------------------------------------------------------
def extract_output(tool_response):
    """Extract actual text output from @tool responses."""
    if isinstance(tool_response, str):
        return tool_response
    elif isinstance(tool_response, dict):
        return tool_response.get('output',
               tool_response.get('result',
               tool_response.get('text', str(tool_response))))
    else:
        return str(tool_response)


# --------------------------------------------------------------------------
# Agent + Critique loops
# --------------------------------------------------------------------------

def writer_with_critique(state, memory):
    """WriterAgent → Critic → WriterAgent again (refined)."""
    print("\n🧠 Running WriterAgent + Critique loop...")

    user_prompt = state["userprompt"]

    # 🔒 Compliance Stage 1: raw user prompt
    prompt_check = run_text_compliance(stage="user prompt", text=user_prompt)
    if not prompt_check["allowed"]:
        reason = prompt_check["reason"]
        print(f"🛑 Compliance block at PROMPT stage: {reason}")

        memory.remember({
            "tool": "compliance",
            "stage": "prompt",
            "input": user_prompt,
            "output": reason,
        })

        # Mark state as blocked; Decision node will stop the workflow.
        blocked_state = {
            **state,
            "compliance_blocked": True,
            "compliance_stage": "prompt",
            "compliance_reason": reason,
        }
        return blocked_state

    # ✅ If allowed, continue as before
    enhanced_response = enhance_prompt_tool.invoke({
        "userprompt": user_prompt,
        "memory": memory
    })
    enhanced_text = extract_output(enhanced_response)
    print(f"✅ WriterAgent: Enhanced prompt created ({len(enhanced_text)} chars)")

    critique_response = critic_tool.invoke({
        "outline": enhanced_text,
        "memory": memory
    })
    critique_text = extract_output(critique_response)
    print(f"🧐 Critic: Feedback generated ({len(critique_text)} chars)")

    refined_response = enhance_prompt_tool.invoke({
        "userprompt": user_prompt + "\n\nCritic feedback:\n" + critique_text,
        "memory": memory
    })
    refined_text = extract_output(refined_response)
    print(f"✅ WriterAgent (Refined): Enhanced prompt re-generated ({len(refined_text)} chars)")

    print(f"🧠 Memory STM size: {len(memory.stm)} | Episodic entries: {len(memory.episodic)}")

    return {**state, "enhanced": refined_text, "writer_critique": critique_text}



def outliner_with_critique(state, memory):
    """Outliner → Critic → Outliner again (refined)."""
    print("\n📋 Running Outliner + Critique loop...")

    outline_response = outline_generator_tool.invoke({
        "enhanced": state["enhanced"],
        "memory": memory
    })
    outline_text = extract_output(outline_response)
    print(f"✅ Outliner: Outline created ({len(outline_text)} chars)")

    critique_response = critic_tool.invoke({
        "outline": outline_text,
        "memory": memory
    })
    critique_text = extract_output(critique_response)
    print(f"🧐 Critic: Feedback generated ({len(critique_text)} chars)")

    refined_response = outline_generator_tool.invoke({
        "enhanced": state["enhanced"],
        "feedback": critique_text + "\nPrevious outline:\n" + outline_text,
        "memory": memory
    })
    refined_outline = extract_output(refined_response)
    print(f"✅ Outliner (Refined): Outline improved ({len(refined_outline)} chars)")

    print(f"🧠 Memory STM size: {len(memory.stm)} | Episodic entries: {len(memory.episodic)}")

    return {**state, "outline": refined_outline, "outline_critique": critique_text}


def captioner_with_critique(state, memory):
    """Captioner → Critic → Captioner again (refined)."""
    print("\n💬 Running Captioner + Critique loop...")

    # 1️⃣ Initial caption generation (JSON-aware)
    caption_response = caption_generator_tool.invoke({
        "outline": state["outline"],
        "memory": memory
    })
    caption_data = extract_output(caption_response)  # dict or str

    # For printing
    if isinstance(caption_data, dict):
        caption_printable = json.dumps(caption_data, ensure_ascii=False)
    else:
        caption_printable = str(caption_data)

    print(f"✅ Captioner: Caption created ({len(caption_printable)} chars)")

    # 2️⃣ Build a human-readable string for the critic
    if isinstance(caption_data, dict):
        parts = []
        if caption_data.get("caption"):
            parts.append(str(caption_data["caption"]))
        if caption_data.get("description"):
            parts.append(str(caption_data["description"]))
        hashtags = caption_data.get("hashtags") or []
        if isinstance(hashtags, list):
            parts.append(" ".join(str(h) for h in hashtags))
        else:
            parts.append(str(hashtags))
        caption_for_critic = "\n".join(parts)
    else:
        caption_for_critic = caption_printable

    critique_response = critic_tool.invoke({
        "outline": caption_for_critic,
        "memory": memory
    })
    critique_text = extract_output(critique_response)
    print(f"🧐 Critic: Feedback generated ({len(critique_text)} chars)")

    # 3️⃣ Refine caption using outline + explicit feedback + previous caption
    outline_for_refine = (
        state["outline"]
        + "\n\nCritic feedback:\n"
        + critique_text
        + "\nPrevious caption:\n"
        + caption_printable
    )

    refined_response = caption_generator_tool.invoke({
        "outline": outline_for_refine,
        "memory": memory
    })
    refined_caption_data = extract_output(refined_response)

    if isinstance(refined_caption_data, dict):
        refined_printable = json.dumps(refined_caption_data, ensure_ascii=False)
    else:
        refined_printable = str(refined_caption_data)

    print(f"✅ Captioner (Refined): Caption improved ({len(refined_printable)} chars)")

    print(f"🧠 Memory STM size: {len(memory.stm)} | Episodic entries: {len(memory.episodic)}")

    # state["caption"] is now typically:
    # { "caption": "...", "description": "...", "hashtags": [...] }
    return {**state, "caption": refined_caption_data, "caption_critique": critique_text}


def designer_with_critique(state, memory):
    """Designer → Critic → Designer again (refined)."""
    print("\n🎨 Running Designer + Critique loop...")

    image_prompt_response = image_prompt_tool.invoke({
        "outline": state["outline"],
        "memory": memory
    })
    image_prompt_text = extract_output(image_prompt_response)
    print(f"✅ Designer: Image prompt created ({len(image_prompt_text)} chars)")

    critique_response = critic_tool.invoke({
        "outline": image_prompt_text,
        "memory": memory
    })
    critique_text = extract_output(critique_response)
    print(f"🧐 Critic: Feedback generated ({len(critique_text)} chars)")

    refined_response = image_prompt_tool.invoke({
        "outline": state["outline"],
        "feedback": critique_text + "\nPrevious image prompt:\n" + image_prompt_text,
        "memory": memory
    })
    refined_image_prompt = extract_output(refined_response)
    print(f"✅ Designer (Refined): Image prompt improved ({len(refined_image_prompt)} chars)")

    # 🔒 Compliance Stage 2: final image prompt before generation
    img_prompt_check = run_text_compliance(stage="image prompt", text=refined_image_prompt)
    if not img_prompt_check["allowed"]:
        reason = img_prompt_check["reason"]
        print(f"🛑 Compliance block at IMAGE PROMPT stage: {reason}")

        memory.remember({
            "tool": "compliance",
            "stage": "image_prompt",
            "input": refined_image_prompt,
            "output": reason,
        })

        blocked_state = {
            **state,
            "image_prompt": refined_image_prompt,  # keep for transparency
            "image_prompt_critique": critique_text,
            "compliance_blocked": True,
            "compliance_stage": "image_prompt",
            "compliance_reason": reason,
        }
        return blocked_state

    print(f"🧠 Memory STM size: {len(memory.stm)} | Episodic entries: {len(memory.episodic)}")

    return {**state, "image_prompt": refined_image_prompt, "image_prompt_critique": critique_text}


def image_generator_agent(state, memory):
    """Generate final image from refined image prompt + add brand logo."""
    print("\n🖼️ Running ImageGenerator...")

    from backend.media.logo_dropper import add_logo_to_image

    image_prompt = state.get("image_prompt", "")
    if not image_prompt:
        print("⚠️ No image prompt found. Skipping generation.")
        return {**state, "generated_image": "ERROR: No image prompt."}

    # --------------------------------------
    # STEP 1 — Generate Raw Image
    # --------------------------------------
    image_filepath = image_generation_tool.invoke({
        "image_prompt": image_prompt,
        "memory": memory
    })
    image_filepath = extract_output(image_filepath)

    print(f"✅ ImageGenerator: Raw image saved to {image_filepath}")

    # --------------------------------------
    # STEP 2 — Compliance Check (as before)
    # --------------------------------------
    context_chunks = []
    if "outline" in state:
        context_chunks.append(f"Outline: {state['outline']}")

    caption_obj = state.get("caption")
    if caption_obj is not None:
        if isinstance(caption_obj, dict):
            caption_str = json.dumps(caption_obj, ensure_ascii=False)
        else:
            caption_str = str(caption_obj)
        context_chunks.append(f"Caption: {caption_str}")

    context_chunks.append(f"Image prompt: {image_prompt}")
    context_text = "\n\n".join(context_chunks)

    img_check = run_image_compliance(image_path=image_filepath, context_text=context_text)
    if not img_check["allowed"]:
        reason = img_check["reason"]
        print(f"🛑 Compliance block at FINAL IMAGE stage: {reason}")

        memory.remember({
            "tool": "compliance",
            "stage": "image",
            "input": image_filepath,
            "output": reason,
        })

        blocked_state = {
            **state,
            "generated_image": f"ERROR: Image blocked due to compliance – {reason}",
            "compliance_blocked": True,
            "compliance_stage": "image",
            "compliance_reason": reason,
        }
        print(f"🧠 Memory STM size: {len(memory.stm)} | Episodic entries: {len(memory.episodic)}")
        return blocked_state

    # --------------------------------------
    # STEP 3 — Add Logo After Compliance Check
    # --------------------------------------
    final_path = os.path.join("outputs", "final_post.png")  # final branded output

    # Prefer user-specific logo_path from state; fall back to default
    logo_path = state.get("logo_path") or "assets/brand_logo.png"

    try:
        branded_image_path = add_logo_to_image(
            input_image=image_filepath,
            logo_path=logo_path,
            output_path=final_path
        )
        print(f"🎉 Logo added successfully → {branded_image_path}")
    except Exception as e:
        print(f"⚠️ Logo overlay failed: {e}")
        branded_image_path = image_filepath  # fallback to raw image

    print(f"🧠 Memory STM size: {len(memory.stm)} | Episodic entries: {len(memory.episodic)}")

    return {
        **state,
        "generated_image": branded_image_path,   # raw image replaced by branded
        "final_image_path": branded_image_path,
        "final_caption": state.get("caption"),
    }



# --------------------------------------------------------------------------
# Register these in LangGraph
# --------------------------------------------------------------------------

LANGRAPH_AGENT_HANDLERS = {
    "WriterAgent": writer_with_critique,
    "Outliner": outliner_with_critique,
    "Captioner": captioner_with_critique,
    "Designer": designer_with_critique,
    "ImageGenerator": image_generator_agent,
    # "InstagramPostFormatter": instagram_post_formatter_agent,
}
