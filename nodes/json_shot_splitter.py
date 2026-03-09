import json

MAX_SHOTS = 20


class SD_JSONShotSplitter:
    CATEGORY = "StudioDeep/JSON"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {"forceInput": True}),
                "shot_count":  ("INT", {"default": 2, "min": 1, "max": MAX_SHOTS, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",) * MAX_SHOTS
    RETURN_NAMES = tuple(f"shot_{i+1}" for i in range(MAX_SHOTS))
    FUNCTION = "split"

    def split(self, json_string, shot_count):
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

        manifest = data.get("shot_manifest", {})

        outputs = []
        for i in range(1, shot_count + 1):
            shot = manifest.get(f"shot_{i}", {})
            # Pass strings through; serialize objects/arrays to formatted JSON
            outputs.append(shot if isinstance(shot, str) else json.dumps(shot, indent=2))

        # Pad to MAX_SHOTS so the return tuple always matches RETURN_TYPES length
        outputs += [""] * (MAX_SHOTS - len(outputs))
        return tuple(outputs)


NODE_CLASS_MAPPINGS = {
    "SD_JSONShotSplitter": SD_JSONShotSplitter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_JSONShotSplitter": "JSON Shot Splitter",
}
