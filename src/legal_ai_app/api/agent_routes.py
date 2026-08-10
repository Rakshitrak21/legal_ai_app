from fastapi import APIRouter

from legal_ai_app.models.schemas import (
    AskRequest,
    AskResponse,
)

from legal_ai_app.agent.legal_agent import (
    LegalAgent,
)

from legal_ai_app.services.citation_service import (
    CitationService,
)


router = APIRouter(
    prefix="/agent",
    tags=["Legal Agent"],
)


legal_agent = LegalAgent()
citation_service = CitationService()


@router.post(
    "/ask",
    response_model=AskResponse,
)
async def agent_ask(
    request: AskRequest,
):

    # Run the ReAct agent.
    result = legal_agent.run(
        question=request.question,
        max_steps=5,
    )

    # Generate final answer from structured evidence.
    answer = legal_agent.generate_final_answer(
        question=request.question,
        evidence=result["evidence"],
    )

    # Collect Documents for existing citation service.
    documents = []

    for observation in result["observations"]:

        documents.extend(
            observation.get(
                "documents",
                []
            )
        )

    # Build API sources.
    sources = citation_service.build_sources(
        documents
    )

    return AskResponse(
        answer=answer,
        sources=sources,
    )