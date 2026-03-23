import os
import json

INGREDIENTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompt_ingredients')


def _load_ingredients():
    """Load all JSON files from prompt_ingredients/ into a dict keyed by label."""
    data = {}
    if not os.path.isdir(INGREDIENTS_DIR):
        return data
    for fname in sorted(os.listdir(INGREDIENTS_DIR)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(INGREDIENTS_DIR, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                obj = json.load(f)
            label = obj.get('label', fname[:-5])
            data[label] = obj
        except Exception:
            pass
    return data


INGREDIENTS = _load_ingredients()

# Register API route so the JS extension can fetch all ingredient data
try:
    from server import PromptServer
    from aiohttp import web

    @PromptServer.instance.routes.get("/studiodeep/prompt_ingredients")
    async def get_prompt_ingredients(request):
        return web.json_response(INGREDIENTS)

    @PromptServer.instance.routes.post("/studiodeep/prompt_ingredients/reload")
    async def reload_prompt_ingredients(request):
        global INGREDIENTS
        INGREDIENTS = _load_ingredients()
        return web.json_response(INGREDIENTS)
except Exception:
    pass  # Server not available (e.g. during testing)


def _type_labels():
    labels = list(INGREDIENTS.keys())
    return labels if labels else ["(none)"]


def _all_titles():
    """All titles across all types — Python must accept any of them to pass validation."""
    seen = set()
    titles = []
    for type_data in INGREDIENTS.values():
        for item in type_data.get("ingredients", []):
            t = item.get("title")
            if t and t not in seen:
                seen.add(t)
                titles.append(t)
    return titles if titles else ["(none)"]


class SD_PromptIngredient:
    CATEGORY = "StudioDeep"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ingredient_type": (_type_labels(),),
                "ingredient":      (_all_titles(),),
                "custom_override": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "If non-empty, overrides the ingredient selection above",
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build"

    def build(self, ingredient_type, ingredient, custom_override):
        if custom_override.strip():
            return (custom_override.strip(),)
        type_data = INGREDIENTS.get(ingredient_type, {})
        for item in type_data.get("ingredients", []):
            if item["title"] == ingredient:
                return (item["prompt"],)
        return ("",)


NODE_CLASS_MAPPINGS = {"SD_PromptIngredient": SD_PromptIngredient}
NODE_DISPLAY_NAME_MAPPINGS = {"SD_PromptIngredient": "Prompt Ingredient"}
