# backend/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import sys

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

@app.post("/ask")
async def ask(request: QueryRequest):
    chunks = [result[0] for result in retrieve(collection="rag-sliding", query=request.question, k=request.k)]
    llm_result = complete(question=request.question, chunks=chunks)
    #print(llm_result)
    return QueryResponse(question=request.question, answer=llm_result, chunks=chunks)



### Run as 
# uvicorn api.main:app --reload