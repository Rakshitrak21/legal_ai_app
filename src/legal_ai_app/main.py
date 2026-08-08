from fastapi import FastAPI
from legal_ai_app.api.routes import router

app = FastAPI(
    title="Legal AI RAG",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Legal AI RAG is running 🚀"
    }