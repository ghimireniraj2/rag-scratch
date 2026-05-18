# backend/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pathlib import Path
import sys
import json

current_dir = Path(__file__).resolve().parent
ingest_dir = current_dir.parent / "ingest"
sys.path.append(str(ingest_dir))
llm_dir = current_dir.parent / "api"
sys.path.append(str(llm_dir))

from model import get_device
from qdrant_store import retrieve
from llm import complete

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-warm the retrieval index on startup."""
    get_device()
    yield

class QueryRequest(BaseModel):
    question: str
    k: int

class ChunkResult(BaseModel):
    text: str
    score: float
    page: int
    source: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    chunks: list[ChunkResult]

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(query_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}

async def stream_response(question: str, chunks:list):
    response = complete(question=question, chunks=chunks, stream=True)
    
    # yield each chunk as SSE
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            yield f"data: {json.dumps({'delta': delta})}\n\n"
    
    # yield final event with sources
    yield f"data: {json.dumps({'done': True, 'sources': chunks})}\n\n"

@app.post("/ask")
async def ask(request: QueryRequest):
    chunks = [result[0] for result in retrieve(collection="rag-sliding", query=request.question, k=request.k)]
    llm_result = complete(question=request.question, chunks=chunks)
    #print(llm_result)
    return QueryResponse(question=request.question, answer=llm_result.choices[0].message.content, chunks=chunks)

@app.post("/ask-stream")
def ask(request: QueryRequest):
    chunks = [result[0] for result in retrieve(collection="rag-sliding", query=request.question, k=request.k)]
    return StreamingResponse(
        stream_response(request.question, chunks),
        media_type="text/event-stream"
    )

### Run as 
# uvicorn api.main:app --reload

### Test
# curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\": \"What is rounding?\", \"k\": 5}"
# Stream
# curl -X POST http://localhost:8000/ask-stream -H "Content-Type: application/json" -d "{\"question\": \"What is rounding?\", \"k\": 5}"  --no-buffer