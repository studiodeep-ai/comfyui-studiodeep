from .llm_backend        import NODE_CLASS_MAPPINGS as _llm_c, NODE_DISPLAY_NAME_MAPPINGS as _llm_d
from .n8n_backend        import NODE_CLASS_MAPPINGS as _n8n_c, NODE_DISPLAY_NAME_MAPPINGS as _n8n_d
from .t2v_prompt_builder import NODE_CLASS_MAPPINGS as _t2v_c, NODE_DISPLAY_NAME_MAPPINGS as _t2v_d

NODE_CLASS_MAPPINGS = {
    **_llm_c,
    **_n8n_c,
    **_t2v_c,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **_llm_d,
    **_n8n_d,
    **_t2v_d,
}
