from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS（Vercelのプレビュー/本番を許可）
origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Support-AI Backend on Render"}
