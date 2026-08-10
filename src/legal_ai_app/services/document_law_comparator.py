import json

from openai import OpenAI

from legal_ai_app.core.config import settings
from legal_ai_app.rag.legal_rag import LegalRAG


class DocumentLawComparator:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.legal_rag = LegalRAG()

    def compare(
        self,
        document_text: str,
        document_analysis: dict,
    ):

        # Use important clauses and legal issues
        # as queries against the legal knowledge base.

        queries = []

        queries.extend(
            document_analysis.get(
                "legal_issues",
                []
            )
        )

        queries.extend(
            document_analysis.get(
                "important_clauses",
                []
            )
        )

        # Fallback if analyzer did not find anything.
        if not queries:
            queries = [
                document_analysis.get(
                    "summary",
                    document_text[:2000]
                )
            ]

        legal_documents = []

        for query in queries[:10]:

            results = self.legal_rag.retrieve(
                query=query,
                k=5,
            )

            legal_documents.extend(
                results
            )

        # Remove duplicate legal chunks.

        unique_documents = []
        seen = set()

        for document in legal_documents:

            content = document.page_content.strip()

            if content not in seen:

                seen.add(content)

                unique_documents.append(
                    document
                )

        legal_context = "\n\n".join(
            document.page_content
            for document in unique_documents[:20]
        )

        prompt = f"""
You are an Indian legal document comparison assistant.

Compare the user's document against the provided
Indian legal knowledge base.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "comparisons": [
        {{
            "document_issue": "",
            "legal_position": "",
            "assessment": "",
            "reason": "",
            "document_evidence": "",
            "legal_evidence": ""
        }}
    ],
    "overall_assessment": "",
    "additional_information_needed": []
}}

Rules:

- Use ONLY the document and legal context provided.
- Do not invent laws, sections, articles or judgments.
- Do not assume that a retrieved legal document automatically
  applies to the user's exact situation.
- Clearly distinguish document facts from legal information.
- "document_evidence" must refer to information actually
  present in the user's document.
- "legal_evidence" must come from the supplied legal context.
- If there is insufficient legal information, say so.
- Do not give a definitive legal conclusion where the evidence
  is insufficient.
- This is legal information and document analysis, not a
  substitute for a lawyer.

DOCUMENT ANALYSIS:

{json.dumps(document_analysis, indent=2)}

USER DOCUMENT:

{document_text}

LEGAL KNOWLEDGE BASE:

{legal_context}
"""

        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format={
                "type": "json_object"
            },
        )

        result = json.loads(
            response.choices[0].message.content
        )

        return {
            "comparison": result,
            "legal_documents": unique_documents[:10],
        }