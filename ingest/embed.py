from sentence_transformers import SentenceTransformer
from load import chunk_fixed, chunk_sentences, chunk_sliding, load_pdf

import numpy as np

import torch
torch.set_grad_enabled(False)

_model = None
_device = None


def get_device():
    global _device

    # if _device == None:
    #     try:
    #         import torch_directml
    #         _device = torch_directml.device()
    #         return _device
    #     except ImportError:
    #         pass
    # else:
    #     _device = "cpu"

    _device = "cpu"


    return _device

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2", device=get_device())
    return _model

def cosine_similarity(a, b) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query: str, embeddings, chunks: list[str], topk: int = 5) -> list[dict]:
    query_embedding = get_model().encode([query])[0]
    scores = {i : cosine_similarity(query_embedding, embedding) for i, embedding in enumerate(embeddings)}
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [(chunks[i], score) for i, score in sorted_scores[:topk]]


_pages = load_pdf(file="data/raw/openstax-prealgebra.pdf")
_chunks_sliding = chunk_sliding(_pages[18]["text"])
_embeddings = get_model().encode(_chunks_sliding)
_search_results = search(query="What is a whole number?", embeddings=_embeddings, chunks=_chunks_sliding)
print()
print(_search_results)
