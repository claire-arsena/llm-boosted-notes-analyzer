# 🧠 Analyseur de Notes Intelligentes

Un mini-projet fullstack Python/JS conçu pour **apprendre la mécanique d'intégration IA** (Prompt Engineering, RAG basique, API LLM) dans un environnement propre et jetable.

---

## 🎯 Objectif pédagogique

Ce projet suit une progression en deux phases :

1. **Phase 1 — Structure** : une API FastAPI retourne des données mockées. Le frontend fonctionne déjà, la plomberie est en place.
2. **Phase 2 — Intégration IA** : on remplace le mock par un vrai appel LLM (Groq/Llama 3). C'est là que l'apprentissage commence.

---

## 🗂️ Structure du projet

```
.
├── main.py        # Backend Python — FastAPI
└── index.html     # Frontend — Vanilla JS + Tailwind CSS (CDN)
```

Architecture **Clean** : le Front et le Back sont **totalement séparés** et communiquent uniquement via une API REST.

---

## ⚙️ Installation & Lancement

### Prérequis
- Python 3.8+
- Un terminal

### 1. Installer les dépendances

```bash
pip install fastapi uvicorn
```

### 2. Lancer le backend

```bash
uvicorn main:app --reload
```

Le serveur écoute sur `http://localhost:8000`.

### 3. Ouvrir le frontend

Ouvre simplement `index.html` dans ton navigateur. Aucun serveur frontend requis.

---

## 🔌 API

### `POST /api/analyze-note`

**Corps de la requête :**
```json
{
  "content": "Texte de la note à analyser..."
}
```

**Réponse (mock phase 1) :**
```json
{
  "summary": "Ceci est un faux résumé généré par le backend",
  "sentiment": "Positif",
  "tags": ["tag1", "tag2"]
}
```

---

## 🚀 Phase 2 — Intégrer un vrai LLM (Groq)

### Étape 1 : Créer un compte Groq

Rends-toi sur [console.groq.com](https://console.groq.com) → génère une clé API gratuite.

### Étape 2 : Installer le client Groq

```bash
pip install groq
```

### Étape 3 : Modifier `main.py`

Remplace le mock dans la route `/api/analyze-note` par ce code :

```python
from groq import Groq
import json

client = Groq(api_key="TA_CLE_SECRETE")  # ← remplace par ta vraie clé

prompt_system = """Tu es un analyseur de texte.
Tu dois analyser le texte fourni et répondre UNIQUEMENT avec un objet JSON valide au format exact suivant :
{
  "summary": "Résumé en une phrase",
  "sentiment": "Positif, Négatif ou Neutre",
  "tags": ["mot-clé 1", "mot-clé 2"]
}
Ne rajoute aucun texte avant ou après le JSON."""

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": request.content}
    ],
    model="llama3-8b-8192",
    response_format={"type": "json_object"}
)

return json.loads(chat_completion.choices[0].message.content)
```

### Étape 4 : Tester l'injection de contexte (RAG basique)

Une fois que ça marche, ajoute une variable de contexte dans `main.py` et injecte-la dynamiquement dans le prompt système :

```python
profil_utilisateur = "L'utilisateur est un étudiant en droit qui cherche des insights concis"

prompt_system = f"""Tu es un analyseur de texte personnalisé.
Contexte utilisateur : {profil_utilisateur}
...
"""
```

Observe comment l'IA adapte le ton de son résumé **sans que le frontend n'ait à changer**.  
C'est le principe fondamental du RAG.

---

## 💡 Concepts appris

| Concept | Où ça se passe |
|---|---|
| **Clean Architecture** | Séparation `index.html` / `main.py` |
| **API REST** | Endpoint `POST /api/analyze-note` |
| **Prompt Engineering** | `prompt_system` dans `main.py` |
| **Structured Output** | `response_format: json_object` |
| **RAG basique** | Injection de `profil_utilisateur` dans le prompt |
| **CORS** | Configuration FastAPI pour les requêtes locales |

---

## 🔐 Sécurité

> ⚠️ Ne commite **jamais** ta clé API en dur dans le code.

En production, utilise une variable d'environnement :

```bash
export GROQ_API_KEY="ta_cle_ici"
```

```python
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
```

---

## 📦 Dépendances

| Package | Usage |
|---|---|
| `fastapi` | Framework web Python |
| `uvicorn` | Serveur ASGI pour FastAPI |
| `groq` | Client officiel Groq (Phase 2) |
| Tailwind CSS | Styling frontend (CDN, aucune installation) |
