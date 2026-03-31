import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_script(level):
    prompt = f"Create a short English lesson for level {level} in JSON format."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response["choices"][0]["message"]["content"]
        data = json.loads(content)
        data["level"] = level

        return data

    except Exception as e:
        print("⚠️ fallback:", e)
        return {
            "level": level,
            "hook": "STOP saying this",
            "error": "I have 30 years",
            "fix": "I am 30 years old",
            "grammar_tip": "Use 'to be'",
            "class_tip": "I am + age",
            "examples": ["I’m 25", "She’s 40"],
            "real_example": ["How old are you?", "I’m 25"],
            "cta": "Save this"
        }