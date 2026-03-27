import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from core.prompt_builder import build_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_script(level):
    prompt = build_prompt(level)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return only JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        print("JSON error:")
        print(content)
        return None


def generate_multiple(levels, count_per_level=1):
    scripts = []

    for level in levels:
        for _ in range(count_per_level):
            script = generate_script(level)
            if script:
                scripts.append(script)

    return scripts