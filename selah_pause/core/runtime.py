import os
from openai import OpenAI
from core.memory import save_entry, load_entries

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_context(current_input, history):
    history_text = "\n".join([f"- {e['text']}" for e in history])

    return f"""
Current reflection:
{current_input}

Recent reflections:
{history_text}
"""

def get_prompt(context):
    return f"""
You are a calm and non-directive assistant.

Follow strictly:
- One neutral observation
- At most one gentle question (optional)
- One bounded suggestion OR permission to pause

Do NOT:
- Give advice
- Give instructions
- Assume action is required

Context:
{context}
"""

def validate_response(text):
    parts = [p for p in text.split("\n\n") if p.strip()]
    return len(parts) == 3


def kairoseed_run(user_input: str):

    # Save memory
    save_entry(user_input)

    # Load recent entries
    history = load_entries()[-5:]

    # Build prompt
    context = build_context(user_input, history)
    prompt = get_prompt(context)

    # Call LLM
    response = client.chat.completions.create(
        model="gpt-5-mini",
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content

    # Validate structure
    if not validate_response(output):
        return "…"

    return output
