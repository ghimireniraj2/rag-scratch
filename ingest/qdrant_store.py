from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib
from ingest.model import get_model

_client = None

def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient("http://localhost:6333/")
    return _client
    
def int():
    if not get_client().collection_exists("rag-scratch"):
        get_client().create_collection(
            collection_name="rag-scratch", 
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def upsert(chunks: list[str], embeddings, source: str, page: int):
    get_client().upsert(
    collection_name="rag-scratch",
    wait=True,
    points=[
        PointStruct(id=hashlib.md5(f"{source}-{page}-{i}".encode()).hexdigest(), vector=embeddings[i].tolist(), payload={"file_name": source, "page_number": page, "text": chunk, "chunk_index": i}) for i, chunk in enumerate(chunks)
    ],
)
    
def retrieve(query: str, k: int = 5) -> list [dict]:
    query_embedding = get_model().encode([query])[0]
    search_result = get_client().query_points(
        collection_name="rag-scratch",
        query=query_embedding,
        with_payload=True,
        limit=k
    )
    print(search_result)
    return [ [point.payload["text"], point.score] for point in search_result.points]

int()

