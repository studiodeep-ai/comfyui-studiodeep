# StudioDeep — ComfyUI Nodes

Custom ComfyUI nodes for StudioDeep — AI-assisted text-to-video prompt building with LLM and N8N backend integrations.

## Nodes

### LLM Backend
Send prompts to a language model (Anthropic/OpenAI) and receive text responses directly in your ComfyUI workflow.

### N8N Backend
Trigger N8N webhooks from within ComfyUI and pass data between your automation workflows and image/video pipelines.

### T2V Prompt Builder
Structured prompt assembly for text-to-video models. Combines scene, style, motion, and camera direction fields into a single optimised prompt string.

## Installation

**Via ComfyUI Manager** (recommended)
Search for "StudioDeep" in the Custom Node Manager and install.

**Manual**
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/studiodeep-ai/comfyui-studiodeep StudioDeep
pip install -r StudioDeep/requirements.txt
```

## Setup

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Then edit `.env` with your credentials. ComfyUI must be restarted after changes to `.env`.

## Adding New Nodes

Each node lives in its own file under `nodes/`. To add a new one:

1. Create `nodes/<node_name>.py` with the class and its own `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS`
2. Add one import line and spread it into both dicts in `nodes/__init__.py`
3. Bump `version` in `pyproject.toml` (PATCH for small additions, MINOR for new categories)
4. Push to `main` — the GitHub Action publishes to the Registry automatically

## License

MIT — see [LICENSE](LICENSE)
