from fastapi import FastAPI

from legal_ai_app.api.routes import router
from legal_ai_app.api.knowledge_routes import router as knowledge_router


app = FastAPI(
    title="Legal AI RAG",
    version="1.0.0",
)

app.include_router(router)
app.include_router(knowledge_router)


@app.get("/")
def root():
    return {
        "message": "Legal AI RAG is running 🚀"
    }