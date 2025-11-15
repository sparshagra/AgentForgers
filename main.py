# from orchestrator import build_graph, stream_workflow
# import os


# def run_workflow(user_prompt, context=None):
#     """
#     Run the LangGraph workflow and also collect a step-by-step timeline.

#     Returns a dict containing:
#       - generated_image
#       - caption
#       - other fields from the final state
#       - timeline: list of step dicts
#     """

#     # Initial state for non-stream fallback
#     initial_state = {"userprompt": user_prompt}
#     if context and isinstance(context, dict) and "logo_path" in context:
#         initial_state["logo_path"] = context["logo_path"]

#     timeline = []
#     last_state = None

#     # --- Try to use streaming to build a timeline ---
#     try:
#         for raw_event in stream_workflow(user_prompt, context=context):
#             # raw_event is like { "WriterAgent": { ...state... } }
#             if not isinstance(raw_event, dict):
#                 continue

#             for node_name, node_state in raw_event.items():
#                 if not isinstance(node_state, dict):
#                     continue

#                 last_state = node_state

#                 payload = {"step": node_name}
#                 # include useful keys when present
#                 for key in [
#                     "enhanced",
#                     "outline",
#                     "caption",
#                     "image_prompt",
#                     "generated_image",
#                     "compliance_blocked",
#                     "compliance_stage",
#                     "compliance_reason",
#                 ]:
#                     if key in node_state:
#                         payload[key] = node_state[key]

#                 timeline.append(payload)

#     except Exception:
#         # If anything goes wrong with streaming, fall back to simple invoke
#         graph = build_graph(context=context)
#         last_state = graph.invoke(initial_state)

#     # If for some reason streaming yielded nothing, still ensure we have a result
#     if last_state is None:
#         graph = build_graph(context=context)
#         last_state = graph.invoke(initial_state)

#     # Compose results as structured dict for API
#     result = {
#         "compliance_blocked": last_state.get("compliance_blocked"),
#         "compliance_stage": last_state.get("compliance_stage"),
#         "compliance_reason": last_state.get("compliance_reason"),
#         "enhanced": last_state.get("enhanced"),
#         "outline": last_state.get("outline"),
#         "critique": last_state.get("critique"),
#         "caption": last_state.get("caption"),  # dict from Captioner
#         "image_prompt": last_state.get("image_prompt"),
#         "generated_image": last_state.get("generated_image"),
#         "image_path": last_state.get("generated_image"),
#         "full_image_path": (
#             os.path.abspath(last_state.get("generated_image", ""))
#             if last_state.get("generated_image")
#             else None
#         ),
#         # NEW: full per-step timeline (what SSE used to stream)
#         "timeline": timeline,
#     }
#     return result

from orchestrator import build_graph, stream_workflow
import os


def run_workflow(user_prompt, context=None):
    """
    Run the LangGraph workflow and also collect a step-by-step timeline.

    Returns a dict containing:
      - generated_image
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

    # If for some reason streaming yielded nothing, still ensure we have a result
    if last_state is None:
        graph = build_graph(context=context)
        last_state = graph.invoke(initial_state)

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
        "generated_image": last_state.get("generated_image"),
        "image_path": last_state.get("generated_image"),
        "full_image_path": (
            os.path.abspath(last_state.get("generated_image", ""))
            if last_state.get("generated_image")
            else None
        ),
        # NEW: full per-step timeline (what SSE used to stream)
        "timeline": timeline,
    }
    return result
