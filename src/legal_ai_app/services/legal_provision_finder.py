from openai import OpenAI
import json

from legal_ai_app.core.config import settings
from legal_ai_app.rag.legal_rag import LegalRAG


class LegalProvisionFinder:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.legal_rag = LegalRAG()

    def find(
        self,
        question: str,
        issue_analysis: dict,
        top_k: int = 8,
    ):

        queries = issue_analysis.get(
            "retrieval_queries",
            []
        )

        if not queries:
            queries = [question]

        documents = []

        for query in queries:

            # Search Acts.
            act_documents = self.legal_rag.retrieve(
                query=query,
                category=issue_analysis.get("category"),
                document_type="act",
                k=top_k,
            )

            # Search Constitution.
            constitution_documents = self.legal_rag.retrieve(
                query=query,
                category="constitutional_law",
                document_type="constitution",
                k=top_k,
            )

            documents.extend(act_documents)
            documents.extend(constitution_documents)

        # Remove duplicate chunks.
        unique_documents = []
        seen = set()

        for document in documents:

            content = document.page_content.strip()

            if content not in seen:

                seen.add(content)

                unique_documents.append(
                    document
                )

        if not unique_documents:
            return {
                "provisions": [],
                "message": "No relevant legal provisions found in the legal knowledge base."
            }

        context = "\n\n".join(
            document.page_content
            for document in unique_documents
        )

        prompt = f"""
You are an Indian legal research assistant.

Identify legal provisions ONLY from the provided
legal knowledge base context.

Do not invent Articles, Sections, Acts or legal provisions.

Return ONLY valid JSON using this structure:

{{
    "provisions": [
        {{
            "name": "",
            "type": "",
            "provision": "",
            "act": "",
            "reason": ""
        }}
    ]
}}

For each provision:

- name = Article or Section name if available
- type = "Article" or "Section"
- provision = exact provision identifier
- act = name of the Act or Constitution
- reason = why this provision may be relevant

If the context does not contain a provision,
do not guess it.

User question:

{question}

Situation analysis:

{json.dumps(issue_analysis, indent=2)}

Legal knowledge base:

{context}
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
            "provisions": result.get(
                "provisions",
                []
            ),
            "documents": unique_documents,
        }