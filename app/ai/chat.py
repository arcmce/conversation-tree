import os
from openai import OpenAI

_client = None
def client():
    global _client

    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    return _client

def generate_reply(messages: list[dict]) -> str:
    resp = client().chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return resp.choices[0].message.content
