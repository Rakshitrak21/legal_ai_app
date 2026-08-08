from openai import OpenAI

from legal_ai_app.core.config import settings


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def ask(self, context: str, question: str):

        prompt = f"""
            You are a legal document assistant.

            You must answer using ONLY the context below.

            If the answer exists anywhere in the context,
            answer it in your own words.

            If the answer truly does not exist,
            reply exactly:

            I could not find this information in the uploaded document.

            =====================
            Context
            =====================

            {context}
            
            =====================
            Question
            =====================
            
            {question}
            
            Answer:
            """

        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content