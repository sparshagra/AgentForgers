# AgentForgers — Backend Study Plan

**Living document.** Updated as we go. Status legend: ⬜ not started · 🟡 in progress · ✅ done

| Field | Value |
|---|---|
| Repo | `AgentForgers` (branch `refactor/backend-structure`) |
| Scope | Backend only. Frontend (`frontend/`, React + Vite + TS) is out of scope. |
| Backend size | ~2,450 lines of Python across 23 modules |
| Last updated | 2026-08-23 — Phase 0 complete |

---

## 0. What this project actually is

An **AI marketing-campaign generator for Instagram**. A user registers a brand
(name, idea, logo, IG credentials). They then either:

- **Option 1 — Interactive:** type a prompt → a multi-agent pipeline writes a
  creative brief, an outline, a caption, an image prompt, generates an image,
  stamps the brand logo on it, and returns it for preview → user clicks publish.
- **Option 2 — Scheduled:** register a festival + date → 48 hours before, a cron
  job auto-generates the campaign and **emails the user** a preview with three
  links: *Publish / Regenerate / Abort*. Clicking a link hits a backend endpoint.

The interesting engineering is the **dynamic LangGraph orchestration**: instead of
hard-coded edges, a "Decision" node uses an LLM to pick which agent runs next,
gated by a dependency table. Compliance checks are woven in at three stages.

---

## 1. Phase 0 — Restructure ✅ DONE

The backend used to be **23 flat `.py` files at the repo root**. It is now:

```
AgentForgers/
├── backend/                        ← all backend Python (a real package)
│   ├── app.py                      ← FastAPI app: every HTTP endpoint
│   ├── graph/                      ← LangGraph orchestration layer
│   │   ├── orchestrator.py         ← builds the graph, Decision node, streaming
│   │   ├── workflow_runner.py      ← (was main.py) runs graph, builds timeline
│   │   ├── nodes.py                ← (was agents.py) the 5 graph node handlers
│   │   └── tools.py                ← LangChain @tool wrappers around agents
│   ├── agents/                     ← leaf agents: one LLM call each
│   │   ├── prompt_enhancer.py
│   │   ├── outline_generator.py
│   │   ├── critic_agent.py
│   │   ├── caption_generator.py
│   │   ├── image_prompt_generator.py
│   │   └── compliance_agent.py     ← safety gate (text + image)
│   ├── core/                       ← shared primitives
│   │   ├── llm_api.py              ← 3 near-identical LLM callers (token rotation)
│   │   └── agent_memory.py         ← STM / LTM / episodic memory class
│   ├── media/
│   │   ├── image_api.py            ← FLUX.1-schnell text-to-image (ACTIVE)
│   │   ├── image_generator.py      ← older FLUX.1-dev variant (UNUSED)
│   │   └── logo_dropper.py         ← Pillow: 1080×1080 canvas + logo overlay
│   ├── publishing/
│   │   ├── publisher.py            ← caption assembly + approval-email builder
│   │   ├── email_sender.py         ← Gmail SMTP with attachment
│   │   └── insta_local.py          ← instagrapi photo upload
│   ├── scheduling/
│   │   ├── scheduler_utils.py      ← JSON-file task CRUD, "48h before" logic
│   │   └── scheduler_runner.py     ← dumb 60-second polling loop
│   └── storage/
│       └── user_utils.py           ← users/<name>/{login,brand,logo} on disk
├── legacy/
│   └── agent_controller.py         ← ⚠️ DEAD: first hard-coded graph attempt
├── assets/brand_logo.png           ← default fallback logo
├── docs/CODEBASE_STUDY_PLAN.md     ← this file
├── frontend/                       ← out of scope
└── requirements.txt · README.md · LICENSE · .gitignore
```

**What changed mechanically:**
- 24 files moved with `git mv` (history preserved).
- `main.py` → `graph/workflow_runner.py` (it was never the app entry point — `app.py` is).
- `agents.py` → `graph/nodes.py` (it holds LangGraph *nodes*, not agents; the actual agents now live in `agents/`).
- All 25 intra-project imports rewritten to absolute `backend.<pkg>.<mod>` form.
- `brand_logo.png` → `assets/brand_logo.png`; the fallback in `nodes.py:309` updated.
- Dead code annotated in-place: `legacy/agent_controller.py` and two tools in
  `graph/tools.py` that import modules (`image_critic`, `image_prompt_critic`)
  which **do not exist in this repo**.
- Added `.gitignore` (runtime dirs `outputs/ users/ scheduled/ uploads/` are
  generated data, not source, and were being tracked).

**How to run now** (from repo root, so relative paths like `outputs/` still resolve):

```bash
uvicorn backend.app:app --reload --port 8000
```

Scheduler poller, in a second terminal:

```bash
python -m backend.scheduling.scheduler_runner
```

> ⚠️ Verified: the full import chain `backend.app → graph.workflow_runner →
> graph.orchestrator` resolves correctly. It stops only at `import langgraph`,
> which is not installed in the shell I tested from. `compileall` passes on
> every file. Install deps and it runs as before — **no endpoint changed**, so
> the frontend needs no edits.

---

## 2. Framework primer — read this before the code

### FastAPI (in 5 lines)
A Python web framework where you declare an endpoint as a plain function with
**type-annotated parameters**, and FastAPI does the rest: it parses the request,
validates/coerces types via Pydantic, returns JSON automatically, and generates
interactive API docs at `/docs` for free. `async def` endpoints run on an event
loop, so I/O-bound work scales without threads. In this repo it's the entire
HTTP surface — `backend/app.py`, ~15 endpoints, using `Form(...)`/`File(...)`
for multipart uploads (logo images), plus `StaticFiles` mounts so the frontend
can `<img src>` generated images directly.

### LangChain
A toolkit for building LLM applications. Its ideas you'll meet here:
- **Tool** — a Python function wrapped with the `@tool` decorator. The decorator
  reads the function's signature + docstring and turns it into a schema an LLM
  could call. You invoke it with `my_tool.invoke({"arg": value})`, not `my_tool(value)`.
- (LangChain also has chains, retrievers, memory, agents — **this repo uses
  almost none of that.** It uses `@tool` as a thin, uniform wrapper and calls
  the OpenAI SDK directly. Don't expect idiomatic LangChain here.)

### LangGraph
LangChain's sibling for **stateful, cyclic agent workflows**. Where a chain is a
straight line, a graph can loop, branch, and revisit. The five concepts:

| Concept | Meaning | Where in this repo |
|---|---|---|
| **State** | A dict (or Pydantic model) passed between nodes; each node returns an updated copy | `state_schema = dict` — plain dict, `orchestrator.py:8` |
| **Node** | A function `state → new_state` | The 5 handlers in `graph/nodes.py` |
| **Edge** | Fixed "after A, go to B" | `g.add_edge(name, "Decision")` |
| **Conditional edge** | A router function picks the next node at runtime | `add_conditional_edges("Decision", route_decision, ...)` |
| **`END`** | Sentinel that terminates the graph | Returned by `route_decision` |

You build a `StateGraph`, `add_node`/`add_edge`, `set_entry_point`, then
`.compile()` it into a runnable. Then `.invoke(state)` for a single result, or
`.stream(state)` to yield `{node_name: state}` after each node — which is exactly
how this repo builds its step-by-step frontend timeline.

**The pattern used here (worth understanding — it's the project's core idea):**
every agent node has an unconditional edge back to a central `Decision` node.
`Decision` looks at which keys exist in state, computes which agents have their
dependencies satisfied and haven't run yet, and then — if more than one is
eligible — *asks a small LLM to choose*. That's a **hub-and-spoke dynamic
router**, not a fixed DAG. A `loop_count > 15` safeguard prevents runaway cycles.

### The other frameworks present

| Library | Version | Role |
|---|---|---|
| **openai** | 2.7.2 | Used as a *client*, but pointed at `https://router.huggingface.co/v1` — HF exposes an OpenAI-compatible API, so you get the OpenAI SDK ergonomics with HF-hosted Llama models. |
| **huggingface-hub** | 0.36.0 | `InferenceClient.text_to_image()` for image generation (FLUX.1-schnell). |
| **Pydantic** | 2.11.7 | FastAPI's validation engine. Also used directly in the dead `legacy/agent_controller.py`. |
| **Pillow** | 12.0.0 | Image compositing: white 1080² canvas, `ImageOps.contain`, logo alpha paste. |
| **instagrapi** | 2.2.1 | Unofficial Instagram private-API client — logs in with user/password and uploads a photo. |
| **uvicorn** | 0.38.0 | The ASGI server that actually runs FastAPI. |
| **python-dotenv** | 1.2.1 | Loads `HF_TOKEN`, `HF_TOKEN_2`, `HF_TOKEN_3`, SMTP creds from `.env`. |
| **rich** | 14.2.0 | Pretty console printing (only in the dead legacy file). |

**Models in use** — all via HF router, all small:
- `meta-llama/Llama-3.2-1B-Instruct` — prompt enhancer, outline generator
- `meta-llama/Llama-3.2-3B-Instruct` — critic, caption, image prompt, compliance, **and the Decision router**
- `black-forest-labs/FLUX.1-schnell` — image generation

---

## 3. Reading order — three passes, increasing depth

### Pass 1 — Overall shape (≈30 min, 4 files, skim)
Goal: be able to draw the request→response arrow on a whiteboard.

| # | File | What to extract |
|---|---|---|
| 1 | [backend/app.py](../backend/app.py) | Skim endpoint names only. Two flows exist: `/run_workflow` (interactive) and `/scheduler/*` (scheduled). |
| 2 | [backend/graph/workflow_runner.py](../backend/graph/workflow_runner.py) | 105 lines, the whole file. The single bridge between HTTP and the graph. |
| 3 | [backend/graph/orchestrator.py](../backend/graph/orchestrator.py) | `AGENT_DEPENDENCIES` (lines 10–17) and `build_graph` (109–125). This is the architecture in 20 lines. |
| 4 | [backend/graph/nodes.py](../backend/graph/nodes.py) | Just `LANGRAPH_AGENT_HANDLERS` at the bottom (337–344) — the cast list. |

**Checkpoint question:** *Why does every node point back to `Decision` instead of
to the next agent?*

### Pass 2 — Layer by layer (the main study, 6 layers)

Each layer below is a self-contained session. Detailed notes get appended to
§5 as we complete them.

| Layer | Files | Focus |
|---|---|---|
| **L1 — Orchestration** ⬜ | `graph/orchestrator.py` | Dependency gating, LLM routing, `should_halt_compliance`, streaming, the loop safeguard |
| **L2 — Nodes & critique loops** ⬜ | `graph/nodes.py`, `graph/tools.py` | The generate→critique→regenerate pattern repeated 4×; `@tool` wrapping; `extract_output` |
| **L3 — Agents & LLM plumbing** ⬜ | `agents/*.py`, `core/llm_api.py`, `core/agent_memory.py` | Prompt engineering per agent, JSON-mode captioning, 3-token rotation, memory injection |
| **L4 — Compliance & media** ⬜ | `agents/compliance_agent.py`, `media/*.py` | 3-stage safety gate, fail-closed parsing, FLUX generation, Pillow logo compositing |
| **L5 — API surface** ⬜ | `app.py` (full read) | Multipart uploads, static mounts, cron secret, path handling |
| **L6 — Scheduling & publishing** ⬜ | `scheduling/*`, `publishing/*`, `storage/user_utils.py` | File-as-database, 48h trigger, email-as-UI approval, SMTP + instagrapi |

### Pass 3 — Cross-cutting deep dives ⬜
Only after L1–L6. These cut *across* layers:

1. **State-key lifecycle** — trace every key in the graph state dict: who writes
   `enhanced`, `outline`, `caption`, `image_prompt`, `generated_image`,
   `raw_image_path`, `compliance_*`; and which are read downstream.
2. **The three compliance gates** — prompt / image-prompt / final-image. Where
   each fires, how a block propagates to `Decision`, and what the user sees.
3. **Error handling & failure modes** — what happens when the HF API 503s, when
   the LLM returns non-JSON, when instagrapi login fails.
4. **Memory: designed vs. actually used** — `AgentMemory` supports STM/LTM/episodic,
   but trace what's genuinely fed back into prompts.
5. **Security & correctness review** — plaintext IG passwords on disk, SHA-256
   without salt, `allow_origins=["*"]`, unauthenticated GET endpoints that
   publish to Instagram, path-join inconsistencies around `outputs/`.

---

## 4. Model & effort recommendations per layer

I **cannot switch models myself** — you'll need to switch manually. I'll prompt
you at the end of each response when the next layer wants a different model.

Effort = reasoning depth (`/effort` if available in your client).

| Layer | Model | Effort | Why |
|---|---|---|---|
| Phase 0 restructure | **Opus 5** | medium | Multi-file refactor with import-graph correctness. ✅ done |
| L1 Orchestration | **Opus 5** | **high** | The subtlest code in the repo — dynamic routing, halt conditions, cyclic graph semantics. Worth full reasoning. |
| L2 Nodes & tools | **Opus 5** | medium | Repetitive pattern; once you see one critique loop you've seen four. Depth is in *why* it's structured this way. |
| L3 Agents & LLM | **Sonnet 5** | medium | Mostly prompt strings + three copy-pasted functions. Sonnet is plenty and much cheaper. |
| L4 Compliance & media | **Sonnet 5** | medium | Straightforward, self-contained. Bump to Opus only for the fail-closed-parsing discussion. |
| L5 API surface | **Sonnet 5** | low–medium | Standard FastAPI CRUD. Skim-friendly. |
| L6 Scheduling & publishing | **Sonnet 5** | medium | Simple file I/O + SMTP. The *design* discussion (why files, not a DB) is the valuable part. |
| Pass 3 cross-cutting | **Opus 5** | **high** | Whole-system tracing and a security review — exactly where deep reasoning pays. |
| Any "explain this concept" detour | **Sonnet 5** | low | Framework Q&A doesn't need Opus. |

**Subagents:** not needed for this. The backend is ~2.5k lines and fits in
context; spawning agents would re-derive context we already have and lose the
teaching thread. The one exception worth considering is Pass 3 item 5
(security review) — the built-in `/security-review` skill could run over the
diff independently.

---

## 5. Notes log — filled in as we complete layers

### Phase 0 ✅ — Restructure (2026-08-23)
Done. Findings worth carrying forward:

- **`main.py` was misleadingly named.** It is not the entry point; `app.py` is.
  Renamed to `workflow_runner.py`.
- **`agents.py` contained no agents**, it contained LangGraph node handlers.
  Renamed to `graph/nodes.py`; the real agents were the loose leaf modules.
- **Dead code found:** `agent_controller.py` (the original hard-coded graph)
  imports two modules that don't exist — it cannot run. Two tools in `tools.py`
  (`image_prompt_critic_tool`, `image_critic_tool`) are likewise broken but were
  never registered, so nothing failed at runtime. `ALL_TOOLS` is exported and
  never imported. `media/image_generator.py` is superseded by `media/image_api.py`.
- **Runtime state lives in flat files**, not a database: `users/<name>/*.json`,
  `scheduled/<task_id>.json`, `outputs/*.png`. Now gitignored.
- **Three HF tokens** (`HF_TOKEN`, `HF_TOKEN_2`, `HF_TOKEN_3`) exist purely to
  spread rate limits — `call_llm`, `call_llm_2`, `call_llm_3` are otherwise
  identical copy-paste. Prime refactor candidate later.
- **Real bug found while tracing paths (queued for Pass 3).** The convention is:
  `nodes.py:326` emits `outputs/final_post.png` → `workflow_runner.py:68`
  strips it to the bare filename `final_post.png` → callers re-prepend `outputs/`.
  `/scheduler/run_due` does that correctly (`app.py:364`), but
  `/scheduler/regenerate` does **not** — `app.py:509` stores the bare filename
  into `task["last_result"]["image_path"]`. `/scheduler/publish` (`app.py:424`)
  then reads that value and hands it straight to instagrapi.
  **Consequence:** publish works after a normal scheduled generation, but a user
  who clicks *Regenerate* and then *Publish* hits a file-not-found, because the
  image lives in `outputs/`, not the CWD.
- **Related:** the branded output filename is hard-coded (`final_post.png`), so
  every run overwrites the same file — two concurrent workflows would clobber
  each other. The *raw* image is timestamped (`image_api.py`), only the branded
  one is not.

### L1 — Orchestration ⬜
_(pending)_

### L2 — Nodes & critique loops ⬜
_(pending)_

### L3 — Agents & LLM plumbing ⬜
_(pending)_

### L4 — Compliance & media ⬜
_(pending)_

### L5 — API surface ⬜
_(pending)_

### L6 — Scheduling & publishing ⬜
_(pending)_

### Pass 3 — Cross-cutting ⬜
_(pending)_
