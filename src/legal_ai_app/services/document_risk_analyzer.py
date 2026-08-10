import json

from openai import OpenAI

from legal_ai_app.core.config import settings


class DocumentRiskAnalyzer:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def analyze(
        self,
        document_text: str,
        document_analysis: dict,
    ):

        prompt = f"""
You are an Indian legal document risk analysis assistant.

Analyze the document for potential legal risks.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "overall_risk": "low",
    "risks": [
        {{
            "title": "",
            "severity": "low",
            "description": "",
            "evidence": "",
            "reason": "",
            "legal_area": ""
        }}
    ],
    "missing_information": [],
    "questions_to_ask": []
}}

Allowed severity values:

- low
- medium
- high

Rules:

- Use ONLY information present in the document.
- Do not invent facts.
- Do not claim that something is legally illegal unless the
  provided information supports that conclusion.
- Identify potential risks, not definitive legal conclusions.
- Quote or reference the relevant document language in "evidence".
- Explain why the item may be risky.
- Identify information that should be checked by a lawyer.
- If no obvious risk is found, return an empty risks list.
- Do not invent Articles, Sections, Acts or case citations.

DOCUMENT ANALYSIS:

{json.dumps(document_analysis, indent=2)}

DOCUMENT:

{document_text}
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