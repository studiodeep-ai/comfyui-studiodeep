import requests

MODEL_LABELS = ["GenHQ (Universal)", "Nano Banana"]
MODEL_VALUES  = {"GenHQ (Universal)": "genhq-universal", "Nano Banana": "nano-banana"}

class SD_ImagePromptBySeedIdea:
    CATEGORY = "StudioDeep"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "backend":    ("AI_BACKEND",),
                "model":      (MODEL_LABELS, {"default": "Nano Banana"}),
                "seed_idea":  ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"

    def run(self, backend, model, seed_idea):
        payload = {
            "seed_idea": seed_idea,
            "model":     MODEL_VALUES[model],
        }
        auth = (backend["username"], backend["password"]) if backend.get("username") else None
        response = requests.post(backend["webhook_url"], json=payload, auth=auth, timeout=30)
        response.raise_for_status()
        return (response.json().get("prompt", ""),)

NODE_CLASS_MAPPINGS = {"SD_ImagePromptBySeedIdea": SD_ImagePromptBySeedIdea}
NODE_DISPLAY_NAME_MAPPINGS = {"SD_ImagePromptBySeedIdea": "Image Prompt by Seed Idea"}
