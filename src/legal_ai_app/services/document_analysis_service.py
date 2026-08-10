import json

from openai import OpenAI

from legal_ai_app.core.config import settings


class DocumentAnalysisService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def analyze(
        self,
        question: str,
        documents: list,
    ):

        if not documents:
            return {
                "analysis": "No user document was found.",
                "documents": [],
            }

        context = []

        for index, document in enumerate(documents):

            context.append(
                f"""
DOCUMENT {index + 1}

Source:
{document.metadata.get("source")}

Page:
{document.metadata.get("page")}

Content:
{document.page_content}
"""
            )

        prompt = f"""
You are an Indian legal document analysis assistant.

Analyze the user's uploaded document in relation to
the user's question.

USER QUESTION:

{question}

DOCUMENT:

{"".join(context)}

Return ONLY valid JSON:

{{
    "document_type": "",
    "key_facts": [],
    "legal_issues": [],
    "important_dates": [],
    "parties": [],
    "obligations": [],
    "potential_risks": [],
    "missing_information": [],
    "relevant_evidence": []
}}

Rules:

- Extract only information present in the document.
- Do not invent facts.
- Do not invent legal provisions.
- Do not assume missing information.
- If something is not present, use an empty list.
- Separate facts from legal conclusions.
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

        return json.loads(
            response.choices[0].message.content
        )