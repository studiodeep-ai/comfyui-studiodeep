class SD_N8NBackend:
    CATEGORY = "StudioDeep/Backends"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webhook_url": ("STRING", {"default": "https://your-n8n-instance.com/webhook/..."}),
                "username":    ("STRING", {"default": ""}),
                "password":    ("STRING", {"default": "", "password": True}),
            }
        }

    RETURN_TYPES = ("AI_BACKEND",)
    RETURN_NAMES = ("backend",)
    FUNCTION = "build"

    def build(self, webhook_url, username, password):
        return ({"type": "n8n", "webhook_url": webhook_url, "username": username, "password": password},)


NODE_CLASS_MAPPINGS = {
    "SD_N8NBackend": SD_N8NBackend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_N8NBackend": "N8N Backend",
}
