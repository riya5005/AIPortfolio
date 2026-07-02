# Riya Sharma — Portfolio + AI Chatbot

Two separate apps that talk to each other:

```
riya-portfolio/
├── frontend/     → React (Vite) portfolio website
└── backend/      → FastAPI + LangChain + LangGraph chatbot API
```

The frontend is a normal React site (what you already know: components, JSX, DOM-driven state).
The backend is a small Python AI service that answers chatbot questions about you, using
the exact stack from your roadmap:

| Roadmap item      | What's used here            |
|--------------------|------------------------------|
| Language            | Python |
| Backend Framework   | FastAPI |
| Database            | PostgreSQL (optional — logs chat history) |
| Vector Database     | FAISS |
| LLM                 | Open-source model via Hugging Face Inference API (default: Mistral-7B-Instruct) |
| Embeddings          | Open-source, local (sentence-transformers/all-MiniLM-L6-v2) |
| RAG Framework       | LangChain |
| Agents Framework    | LangGraph |
| Deployment          | Docker + Render/AWS |

Everything in the AI layer — embeddings and the LLM — is now open-source and
routed through Hugging Face, no OpenAI/Groq dependency.

---

## 1. Folder structure explained

```
frontend/
  src/
    components/
      Navbar.jsx        → top nav bar
      Hero.jsx           → your photo + name + bio + links (top-left section)
      Skills.jsx         → technical skills grid
      Projects.jsx       → fraud detection + house price projects
      Education.jsx      → B.Tech info
      Footer.jsx
      Chatbot.jsx         → floating chat widget, talks to the backend
    App.jsx               → assembles all sections
    index.css              → all styling (one file, easy to tweak)
  public/
    riya-photo.jpg          → ← put your photo here (see note in that folder)

backend/
  app/
    main.py                 → FastAPI app + /api/chat endpoint
    config.py                → reads your .env settings
    db.py                     → optional Postgres chat-history logging
    rag/
      knowledge_base.py        → ← EDIT THIS to update facts about you
      vectorstore.py             → builds/loads the FAISS index
      chain.py                    → prompt + Groq LLM call
    agent/
      graph.py                     → LangGraph agent (classify → retrieve → generate)
  requirements.txt
  Dockerfile
  .env.example
```

**The one file you'll edit most often:** `backend/app/rag/knowledge_base.py`.
Whenever your resume changes, update the text there — the chatbot's answers come
directly from it (this is what "RAG" means: it retrieves facts from this file
before generating a reply, so it won't make things up).

---

## 2. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — you'll see the site immediately (chatbot will show
a friendly error until the backend is running, that's expected).

To connect it to a deployed backend later, create `frontend/.env` from
`.env.example` and set `VITE_API_URL` to your backend's URL.

---

## 3. Run the backend

### 3.1 Get a free Hugging Face token
Go to https://huggingface.co → sign up (free) → Settings → Access Tokens →
"New token" → role **Read** is enough. Copy it.

You'll also need to accept the model's usage terms once, on its page, e.g.
https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 → click "Agree and
access repository" (only needed for gated models like Mistral/Llama; fully
open models skip this step).

### 3.2 Set up and run

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# open .env and paste your HF_TOKEN

uvicorn app.main:app --reload --port 8000
```

**If you'd rather not deal with a gated model:** open `.env` and change
`HF_MODEL` to a fully open, ungated instruct model, e.g.:
```
HF_MODEL=HuggingFaceH4/zephyr-7b-beta
```
No extra "agree to terms" step needed for models like that.

The first request will download a small local embedding model
(`all-MiniLM-L6-v2`, ~80MB, free, no API key needed) and build the FAISS
index automatically — this happens once and is cached in
`backend/vectorstore_data/`.

Test it directly:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are Riya qualifications?"}'
```

### 3.3 (Optional) PostgreSQL chat logging
If you want to see what visitors ask, spin up a Postgres instance (locally,
via Docker, or a free tier like Render/Supabase/Neon) and set `DATABASE_URL`
in `.env`. If you leave it blank, the chatbot still works — it just won't log
anything.

---

## 4. How the chatbot actually works (LangChain + LangGraph)

1. **Frontend** sends `{ message: "..." }` to `POST /api/chat`.
2. **LangGraph agent** (`agent/graph.py`) runs a 3-step graph:
   - `classify_intent` — looks at keywords to guess if you're asking about
     links, projects, skills, or education.
   - `retrieve` — searches the FAISS vector index for the most relevant facts
     from `knowledge_base.py`.
   - `generate` — sends those facts + your question to an open-source LLM
     hosted on the Hugging Face Inference API (LangChain's `ChatHuggingFace`)
     with a system prompt that keeps it grounded in your real resume data.
3. The answer streams back to the floating chat widget.

The suggested-prompt buttons ("What are Riya's qualifications?", "Which tech
stack does Riya know?", etc.) just pre-fill common questions so visitors don't
have to think of what to ask — you can add more in
`frontend/src/components/Chatbot.jsx` (`suggestedPrompts` array).

---

## 5. Deploying (matches your roadmap: Docker + AWS/Render)

**Backend (Render — easiest for a student project):**
1. Push this repo to GitHub.
2. On Render: New → Web Service → connect the repo → set root directory to `backend`.
3. Render auto-detects the `Dockerfile`. Add environment variables
   (`HF_TOKEN`, `HF_MODEL`, `DATABASE_URL` if using Postgres, `FRONTEND_ORIGIN`
   = your deployed frontend URL).
4. Deploy. You'll get a URL like `https://riya-chatbot.onrender.com`.

**Frontend (Render Static Site, Vercel, or Netlify all work):**
1. Set `VITE_API_URL` env var to your backend's Render URL.
2. Build command: `npm run build`, publish directory: `dist`.

**Docker locally (optional, to test before deploying):**
```bash
cd backend
docker build -t riya-chatbot-api .
docker run -p 8000:8000 --env-file .env riya-chatbot-api
```

---

## 6. Quick customization checklist

- [ ] Add your real photo to `frontend/public/riya-photo.jpg`
- [ ] Update LinkedIn/email in `frontend/src/components/Hero.jsx`
- [ ] Update `backend/app/rag/knowledge_base.py` if your resume changes
- [ ] Get a Hugging Face token and add it to `backend/.env`
- [ ] Deploy backend first, then point the frontend's `VITE_API_URL` at it
