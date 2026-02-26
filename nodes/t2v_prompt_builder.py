import json
import requests

# ---------------------------------------------------------------------------
# Option lists — "auto" always first so it's the default
# ---------------------------------------------------------------------------

MEDIUM_OPTIONS = [
    "auto",
    # Analog Film
    "8mm / Super 8 Film", "16mm Film", "35mm Film", "70mm / IMAX Film", "Polaroid / Instant Film",
    # Broadcast & Digital
    "Digital Cinema (Arri/Red)", "VHS / Camcorder", "CCTV / Security Cam",
    "GoPro / Action Cam", "iPhone / Smartphone",
    # Animation & Synthetic
    "Unreal Engine 5 / CGI", "Stop-Motion Animation", "Anime / Cel Shaded",
    "3D Claymation", "Cybernetic Glitch Art",
    # Photography & Editorial
    "Fashion Editorial", "National Geographic Style", "Street Photography",
]

SHOT_OPTIONS = [
    "auto",
    "Extreme Close-Up", "Close-Up", "Medium Close-Up", "Medium Shot",
    "Medium Full Shot", "Full Shot", "Wide Shot", "Extreme Wide Shot",
]

ANGLE_OPTIONS = [
    "auto",
    "Eye-Level", "Low Angle", "High Angle", "Overhead Shot",
    "Dutch Angle", "Point-of-View", "Over-the-Shoulder",
]

MOVEMENT_OPTIONS = [
    "auto",
    "Static", "Pan", "Tilt", "Jib Up/Down (Crane)",
    "Push-In (Dolly In)", "Pull-Out (Dolly Out)", "Truck (Left/Right)",
    "Orbit/Arc", "Zoom", "Handheld",
]

FOCUS_OPTIONS = [
    "auto",
    "Rack Focus", "Deep Focus", "Shallow Focus", "Split-Field Diopter",
]

LIGHTING_OPTIONS = [
    "auto",
    "Chiaroscuro", "Three-Point Lighting", "Motivated Lighting",
    "Neon Noir (Cyberpunk)", "High-Key Lighting", "Low-Key Lighting",
    "Volumetric Lighting", "Color Gels", "Rim Lighting / Hair Light",
    "Rembrandt Lighting", "Practical Lighting", "Haze / Atmospheric",
]

COLOR_OPTIONS = [
    "auto",
    "Orange & Teal", "Monochromatic", "Analogous", "Complementary",
]

OPTIONS_MAP = {
    "medium":   MEDIUM_OPTIONS[1:],
    "shot":     SHOT_OPTIONS[1:],
    "angle":    ANGLE_OPTIONS[1:],
    "movement": MOVEMENT_OPTIONS[1:],
    "focus":    FOCUS_OPTIONS[1:],
    "lighting": LIGHTING_OPTIONS[1:],
    "color":    COLOR_OPTIONS[1:],
}

# Template order: [Medium] [Shot] [Angle] [Movement] [Focus] {subject} [Lighting] [Color]
PRE_SUBJECT  = ["medium", "shot", "angle", "movement", "focus"]
POST_SUBJECT = ["lighting", "color"]

# ------------------------------------------------------------------
# System prompts
# ------------------------------------------------------------------

SYSTEM_PROMPT_FILL = """You are a text-to-video prompt specialist.

Template: [Medium] [Shot] [Angle] [Movement] [Focus] {subject} [Lighting] [Color]

Your job: given a scene description and some locked values, fill in the remaining fields
by choosing exactly one value per field from the provided option lists.

Return ONLY a valid JSON object with these 7 keys:
medium, shot, angle, movement, focus, lighting, color

No explanation. No markdown. No code fences. Raw JSON only."""

GLUE_RULES = """
Follow this exact sentence structure:
  [Medium], [Shot] from a [Angle]. [Movement] camera with [Focus]. {Subject, written as a full sentence.} [Lighting] casting the scene. [Color] color palette.

Adapt the connectors naturally to the values — for example:
  - "from a [Low Angle]" / "at [Eye-Level]" / "from an [Overhead Shot]"
  - "[Static] camera" / "[Handheld] camera movement" / "[Pan] following the action"
  - "with [Deep Focus]" / "with [Shallow Focus] and soft bokeh"
  - "[Chiaroscuro] lighting with dramatic shadows" / "[Motivated Lighting] from a nearby window"
  - "[Orange & Teal] color palette" / "[Monochromatic] palette in deep greens"

Rules:
- Keep ALL bracketed elements exactly as written, in template order — never alter what is inside them
- Use proper punctuation: comma after medium, period after focus, period after subject
- Do not invent new visual elements beyond what the scene description implies
- Write one cohesive paragraph, not a list"""

SYSTEM_PROMPT_ENHANCE = """You are a text-to-video prompt specialist.

Template: [Medium] [Shot] [Angle] [Movement] [Focus] {subject} [Lighting] [Color]

Step 1 — fill in the remaining fields by choosing exactly one value per field from the provided option lists.
Step 2 — write an enhanced_prompt that reads like a real director's shot description.
""" + GLUE_RULES + """

Example output:
{
  "medium": "35mm Film",
  "shot": "Medium Close-Up",
  "angle": "Dutch Angle",
  "movement": "Static",
  "focus": "Deep Focus",
  "lighting": "Chiaroscuro",
  "color": "Monochromatic",
  "enhanced_prompt": "[35mm Film], [Medium Close-Up] with a [Dutch Angle]. [Static] camera and [Deep Focus]. A detective in a trench coat smoking a cigarette under a streetlamp. [Chiaroscuro] lighting with heavy Venetian blind shadows. [Monochromatic] silver-screen color palette."
}

Return ONLY a valid JSON object with these 8 keys:
medium, shot, angle, movement, focus, lighting, color, enhanced_prompt

No explanation. No markdown. No code fences. Raw JSON only."""

SYSTEM_PROMPT_ENHANCE_ONLY = """You are a text-to-video prompt specialist.

You will receive a structured text-to-video prompt with bracketed template elements.
Rewrite it as a single, fluent director's shot description.
""" + GLUE_RULES + """

Example input:
[35mm Film] [Medium Close-Up] [Dutch Angle] [Static] [Deep Focus] a detective in a trench coat smoking a cigarette under a streetlamp [Chiaroscuro] [Monochromatic]

Example output:
[35mm Film], [Medium Close-Up] with a [Dutch Angle]. [Static] camera and [Deep Focus]. A detective in a trench coat smoking a cigarette under a streetlamp. [Chiaroscuro] lighting with heavy Venetian blind shadows. [Monochromatic] silver-screen color palette.

Return ONLY the enhanced prompt string. No explanation, no JSON, no markdown."""


class SD_T2VPromptBuilder:
    CATEGORY = "StudioDeep"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "backend":  ("AI_BACKEND",),
                "prompt":   ("STRING", {"multiline": True, "default": ""}),
                "medium":   (MEDIUM_OPTIONS,),
                "shot":     (SHOT_OPTIONS,),
                "angle":    (ANGLE_OPTIONS,),
                "movement": (MOVEMENT_OPTIONS,),
                "focus":    (FOCUS_OPTIONS,),
                "lighting": (LIGHTING_OPTIONS,),
                "color":    (COLOR_OPTIONS,),
                "enhance":  ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"

    def build_prompt(self, backend, prompt, medium, shot, angle, movement, focus, lighting, color, enhance):
        ingredients = {
            "medium": medium, "shot": shot, "angle": angle,
            "movement": movement, "focus": focus,
            "lighting": lighting, "color": color,
        }

        locked      = {k: v for k, v in ingredients.items() if v != "auto"}
        auto_fields = [k for k, v in ingredients.items() if v == "auto"]

        # N8N handles everything — pass enhance flag along
        if backend["type"] == "n8n":
            return (self._call_n8n(backend, prompt, locked, auto_fields, enhance),)

        # No auto fields and no enhance — pure assembly, no API call
        if not auto_fields and not enhance:
            return (self._assemble(locked, prompt),)

        # No auto fields but enhance is on — just glue the assembled string
        if not auto_fields and enhance:
            assembled = self._assemble(locked, prompt)
            return (self._enhance_only(backend, assembled),)

        # Auto fields exist — fill them, optionally enhance in the same call
        filled, enhanced_prompt = self._call_llm(backend, prompt, locked, auto_fields, enhance)

        if enhance and enhanced_prompt:
            return (enhanced_prompt,)
        return (self._assemble(filled, prompt),)

    # ------------------------------------------------------------------
    # Assembly
    # ------------------------------------------------------------------

    def _assemble(self, ingredients, subject):
        parts = [f"[{ingredients[k]}]" for k in PRE_SUBJECT if k in ingredients]
        if subject:
            parts.append(subject)
        parts += [f"[{ingredients[k]}]" for k in POST_SUBJECT if k in ingredients]
        return " ".join(parts)

    # ------------------------------------------------------------------
    # LLM path (Claude or OpenAI)
    # ------------------------------------------------------------------

    def _call_llm(self, backend, prompt, locked, auto_fields, enhance):
        """Fill auto fields and optionally return an enhanced prompt in one call."""
        system = SYSTEM_PROMPT_ENHANCE if enhance else SYSTEM_PROMPT_FILL

        locked_lines = "\n".join(f'  {k}: "{v}"  (keep as-is)' for k, v in locked.items())
        auto_lines   = "\n".join(f"  {k}: {OPTIONS_MAP[k]}" for k in auto_fields)

        keys = "medium, shot, angle, movement, focus, lighting, color, enhanced_prompt" if enhance \
               else "medium, shot, angle, movement, focus, lighting, color"

        user_msg = (
            f'Scene description: "{prompt}"\n\n'
            f"Locked values (do not change):\n{locked_lines}\n\n"
            f"Fill in these fields (pick one value from each list):\n{auto_lines}\n\n"
            f"Return JSON with all keys: {keys}."
        )

        if backend["type"] == "claude":
            raw = self._call_claude(backend, system, user_msg)
        else:
            raw = self._call_openai(backend, system, user_msg)

        data = json.loads(raw.strip())
        filled = {**locked, **{k: data[k] for k in auto_fields if k in data}}
        enhanced_prompt = data.get("enhanced_prompt") if enhance else None
        return filled, enhanced_prompt

    def _enhance_only(self, backend, assembled_prompt):
        """Add glue text to an already-assembled prompt (no auto fields)."""
        if backend["type"] == "claude":
            raw = self._call_claude(backend, SYSTEM_PROMPT_ENHANCE_ONLY, assembled_prompt)
        else:
            raw = self._call_openai(backend, SYSTEM_PROMPT_ENHANCE_ONLY, assembled_prompt)
        return raw.strip()

    def _call_claude(self, backend, system, user_msg):
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed — run: pip install anthropic")

        client   = anthropic.Anthropic(api_key=backend["api_key"])
        response = client.messages.create(
            model=backend["model"],
            max_tokens=512,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        return response.content[0].text

    def _call_openai(self, backend, system, user_msg):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed — run: pip install openai")

        client   = OpenAI(api_key=backend["api_key"])
        response = client.chat.completions.create(
            model=backend["model"],
            max_tokens=512,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user_msg},
            ],
        )
        return response.choices[0].message.content

    # ------------------------------------------------------------------
    # N8N path
    # ------------------------------------------------------------------

    def _call_n8n(self, backend, prompt, locked, auto_fields, enhance):
        payload = {
            "prompt":   prompt,
            "locked":   locked,
            "auto":     auto_fields,
            "options":  {k: OPTIONS_MAP[k] for k in auto_fields},
            "enhance":  enhance,
        }
        response = requests.post(backend["webhook_url"], json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("prompt", "")


NODE_CLASS_MAPPINGS = {
    "SD_T2VPromptBuilder": SD_T2VPromptBuilder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SD_T2VPromptBuilder": "T2V Prompt Builder",
}
