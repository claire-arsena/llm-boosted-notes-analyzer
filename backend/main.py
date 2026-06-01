from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL    = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
USER_PROFILE  = os.getenv("USER_PROFILE", "")
API_BASE_URL  = os.getenv("API_BASE_URL", "http://localhost:8000")
CORS_ORIGINS  = os.getenv("CORS_ORIGINS", "*").split(",")

app = FastAPI(title="Analyseur de Notes API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

SYSTEM_PROMPT = """Tu es un analyseur de texte expert.
Tu dois analyser le texte fourni et répondre de manière très sadique et agressive avec beaucoup de répartie mais UNIQUEMENT avec un objet JSON valide au format exact suivant :
{{
  "summary": "Un résumé clair et concis en une ou deux phrases",
  "sentiment": "Positif, Négatif ou Neutre",
  "tags": ["mot-clé 1", "mot-clé 2", "mot-clé 3"]
}}
Ne rajoute aucun texte, explication ou formatage avant ou après le JSON.
{profile_context}"""


class NoteRequest(BaseModel):
    content: str


class NoteAnalysis(BaseModel):
    summary: str
    sentiment: str
    tags: list[str]


@app.get("/api/config")
async def get_config():
    return JSONResponse({"apiBaseUrl": API_BASE_URL})


@app.post("/api/analyze-note", response_model=NoteAnalysis)
async def analyze_note(note: NoteRequest):
    if not client:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY manquante dans le .env"
        )

    profile_context = ""
    if USER_PROFILE:
        profile_context = f"\nContexte utilisateur : {USER_PROFILE}"

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(profile_context=profile_context),
                },
                {
                    "role": "user",
                    "content": note.content,
                },
            ],
            model=GROQ_MODEL,
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        raw = completion.choices[0].message.content
        data = json.loads(raw)

        return NoteAnalysis(
            summary=data.get("summary", "Pas de résumé"),
            sentiment=data.get("sentiment", "Neutre"),
            tags=data.get("tags", []),
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Le LLM n'a pas renvoyé du JSON valide")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur Groq : {str(e)}")


FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
