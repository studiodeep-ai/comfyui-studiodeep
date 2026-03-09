class SD_FalBackend:
    CATEGORY = "StudioDeep/Backends"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "password": True}),
            }
        }

    RETURN_TYPES = ("FAL_BACKEND",)
    RETURN_NAMES = ("fal_backend",)
    FUNCTION = "build"

    def build(self, api_key):
        if not api_key:
            raise ValueError("fal.ai API key is required — enter your key from fal.ai/dashboard.")
        return ({"api_key": api_key},)


NODE_CLASS_MAPPINGS = {
    "SD_FalBackend": SD_FalBackend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_FalBackend": "fal.ai Backend",
}
