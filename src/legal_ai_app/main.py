from fastapi import FastAPI

from legal_ai_app.api.routes import router
from legal_ai_app.api.knowledge_routes import router as knowledge_router
from legal_ai_app.api.document_routes import router as document_router
from legal_ai_app.api.agent_routes import router as agent_router



app = FastAPI(
    title="Legal AI RAG",
    version="1.0.0",
)

app.include_router(router)
app.include_router(knowledge_router)
app.include_router(document_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "message": "Legal AI RAG is running 🚀"
    }