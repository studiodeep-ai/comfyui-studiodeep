from .llm_backend        import NODE_CLASS_MAPPINGS as _llm_c, NODE_DISPLAY_NAME_MAPPINGS as _llm_d
from .n8n_backend        import NODE_CLASS_MAPPINGS as _n8n_c, NODE_DISPLAY_NAME_MAPPINGS as _n8n_d
from .t2v_prompt_builder import NODE_CLASS_MAPPINGS as _t2v_c, NODE_DISPLAY_NAME_MAPPINGS as _t2v_d
from .fal_backend        import NODE_CLASS_MAPPINGS as _fal_b_c, NODE_DISPLAY_NAME_MAPPINGS as _fal_b_d
from .fal_vision         import NODE_CLASS_MAPPINGS as _fal_v_c, NODE_DISPLAY_NAME_MAPPINGS as _fal_v_d
from .json_shot_splitter import NODE_CLASS_MAPPINGS as _json_c,  NODE_DISPLAY_NAME_MAPPINGS as _json_d
from .string_passthrough import NODE_CLASS_MAPPINGS as _sp_c,    NODE_DISPLAY_NAME_MAPPINGS as _sp_d
from .compositor_3_916          import NODE_CLASS_MAPPINGS as _comp_c,  NODE_DISPLAY_NAME_MAPPINGS as _comp_d
from .image_prompt_by_seed_idea import NODE_CLASS_MAPPINGS as _seed_c,  NODE_DISPLAY_NAME_MAPPINGS as _seed_d
from .image_analyzer            import NODE_CLASS_MAPPINGS as _n8n_ia_c, NODE_DISPLAY_NAME_MAPPINGS as _n8n_ia_d
from .template_image            import NODE_CLASS_MAPPINGS as _tmpl_c,   NODE_DISPLAY_NAME_MAPPINGS as _tmpl_d
from .prompt_ingredient         import NODE_CLASS_MAPPINGS as _pi_c,     NODE_DISPLAY_NAME_MAPPINGS as _pi_d
from .string_template           import NODE_CLASS_MAPPINGS as _st_c,     NODE_DISPLAY_NAME_MAPPINGS as _st_d
from .story_panel               import NODE_CLASS_MAPPINGS as _stp_c,    NODE_DISPLAY_NAME_MAPPINGS as _stp_d

NODE_CLASS_MAPPINGS = {
    **_llm_c,
    **_n8n_c,
    **_t2v_c,
    **_fal_b_c,
    **_fal_v_c,
    **_json_c,
    **_sp_c,
    **_comp_c,
    **_seed_c,
    **_n8n_ia_c,
    **_tmpl_c,
    **_pi_c,
    **_st_c,
    **_stp_c,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **_llm_d,
    **_n8n_d,
    **_t2v_d,
    **_fal_b_d,
    **_fal_v_d,
    **_json_d,
    **_sp_d,
    **_comp_d,
    **_seed_d,
    **_n8n_ia_d,
    **_tmpl_d,
    **_pi_d,
    **_st_d,
    **_stp_d,
}
