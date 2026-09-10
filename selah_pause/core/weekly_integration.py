from openai import OpenAI
import os
from core.memory import load_entries

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a quiet observer of patterns.

Rules:
- Do NOT give advice
- Do NOT interpret identity
- Do NOT suggest actions
- Do NOT predict outcomes

Only:
- Notice recurring themes
- Stay neutral and minimal

Output:
- 2 to 4 bullet points
- Optional final line: "It is unclear if any action is needed."
"""

def weekly_intelligence():
    entries = load_entries()

    if not entries:
        return "No entries yet."

    recent = entries[-10:]
    text_block = "\n".join([e["text"] for e in recent])

    response = client.chat.completions.create(
        model="gpt-5-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text_block}
        ]
    )

    return response.choices[0].message.content
