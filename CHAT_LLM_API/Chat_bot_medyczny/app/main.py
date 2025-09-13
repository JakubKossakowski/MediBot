# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Chat_bot_medyczny.app.api.routes.settings import router as settings_router
from Chat_bot_medyczny.app.db import init_db
app = FastAPI(title="Chatbot Medical - API")

# Allow local Next.js dev origin and production origin - dostosuj
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(settings_router)

@app.on_event("startup")
def on_startup():
    init_db()
