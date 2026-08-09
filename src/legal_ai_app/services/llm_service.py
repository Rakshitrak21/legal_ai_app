from openai import OpenAI

from legal_ai_app.core.config import settings


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def ask(self, context: str, question: str):

        prompt = f"""
You are a legal AI assistant for Indian law.

Your job is to help the user understand their legal situation.

Use the provided context carefully.

The context may contain:

1. USER DOCUMENTS
   Documents uploaded by the user such as notices,
   contracts, agreements, FIRs, orders, etc.

2. LEGAL KNOWLEDGE
   Indian Constitution, Acts, Supreme Court judgments,
   High Court judgments and other legal sources.

IMPORTANT RULES:

- Do not invent laws, sections, articles, or judgments.
- Do not make claims that are unsupported by the context.
- Clearly distinguish between facts from the user's document
  and information from legal sources.
- If the available information is insufficient, say so.
- Explain the answer in simple language.
- Mention relevant legal provisions when they are present.
- Suggest reasonable next steps.
- Mention important precautions where relevant.
- This is legal information, not a substitute for a qualified lawyer.

CONTEXT:

{context}

USER QUESTION:

{question}

Provide a clear and structured answer.
"""

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