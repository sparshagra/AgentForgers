# compliance_agent.py

import json
from backend.core.llm_api import call_llm_2  # or call_llm if you prefer a single token


def _parse_bool(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        v = val.strip().lower()
        if v in {"true", "yes", "allow", "allowed"}:
            return True
        if v in {"false", "no", "block", "blocked", "deny", "denied"}:
            return False
    return False


def _safe_json_parse(text: str):
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    # fallback: treat whole text as reason, mark blocked to be safe
    return {"allowed": False, "reason": text.strip() or "Unclear response from compliance model."}


def run_text_compliance(stage: str, text: str) -> dict:
    """
    LLM-based compliance check for text inputs:
    - stage: 'prompt' or 'image_prompt' etc.
    - text: the content to evaluate.
    Returns: {"allowed": bool, "reason": str}
    """
    if not text:
        return {"allowed": False, "reason": "Empty content provided for compliance check."}

    system_prompt = (
        "You are a strict compliance officer for social media marketing content "
        "intended for Instagram.\n"
        "You must check legal, ethical, and platform policy compliance, including:\n"
        "- No hate, harassment, or discrimination.\n"
        "- No explicit sexual content or sexualization of minors.\n"
        "- No self-harm encouragement, extreme violence, or illegal activities.\n"
        "- No dangerous medical or health claims.\n"
        "- No misleading, fraudulent, or deceptive advertising.\n"
        "- Respect privacy, consent, and child safety.\n\n"
        "You MUST respond ONLY in valid JSON, no extra text."
    )

    user_prompt = f"""
You are reviewing the following {stage} for legal, ethical, and Instagram policy compliance.

CONTENT:
{text}

Return a JSON object with exactly these keys:
- "allowed": true or false
- "reason": a short one-line explanation

Example:
{{"allowed": true, "reason": "Content is compliant and safe for Instagram."}}
"""

    raw = call_llm_2(
        model_id="meta-llama/Llama-3.2-3B-Instruct",
        prompt=user_prompt,
        system_prompt=system_prompt,
        max_tokens=150,
        temperature=0.2,
    )

    data = _safe_json_parse(raw)
    allowed = _parse_bool(data.get("allowed", False))
    reason = str(data.get("reason", "")).strip() or "No explicit reason provided by model."

    return {"allowed": allowed, "reason": reason}


def run_image_compliance(image_path: str, context_text: str = "") -> dict:
    """
    LLM-based compliance check for the final image, based on its description/context.
    NOTE: We are text-only here; image_path is for logging and future vision use.
    Returns: {"allowed": bool, "reason": str}
    """
    description = context_text.strip() or "(No additional description provided.)"

    system_prompt = (
        "You are a strict compliance officer for Instagram posts.\n"
        "Given a description and context of an image, decide if it is safe and compliant.\n"
        "Focus on legal, ethical, and platform safety.\n"
        "Respond ONLY in JSON."
    )

    user_prompt = f"""
You are validating a final image for Instagram posting.

IMAGE PATH (for reference only): {image_path}

IMAGE CONTEXT / DESCRIPTION:
{description}

Return a JSON object:
{{"allowed": true/false, "reason": "short explanation"}}
"""

    raw = call_llm_2(
        model_id="meta-llama/Llama-3.2-3B-Instruct",
        prompt=user_prompt,
        system_prompt=system_prompt,
        max_tokens=150,
        temperature=0.2,
    )

    data = _safe_json_parse(raw)
    allowed = _parse_bool(data.get("allowed", False))
    reason = str(data.get("reason", "")).strip() or "No explicit reason provided by model."

    return {"allowed": allowed, "reason": reason}
