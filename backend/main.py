from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app = FastAPI(
    title="Analyseur de Notes API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NoteRequest(BaseModel):
    content: str


class NoteAnalysis(BaseModel):
    summary: str
    sentiment: str
    tags: list[str]


@app.get("/api/config")
async def get_config():
    """Expose la config nécessaire au frontend."""
    return JSONResponse({"apiBaseUrl": API_BASE_URL})


@app.post("/api/analyze-note", response_model=NoteAnalysis)
async def analyze_note(note: NoteRequest):
    """Analyse mockée d'une note."""
    return NoteAnalysis(
        summary="Ceci est un faux résumé généré par le backend",
        sentiment="Positif",
        tags=["tag1", "tag2"],
    )


FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
