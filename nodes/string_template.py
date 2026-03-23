class SD_StringTemplate:
    CATEGORY = "StudioDeep"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"

    def execute(self, template, **kwargs):
        result = template
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", str(value) if value is not None else "")
        return (result,)


NODE_CLASS_MAPPINGS = {"SD_StringTemplate": SD_StringTemplate}
NODE_DISPLAY_NAME_MAPPINGS = {"SD_StringTemplate": "String Template"}
