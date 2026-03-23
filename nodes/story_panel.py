import base64
import io
import json
import os
import re

import numpy as np
from PIL import Image

from .llm_backend import CLAUDE_THINKING_BUDGET

_SP_PATH = os.path.join(os.path.dirname(__file__), '..', 'system_prompts', 'story_panel.md')
with open(_SP_PATH, 'r', encoding='utf-8') as _f:
    _SYSTEM_PROMPT = _f.read()


_MAX_PX = 1568       # Claude's recommended max long edge
_MAX_BYTES = 4_800_000  # stay safely under the 5 MB limit


def _tensor_to_jpg_b64(image_tensor):
    """Convert a single ComfyUI IMAGE tensor [H, W, C] to a JPEG base64 string.

    Resizes so the long edge ≤ 1568 px, then compresses until < 5 MB.
    """
    arr = (image_tensor.numpy() * 255).clip(0, 255).astype(np.uint8)
    pil = Image.fromarray(arr).convert("RGB")

    # Resize if too large
    w, h = pil.size
    long_edge = max(w, h)
    if long_edge > _MAX_PX:
        scale = _MAX_PX / long_edge
        pil = pil.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # Encode as JPEG, reduce quality until under the size limit
    buf = io.BytesIO()
    quality = 85
    while quality >= 20:
        buf.seek(0)
        buf.truncate()
        pil.save(buf, format="JPEG", quality=quality)
        if buf.tell() <= _MAX_BYTES:
            break
        quality -= 10

    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _parse_panels(raw):
    match = re.search(r'\[.*\]', raw, re.DOTALL)
    panels = json.loads(match.group() if match else raw)
    return panels[0]["prompt"], panels[1]["prompt"], panels[2]["prompt"]


class SD_StoryPanel:
    CATEGORY = "StudioDeep"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "backend": ("AI_BACKEND",),
                "image":   ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("panel_1", "panel_2", "panel_3")
    FUNCTION = "generate"

    def generate(self, backend, image):
        b64 = _tensor_to_jpg_b64(image[0])
        provider = backend.get("type", "claude")

        if provider == "claude":
            import anthropic
            client = anthropic.Anthropic(api_key=backend["api_key"])
            kwargs = dict(
                model=backend["model"],
                max_tokens=2000,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {
                        "type": "base64", "media_type": "image/jpeg", "data": b64
                    }},
                    {"type": "text", "text": "Generate the three story panels for this reference image."},
                ]}],
            )
            reasoning = backend.get("reasoning", "off")
            if reasoning != "off":
                budget = CLAUDE_THINKING_BUDGET[reasoning]
                kwargs["thinking"] = {"type": "enabled", "budget_tokens": budget}
                kwargs["max_tokens"] = budget + 2000  # max_tokens must exceed budget_tokens
            response = client.messages.create(**kwargs)
            raw = next(b.text for b in response.content if b.type == "text")

        else:  # openai
            import openai
            data_url = f"data:image/jpeg;base64,{b64}"
            client = openai.OpenAI(api_key=backend["api_key"])
            response = client.chat.completions.create(
                model=backend["model"],
                max_tokens=2000,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": [
                        {"type": "image_url", "image_url": {"url": data_url}},
                        {"type": "text", "text": "Generate the three story panels for this reference image."},
                    ]},
                ],
            )
            raw = response.choices[0].message.content

        return _parse_panels(raw)


NODE_CLASS_MAPPINGS = {"SD_StoryPanel": SD_StoryPanel}
NODE_DISPLAY_NAME_MAPPINGS = {"SD_StoryPanel": "Story Panel"}
