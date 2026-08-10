import json

from openai import OpenAI

from legal_ai_app.core.config import settings


class DocumentAnalyzer:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def analyze(self, text: str):

        prompt = f"""
You are an Indian legal document analysis assistant.

Analyze the provided legal document.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "document_type": "",
    "title": "",
    "summary": "",
    "parties": [],
    "important_dates": [],
    "case_numbers": [],
    "legal_issues": [],
    "claims": [],
    "obligations": [],
    "important_clauses": [],
    "potential_risks": [],
    "missing_information": []
}}

Rules:

- Use ONLY information present in the document.
- Do not invent facts.
- Do not provide legal conclusions that are not supported
  by the document.
- If information is unavailable, use an empty list or empty string.
- Preserve names, dates and case numbers accurately.
- Identify potentially important legal clauses or statements.
- Identify possible risks, but clearly treat them as potential risks.
- This is document analysis, not final legal advice.

DOCUMENT:

{text}
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