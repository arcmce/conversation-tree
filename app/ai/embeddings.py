import os
import numpy as np
from openai import OpenAI

MODEL = "text-embedding-3-small"

_client = None
def client():
    global _client
    
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    return _client

def embed_text(text: str) -> list[float]:
    text = text.strip()
    resp = client().embeddings.create(model=MODEL, input=text)

    return resp.data[0].embedding

def cosine_similarity(a: list[float], b: list[float]) -> float:
    va = np.array(a, dtype=np.float32)
    vb = np.array(b, dtype=np.float32)
    denom = (np.linalg.norm(va) * np.linalg.norm(vb)) or 1e-12

    return float(np.dot(va, vb) / denom)
    