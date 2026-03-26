import os
import json

DESCRIBERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'describers')


def _load_describers():
    """Load all JSON files from describers/ into a dict keyed by label."""
    data = {}
    if not os.path.isdir(DESCRIBERS_DIR):
        return data
    for fname in sorted(os.listdir(DESCRIBERS_DIR)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(DESCRIBERS_DIR, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                obj = json.load(f)
            label = obj.get('label', fname[:-5])
            data[label] = obj
        except Exception:
            pass
    return data


DESCRIBERS = _load_describers()

# Register API routes so the JS extension can fetch and reload describer data
try:
    from server import PromptServer
    from aiohttp import web

    @PromptServer.instance.routes.get("/studiodeep/describers")
    async def get_describers(request):
        return web.json_response(DESCRIBERS)

    @PromptServer.instance.routes.post("/studiodeep/describers/reload")
    async def reload_describers(request):
        global DESCRIBERS
        DESCRIBERS = _load_describers()
        return web.json_response(DESCRIBERS)
except Exception:
    pass  # Server not available (e.g. during testing)


def _describer_labels():
    labels = list(DESCRIBERS.keys())
    return labels if labels else ["(none)"]


class SD_Describer:
    CATEGORY = "StudioDeep"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "describer": (_describer_labels(),),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("user_prompt", "system_prompt")
    FUNCTION = "get_prompts"

    def get_prompts(self, describer):
        data = DESCRIBERS.get(describer, {})
        user_prompt = data.get("user_prompt", "")
        system_prompt = data.get("system_prompt", "")
        return (user_prompt, system_prompt)


NODE_CLASS_MAPPINGS = {"SD_Describer": SD_Describer}
NODE_DISPLAY_NAME_MAPPINGS = {"SD_Describer": "Describer"}
