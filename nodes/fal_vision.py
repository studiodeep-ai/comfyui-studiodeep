import base64
import io
import json

import numpy as np
import requests
from PIL import Image

FAL_VISION_ENDPOINT = "https://fal.run/openrouter/router/vision"

VISION_MODELS = [
    "google/gemini-2.5-flash",
    "anthropic/claude-sonnet-4.6",
    "anthropic/claude-sonnet-4.5",
    "openai/gpt-4o",
    "qwen/qwen3-vl-235b-a22b-instruct",
    "x-ai/grok-4-fast",
]


def _tensor_to_data_url(image_tensor):
    """Convert a single ComfyUI IMAGE tensor [H, W, C] float32 to a PNG data URL."""
    arr = (image_tensor.numpy() * 255).clip(0, 255).astype(np.uint8)
    pil = Image.fromarray(arr)
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


class SD_FalVision:
    CATEGORY = "StudioDeep/Vision"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "fal_backend": ("FAL_BACKEND",),
                "image":       ("IMAGE",),
                "model":       (VISION_MODELS,),
                "prompt":      ("STRING", {"default": "Describe this image in detail.", "multiline": True}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "reasoning":     ("BOOLEAN", {"default": False}),
                "temperature":   ("FLOAT",   {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05}),
                "max_tokens":    ("INT",     {"default": 0, "min": 0, "max": 8192, "step": 1,
                                              "tooltip": "Maximum tokens to generate. 0 = no limit."}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("response", "usage")
    FUNCTION = "analyze"

    def analyze(
        self,
        fal_backend,
        image,
        model,
        prompt,
        system_prompt="",
        reasoning=False,
        temperature=1.0,
        max_tokens=0,
    ):
        api_key = fal_backend["api_key"]

        # Use first image in batch
        data_url = _tensor_to_data_url(image[0])

        body = {
            "model":      model,
            "prompt":     prompt,
            "image_urls": [data_url],
            "reasoning":  reasoning,
            "temperature": temperature,
        }

        if system_prompt and system_prompt.strip():
            body["system_prompt"] = system_prompt.strip()

        if max_tokens > 0:
            body["max_tokens"] = max_tokens

        response = requests.post(
            FAL_VISION_ENDPOINT,
            json=body,
            headers={
                "Authorization": f"Key {api_key}",
                "Content-Type":  "application/json",
            },
            timeout=120,
        )

        if not response.ok:
            raise RuntimeError(
                f"fal.ai Vision API error {response.status_code}: {response.text}"
            )

        data = response.json()
        output_text = data.get("output", "")
        usage = data.get("usage", {})

        return (output_text, json.dumps(usage, indent=2))


NODE_CLASS_MAPPINGS = {
    "SD_FalVision": SD_FalVision,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_FalVision": "fal.ai Vision",
}
