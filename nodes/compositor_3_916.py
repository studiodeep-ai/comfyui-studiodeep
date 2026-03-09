import numpy as np
import torch
from PIL import Image

RESOLUTIONS = {
    "1K (1920×1080)": (1920, 1080),
    "2K (2560×1440)": (2560, 1440),
    "4K (3840×2160)": (3840, 2160),
}

BACKGROUNDS = {
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Gray":  (128, 128, 128),
}


def _tensor_to_pil(image_tensor):
    """Convert a single ComfyUI IMAGE tensor [H, W, C] float32 → PIL RGB."""
    arr = (image_tensor.numpy() * 255).clip(0, 255).astype(np.uint8)
    return Image.fromarray(arr).convert("RGB")


def _pil_to_tensor(pil_img):
    """Convert PIL RGB → ComfyUI IMAGE tensor [1, H, W, C] float32."""
    arr = np.array(pil_img).astype(np.float32) / 255.0
    return torch.from_numpy(arr).unsqueeze(0)


def _crop_to_aspect(pil_img, target_w, target_h):
    """Center-crop a PIL image to match the target panel aspect ratio."""
    w, h = pil_img.size
    target_aspect = target_w / target_h

    if w / h > target_aspect:
        # Image is too wide — crop width
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        pil_img = pil_img.crop((left, 0, left + new_w, h))
    elif w / h < target_aspect:
        # Image is too tall — crop height
        new_h = int(w / target_aspect)
        top = (h - new_h) // 2
        pil_img = pil_img.crop((0, top, w, top + new_h))

    return pil_img


class SD_Compositor3x916:
    CATEGORY = "StudioDeep/Compositing"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1":    ("IMAGE",),
                "image_2":    ("IMAGE",),
                "image_3":    ("IMAGE",),
                "resolution": (list(RESOLUTIONS.keys()),),
                "background": (list(BACKGROUNDS.keys()),),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("moodboard",)
    FUNCTION = "composite"

    def composite(self, image_1, image_2, image_3, resolution, background):
        W, H = RESOLUTIONS[resolution]
        bg_color = BACKGROUNDS[background]

        # Full-bleed layout: panels fill edge to edge, gap only between panels
        gap     = round(W / 120)          # thin gap between panels (~16px at 1K)
        panel_h = H                       # full canvas height, no border
        panel_w = (W - 2 * gap) // 3     # equal thirds minus the two gaps

        canvas = Image.new("RGB", (W, H), color=bg_color)

        for i, img_tensor in enumerate((image_1, image_2, image_3)):
            pil = _tensor_to_pil(img_tensor[0])
            pil = _crop_to_aspect(pil, panel_w, panel_h)
            pil = pil.resize((panel_w, panel_h), Image.LANCZOS)
            x = i * (panel_w + gap)
            canvas.paste(pil, (x, 0))

        return (_pil_to_tensor(canvas),)


NODE_CLASS_MAPPINGS = {
    "SD_Compositor3x916": SD_Compositor3x916,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_Compositor3x916": "3-Panel Moodboard",
}
