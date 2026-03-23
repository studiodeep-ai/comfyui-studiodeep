import os
import torch
import numpy as np
from PIL import Image

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}


def _list_templates():
    if not os.path.isdir(TEMPLATES_DIR):
        return ["(none)"]
    files = [f for f in sorted(os.listdir(TEMPLATES_DIR))
             if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
    return files if files else ["(none)"]


class SD_TemplateImage:
    CATEGORY = "StudioDeep"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": (_list_templates(),),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "load_template"

    def load_template(self, template):
        path = os.path.join(TEMPLATES_DIR, template)
        img = Image.open(path).convert("RGB")
        arr = np.array(img).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr).unsqueeze(0)  # [1, H, W, C]
        return (tensor,)


NODE_CLASS_MAPPINGS = {"SD_TemplateImage": SD_TemplateImage}
NODE_DISPLAY_NAME_MAPPINGS = {"SD_TemplateImage": "Template Image"}
