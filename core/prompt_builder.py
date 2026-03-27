def build_prompt(level):
    return f"""
You are an expert English teacher creating viral short-form content.

Generate ONE English micro-lesson for level {level}.

Rules:
- Focus on common mistakes by Spanish speakers
- Use real-life English
- Keep it short and clear
- Include a 2-line real conversation

Return ONLY valid JSON:

{{
  "level": "{level}",
  "hook": "",
  "error": "",
  "fix": "",
  "grammar_tip": "",
  "class_tip": "",
  "examples": ["", ""],
  "real_example": ["", ""],
  "cta": "Save this"
}}
"""