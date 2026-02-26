class SD_N8NBackend:
    CATEGORY = "StudioDeep/Backends"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webhook_url": ("STRING", {"default": "https://your-n8n-instance.com/webhook/..."}),
            }
        }

    RETURN_TYPES = ("AI_BACKEND",)
    RETURN_NAMES = ("backend",)
    FUNCTION = "build"

    def build(self, webhook_url):
        return ({"type": "n8n", "webhook_url": webhook_url},)


NODE_CLASS_MAPPINGS = {
    "SD_N8NBackend": SD_N8NBackend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_N8NBackend": "N8N Backend",
}
