import pdfplumber
import re
from qdrant_store import upsert, init
from embed import get_model

def load_pdf(file:str) -> list[dict]:
    pages = []

    try:
        with pdfplumber.open(file) as pdf:
            print(f"Loading pdf file:", {file})

            for i, page in enumerate(pdf.pages[:30]):
                page_text = page.extract_text()
                if page_text:
                    pages.append({"page": i + 1, "text": page_text})

    except FileNotFoundError:
        print(f"file not found", {file})
        return []
    
    return pages

def get_max(strings:list[str]):
    return max(len(s) for s in strings)

def get_min(strings:list[str]):
    return min(len(s) for s in strings)

def get_average(strings:list[str]):
    return sum(len(s) for s in strings) / len(strings)

def chunk_fixed(text: str, size: int = 512) -> list[str]:
    return [text[i:i + size] for i in range(0, len(text), size)]

def chunk_sentences(text: str, n: int = 5) -> list[str]:
    sentences = re.split(r'(?<=[.?!])\s+', text)
    return ["".join(sentences[i: i + n]) for i in range(0, len(sentences), n)]

def chunk_sliding(text: str, size: int = 512, step: int = 256) -> list[str]:
    return [text[i:i + size] for i in range(0, len(text), step) if len(text[i:i + size]) > 50]

def chunk_stats(strings:list[str]):
    print(f"Chunks count: {len(strings)}")
    print(f"Min chunk size: {get_min(strings)}")
    print(f"Max chunk size: {get_max(strings)}")
    print(f"Average chunk size: {get_average(strings)}")
    print()

_file_name = "openstax-prealgebra.pdf"
_file_path = f"data/raw/{_file_name}"
_pages = load_pdf(file=_file_path)

print("Creating rag-sliding")
init(collection="rag-sliding")
for i, _page in enumerate(_pages):
    _chunks_sliding = chunk_sliding(_page["text"])    
    _embeddings = get_model().encode(_chunks_sliding)
    #print(f"Page {i}: {len(_chunks_sliding)} chunks")
    if len(_chunks_sliding) > 0:
        upsert(collection="rag-sliding", chunks=_chunks_sliding, embeddings=_embeddings, source=_file_name, page=i) 
    
print("Creating rag-fixed")
init(collection="rag-fixed")
for i, _page in enumerate(_pages):
    _chunk_fixed = chunk_fixed(_page["text"])    
    _embeddings = get_model().encode(_chunk_fixed)
    #print(f"Page {i}: {len(_chunk_fixed)} chunks")
    if len(_chunk_fixed) > 0:
        upsert(collection="rag-fixed", chunks=_chunk_fixed, embeddings=_embeddings, source=_file_name, page=i) 

print("Creating rag-sentences")
init(collection="rag-sentences")
for i, _page in enumerate(_pages):
    _chunk_sentences = chunk_sentences(_page["text"])    
    _embeddings = get_model().encode(_chunk_sentences)
    #print(f"Page {i}: {len(_chunk_sentences)} chunks")
    if len(_chunk_sentences) > 0:
        upsert(collection="rag-sentences", chunks=_chunk_sentences, embeddings=_embeddings, source=_file_name, page=i) 
