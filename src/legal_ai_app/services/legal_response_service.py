import json

from openai import OpenAI

from legal_ai_app.core.config import settings
from legal_ai_app.prompts.legal_response_prompt import (
    LEGAL_RESPONSE_PROMPT,
)


class LegalResponseService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate(
        self,
        question: str,
        classification,
        context: str,
        history: list,
    ):

        prompt = LEGAL_RESPONSE_PROMPT.format(
            question=question,
            classification=classification,
            context=context,
            history=history,
        )

        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content