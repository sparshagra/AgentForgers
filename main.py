# from orchestrator import build_graph
# import os

# def run_workflow(user_prompt, context=None):
#     graph = build_graph(context=context)
#     output = graph.invoke({"userprompt": user_prompt})
#     # Compose results as structured dict for API
#     result = {
#         "compliance_blocked": output.get("compliance_blocked"),
#         "compliance_stage": output.get("compliance_stage"),
#         "compliance_reason": output.get("compliance_reason"),
#         "enhanced": output.get("enhanced"),
#         "outline": output.get("outline"),
#         "critique": output.get("critique"),
#         "caption": output.get("caption"),
#         "image_prompt": output.get("image_prompt"),
#         "generated_image": output.get("generated_image"),
#         "image_path": output.get("generated_image"),
#         "full_image_path": os.path.abspath(output.get("generated_image", "")) if output.get("generated_image") else None
#     }
#     return result

from orchestrator import build_graph
import os

def run_workflow(user_prompt, context=None):
    graph = build_graph(context=context)

    # Build initial state passed into LangGraph
    initial_state = {"userprompt": user_prompt}

    # If FastAPI passed a logo_path in context, attach it to state
    if context and isinstance(context, dict):
        if "logo_path" in context:
            initial_state["logo_path"] = context["logo_path"]

    output = graph.invoke(initial_state)

    # Compose results as structured dict for API
    result = {
        "compliance_blocked": output.get("compliance_blocked"),
        "compliance_stage": output.get("compliance_stage"),
        "compliance_reason": output.get("compliance_reason"),
        "enhanced": output.get("enhanced"),
        "outline": output.get("outline"),
        "critique": output.get("critique"),
        "caption": output.get("caption"),  # dict from Captioner
        "image_prompt": output.get("image_prompt"),
        "generated_image": output.get("generated_image"),
        "image_path": output.get("generated_image"),
        "full_image_path": os.path.abspath(output.get("generated_image", "")) if output.get("generated_image") else None,
    }
    return result
