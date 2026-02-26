import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass  # fall back to os.environ

CLAUDE_DEFAULT_MODEL = "claude-sonnet-4-6"
OPENAI_DEFAULT_MODEL = "gpt-4o"


class SD_LLMBackend:
    CATEGORY = "StudioDeep/Backends"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": (["Claude", "OpenAI"],),
                "model": ("STRING", {"default": CLAUDE_DEFAULT_MODEL}),
            }
        }

    RETURN_TYPES = ("AI_BACKEND",)
    RETURN_NAMES = ("backend",)
    FUNCTION = "build"

    def build(self, provider, model):
        defaults = {
            "Claude": CLAUDE_DEFAULT_MODEL,
            "OpenAI": OPENAI_DEFAULT_MODEL,
        }
        # Auto-correct model when user switches provider without updating the field
        if not model or model in (CLAUDE_DEFAULT_MODEL, OPENAI_DEFAULT_MODEL):
            model = defaults[provider]

        if provider == "Claude":
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found — add it to StudioDeep/.env")
            return ({"type": "claude", "model": model, "api_key": api_key},)

        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found — add it to StudioDeep/.env")
        return ({"type": "openai", "model": model, "api_key": api_key},)


NODE_CLASS_MAPPINGS = {
    "SD_LLMBackend": SD_LLMBackend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_LLMBackend": "LLM Backend",
}
