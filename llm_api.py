# this code is for handling different llm api calls with memory integration,so we can run llm with different tokens to reduce stress on a single provider
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

def call_llm(
    model_id,
    prompt,
    system_prompt=None,
    max_tokens=200,
    temperature=0.2,
    memory=None,  # 🧠 Added optional memory
):
    HF_TOKEN = os.environ.get("HF_TOKEN")
    assert HF_TOKEN, "HF_TOKEN must be set in environment"
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HF_TOKEN,
    )

    # 🧠 SMART MEMORY INJECTION
    memory_context = ""
    if memory:
        # Take last 5 memory entries (or fewer)
        stm_entries = memory.recall_stm(5)

        # Include only relevant tool outputs (skip internal or redundant logs)
        allowed_tools = {
            "enhance_prompt",
            "outline_generator",
            "caption_generator",
            "image_prompt",
            "critic"
        }

        # Build compact memory summary with truncation (to avoid token bloat)
        recent_contexts = []
        for entry in stm_entries:
            tool_name = entry.get("tool", "unknown")
            if tool_name in allowed_tools:
                output_text = str(entry.get("output", ""))[:200].replace("\n", " ")
                recent_contexts.append(f"{tool_name}: {output_text}")

        # Join as readable context (if non-empty)
        if recent_contexts:
            memory_context = (
                "\n\n[Recent relevant memory context]\n" +
                "\n".join(f"- {ctx}" for ctx in recent_contexts)
            )

    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({
        "role": "user",
        "content": prompt + memory_context,  # inject compact memory here
    })

 
    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return completion.choices[0].message.content.strip()

# To reduce the stress on the current inference provider

def call_llm_2(
    model_id,
    prompt,
    system_prompt=None,
    max_tokens=200,
    temperature=0.2,
    memory=None,  # 🧠 Added optional memory
):
    HF_TOKEN = os.environ.get("HF_TOKEN_2")
    assert HF_TOKEN, "HF_TOKEN must be set in environment"
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HF_TOKEN,
    )

    # 🧠 SMART MEMORY INJECTION
    memory_context = ""
    if memory:
        # Take last 5 memory entries (or fewer)
        stm_entries = memory.recall_stm(5)

        # Include only relevant tool outputs (skip internal or redundant logs)
        allowed_tools = {
            "enhance_prompt",
            "outline_generator",
            "caption_generator",
            "image_prompt",
            "critic"
        }

        # Build compact memory summary with truncation (to avoid token bloat)
        recent_contexts = []
        for entry in stm_entries:
            tool_name = entry.get("tool", "unknown")
            if tool_name in allowed_tools:
                output_text = str(entry.get("output", ""))[:200].replace("\n", " ")
                recent_contexts.append(f"{tool_name}: {output_text}")

        # Join as readable context (if non-empty)
        if recent_contexts:
            memory_context = (
                "\n\n[Recent relevant memory context]\n" +
                "\n".join(f"- {ctx}" for ctx in recent_contexts)
            )

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({
        "role": "user",
        "content": prompt + memory_context,  # inject compact memory here
    })

   
    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return completion.choices[0].message.content.strip()

# To reduce the stress on the current inference provider

def call_llm_3(
    model_id,
    prompt,
    system_prompt=None,
    max_tokens=200,
    temperature=0.2,
    memory=None,  
):
    HF_TOKEN = os.environ.get("HF_TOKEN_3")
    assert HF_TOKEN, "HF_TOKEN must be set in environment"
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HF_TOKEN,
    )

    # SMART MEMORY INJECTION
    memory_context = ""
    if memory:
        # Take last 5 memory entries (or fewer)
        stm_entries = memory.recall_stm(5)

        # Include only relevant tool outputs (skip internal or redundant logs)
        allowed_tools = {
            "enhance_prompt",
            "outline_generator",
            "caption_generator",
            "image_prompt",
            "critic"
        }

        # Build compact memory summary with truncation (to avoid token bloat)
        recent_contexts = []
        for entry in stm_entries:
            tool_name = entry.get("tool", "unknown")
            if tool_name in allowed_tools:
                output_text = str(entry.get("output", ""))[:200].replace("\n", " ")
                recent_contexts.append(f"{tool_name}: {output_text}")

        # Join as readable context (if non-empty)
        if recent_contexts:
            memory_context = (
                "\n\n[Recent relevant memory context]\n" +
                "\n".join(f"- {ctx}" for ctx in recent_contexts)
            )

    # onstruct the actual chat messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({
        "role": "user",
        "content": prompt + memory_context,  # inject compact memory here
    })

    # LLM call
    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return completion.choices[0].message.content.strip()
