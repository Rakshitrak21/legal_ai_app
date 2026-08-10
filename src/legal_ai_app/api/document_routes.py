from fastapi import APIRouter, UploadFile, File
import os
import tempfile

from legal_ai_app.services.pdf_loader import PDFLoader
from legal_ai_app.services.document_analyzer import DocumentAnalyzer
from legal_ai_app.services.document_risk_analyzer import DocumentRiskAnalyzer
from legal_ai_app.services.document_law_comparator import DocumentLawComparator
from legal_ai_app.services.document_citation_service import DocumentCitationService


router = APIRouter(
    prefix="/documents",
    tags=["Document Intelligence"],
)

pdf_loader = PDFLoader()
document_analyzer = DocumentAnalyzer()
risk_analyzer = DocumentRiskAnalyzer()
law_comparator = DocumentLawComparator()
citation_service = DocumentCitationService()


@router.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...)
):

    file_bytes = await file.read()

    temp_path = os.path.join(
        tempfile.gettempdir(),
        file.filename
    )

    with open(temp_path, "wb") as buffer:
        buffer.write(file_bytes)

    # Load complete document text.
    text = pdf_loader.load_pdf(
        temp_path
    )

    # Load pages separately for page-level citations.
    pages = pdf_loader.load_pages(
        temp_path
    )

    # Analyze document.
    analysis = document_analyzer.analyze(
        text
    )

    # Analyze potential risks.
    risk_analysis = risk_analyzer.analyze(
        document_text=text,
        document_analysis=analysis,
    )

    # Collect evidence from analysis.
    evidence = []

    for clause in analysis.get(
        "important_clauses",
        []
    ):
        evidence.append(clause)

    for risk in analysis.get(
        "potential_risks",
        []
    ):
        evidence.append(risk)

    # Compare document with legal knowledge.
    comparison = law_comparator.compare(
        document_text=text,
        document_analysis=analysis,
    )

    # Build page-level citations.
    document_citations = (
        citation_service.build_document_citations(
            pages=pages,
            evidence=evidence,
        )
    )

    return {
        "filename": file.filename,
        "characters": len(text),
        "pages": len(pages),
        "analysis": analysis,
        "risk_analysis": risk_analysis,
        "legal_comparison": comparison["comparison"],
        "document_citations": document_citations,
    }