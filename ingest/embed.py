import numpy as np
import torch
from model import get_model
torch.set_grad_enabled(False)

def cosine_similarity(a, b) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query: str, embeddings, chunks: list[str], topk: int = 5) -> list[dict]:
    query_embedding = get_model().encode([query])[0]
    scores = {i : cosine_similarity(query_embedding, embedding) for i, embedding in enumerate(embeddings)}
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [(chunks[i], score) for i, score in sorted_scores[:topk]]
