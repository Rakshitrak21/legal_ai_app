import json

from openai import OpenAI

from legal_ai_app.core.config import settings
from legal_ai_app.models.schemas import QueryClassification
from legal_ai_app.prompts.classification_prompt import CLASSIFICATION_PROMPT


class QueryClassifier:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def classify(self, question: str):

        prompt = CLASSIFICATION_PROMPT.format(
            question=question
        )

        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_object"
            }
        )

        result = json.loads(
            response.choices[0].message.content
        )

        return QueryClassification(**result)