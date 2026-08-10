import json

from openai import OpenAI

from legal_ai_app.core.config import settings


class LegalIssueAnalyzer:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def analyze(self, question: str):

        prompt = f"""
You are an Indian legal issue analysis assistant.

Analyze the user's situation.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "main_issue": "",
    "category": "",
    "intent": "",
    "facts": [],
    "important_facts": [],
    "missing_facts": [],
    "legal_areas": [],
    "retrieval_queries": [],
    "evidence_to_collect": []
}}

Rules:

- Identify the user's actual legal problem.
- Extract facts explicitly stated by the user.
- Do not invent facts.
- Identify important missing information.
- Identify broad legal areas that should be researched.
- Create 2 to 4 search queries that should be used
  to retrieve relevant Indian legal documents.
- Do not invent specific Articles, Sections,
  judgments or citations.
- Do not provide legal advice yet.
- This step is only for analyzing the situation
  and preparing legal research.

User situation:

{question}
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