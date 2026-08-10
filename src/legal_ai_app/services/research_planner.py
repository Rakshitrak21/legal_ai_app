import json

from openai import OpenAI

from legal_ai_app.core.config import settings


class ResearchPlanner:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def create_plan(
        self,
        question: str,
        classification: dict,
        issue_analysis: dict,
    ):

        prompt = f"""
You are the research planning component of an
Indian legal research agent.

Create a research plan for the user's legal problem.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "goal": "",
    "research_tasks": [
        {{
            "task_id": 1,
            "type": "",
            "query": "",
            "purpose": "",
            "priority": "high"
        }}
    ]
}}

Allowed task types:

- law_search
- constitution_search
- judgment_search
- user_document_search
- fact_check

Allowed priorities:

- high
- medium
- low

Rules:

- Do not answer the legal question.
- Only create a research plan.
- Do not invent laws, Articles, Sections or cases.
- Create only tasks that are useful for this specific problem.
- Prefer multiple focused searches over one broad search.
- If the user has uploaded a document, include a
  user_document_search task when appropriate.
- Include judgment_search when previous court decisions
  could help.
- Include law_search or constitution_search when legal
  provisions need to be identified.
- Do not create unnecessary tasks.

USER QUESTION:

{question}

QUERY CLASSIFICATION:

{json.dumps(classification, indent=2)}

SITUATION ANALYSIS:

{json.dumps(issue_analysis, indent=2)}
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