CLAUDE_MODELS = [
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "claude-haiku-4-5-20251001",
]

OPENAI_MODELS = [
    "gpt-5o",
    "gpt-5o-mini",
]

ALL_MODELS = CLAUDE_MODELS + OPENAI_MODELS


class SD_LLMBackend:
    CATEGORY = "StudioDeep/Backends"

    # budget_tokens for Claude extended thinking per effort level
    CLAUDE_THINKING_BUDGET = {"low": 1024, "medium": 5000, "high": 16000}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider":  (["Claude", "OpenAI"],),
                "model":     (ALL_MODELS, {"default": CLAUDE_MODELS[1]}),
                "reasoning": (["off", "low", "medium", "high"], {"default": "off"}),
                "api_key":   ("STRING", {"default": "", "password": True}),
            }
        }

    RETURN_TYPES = ("AI_BACKEND",)
    RETURN_NAMES = ("backend",)
    FUNCTION = "build"

    def build(self, provider, model, api_key, reasoning="off"):
        if not api_key:
            raise ValueError(f"API key is required — enter your {'Anthropic' if provider == 'Claude' else 'OpenAI'} API key in the node.")

        return ({"type": "claude" if provider == "Claude" else "openai", "model": model, "api_key": api_key, "reasoning": reasoning},)


NODE_CLASS_MAPPINGS = {
    "SD_LLMBackend": SD_LLMBackend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_LLMBackend": "LLM Backend",
}
