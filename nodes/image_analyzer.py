import base64
import io
import json

import numpy as np
import requests
from PIL import Image


def _tensor_to_data_url(image_tensor):
    """Convert a single ComfyUI IMAGE tensor [H, W, C] float32 to a PNG data URL."""
    arr = (image_tensor.numpy() * 255).clip(0, 255).astype(np.uint8)
    pil = Image.fromarray(arr)
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


class SD_ImageAnalyzer:
    CATEGORY = "StudioDeep/N8N"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "n8n_backend": ("AI_BACKEND",),
                "image":       ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_output",)
    FUNCTION = "analyze"

    def analyze(self, n8n_backend, image):
        data_url = _tensor_to_data_url(image[0])

        payload = {"image_url": data_url}
        auth = (n8n_backend["username"], n8n_backend["password"]) if n8n_backend.get("username") else None

        response = requests.post(n8n_backend["webhook_url"], json=payload, auth=auth, timeout=120)
        response.raise_for_status()

        try:
            data = response.json()
        except Exception:
            return (response.text,)

        if isinstance(data, dict):
            result = data.get("output") or data.get("data") or data.get("json_output") or data
        else:
            result = data

        if isinstance(result, (dict, list)):
            return (json.dumps(result, indent=2),)

        # Try to parse the string as JSON and reformat it
        result_str = str(result)
        try:
            parsed = json.loads(result_str)
            return (json.dumps(parsed, indent=2),)
        except Exception:
            return (result_str,)


NODE_CLASS_MAPPINGS = {
    "SD_ImageAnalyzer": SD_ImageAnalyzer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_ImageAnalyzer": "Image Analyzer",
}
