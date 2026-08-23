from backend.graph.orchestrator import build_graph, stream_workflow
import os


def run_workflow(user_prompt, context=None):
    """
    Run the LangGraph workflow and also collect a step-by-step timeline.

    Returns a dict containing:
      - generated_image  (JUST THE FILENAME, for frontend)
      - raw_image_path   (full backend path, for publishing)
      - caption
      - other fields from the final state
      - timeline: list of step dicts
    """

    # Initial state for non-stream fallback
    initial_state = {"userprompt": user_prompt}
    if context and isinstance(context, dict) and "logo_path" in context:
        initial_state["logo_path"] = context["logo_path"]

    timeline = []
    last_state = None

    # --- Try to use streaming to build a timeline ---
    try:
        for raw_event in stream_workflow(user_prompt, context=context):
            # raw_event is like { "WriterAgent": { ...state... } }
            if not isinstance(raw_event, dict):
                continue

            for node_name, node_state in raw_event.items():
                if not isinstance(node_state, dict):
                    continue

                last_state = node_state

                payload = {"step": node_name}
                # include useful keys when present
                for key in [
                    "enhanced",
                    "outline",
                    "caption",
                    "image_prompt",
                    "generated_image",
                    "compliance_blocked",
                    "compliance_stage",
                    "compliance_reason",
                ]:
                    if key in node_state:
                        payload[key] = node_state[key]

                timeline.append(payload)

    except Exception:
        # If anything goes wrong with streaming, fall back to simple invoke
        graph = build_graph(context=context)
        last_state = graph.invoke(initial_state)

    # If streaming yielded nothing, still ensure we have a result
    if last_state is None:
        graph = build_graph(context=context)
        last_state = graph.invoke(initial_state)

  
    raw_generated_path = last_state.get("generated_image")
    generated_filename = (
        os.path.basename(raw_generated_path)
        if raw_generated_path
        else None
    )

    # raw_image_path was added in ImageGenerator and MUST be returned unchanged
    raw_image_path = last_state.get("raw_image_path")

    # Compose results as structured dict for API
    result = {
        "compliance_blocked": last_state.get("compliance_blocked"),
        "compliance_stage": last_state.get("compliance_stage"),
        "compliance_reason": last_state.get("compliance_reason"),
        "enhanced": last_state.get("enhanced"),
        "outline": last_state.get("outline"),
        "critique": last_state.get("critique"),
        "caption": last_state.get("caption"),  # dict from Captioner
        "image_prompt": last_state.get("image_prompt"),

        # --- IMPORTANT: return ONLY filename for frontend ---
        "generated_image": generated_filename,
        "image_path": generated_filename,

        # Backend full path (for publishing)
        "raw_image_path": raw_image_path,

        # Full path for server use
        "full_image_path": (
            os.path.abspath(raw_generated_path)
            if raw_generated_path
            else None
        ),

        # Full per-step timeline (for frontend)
        "timeline": timeline,
    }

    return result
