class SD_StringPassthrough:
    CATEGORY = "StudioDeep/Utils"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "optional": {
                # Widget-only — updated by JS after execution, never used by Python
                "preview": ("STRING", {"default": "", "multiline": True}),
            },
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "passthrough"

    def passthrough(self, text, preview=""):
        return {"ui": {"text": [text]}, "result": (text,)}


NODE_CLASS_MAPPINGS = {"SD_StringPassthrough": SD_StringPassthrough}
NODE_DISPLAY_NAME_MAPPINGS = {"SD_StringPassthrough": "String Passthrough"}
