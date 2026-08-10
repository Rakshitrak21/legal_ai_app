import json

from openai import OpenAI

from legal_ai_app.core.config import settings

from legal_ai_app.agent.tools import (
    search_legal_knowledge,
    search_judgments,
    search_user_documents,
    analyze_user_document,
)

from legal_ai_app.services.evidence_service import EvidenceService


class LegalAgent:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        # Available agent tools.
        self.tools = {
            "search_legal_knowledge": search_legal_knowledge,
            "search_judgments": search_judgments,
            "search_user_documents": search_user_documents,
            "analyze_user_document": analyze_user_document,
        }

        # Builds structured evidence from tool results.
        self.evidence_service = EvidenceService()

        # Tool definitions given to the LLM.
        self.tool_schemas = [

            {
                "type": "function",
                "function": {
                    "name": "search_legal_knowledge",
                    "description": (
                        "Search the Indian legal knowledge base "
                        "for Acts, Constitution and other legal "
                        "materials."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": (
                                    "Legal search query."
                                ),
                            },
                            "k": {
                                "type": "integer",
                                "description": (
                                    "Number of results."
                                ),
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "search_judgments",
                    "description": (
                        "Search Indian Supreme Court and "
                        "High Court judgments."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": (
                                    "Judgment search query."
                                ),
                            },
                            "k": {
                                "type": "integer",
                                "description": (
                                    "Number of results."
                                ),
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "search_user_documents",
                    "description": (
                        "Search documents uploaded by the user."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": (
                                    "Query for user documents."
                                ),
                            },
                            "k": {
                                "type": "integer",
                                "description": (
                                    "Number of results."
                                ),
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "analyze_user_document",
                    "description": (
                        "Analyze the user's uploaded legal document "
                        "and extract facts, parties, dates, obligations, "
                        "potential risks and relevant evidence."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": (
                                    "Question or situation that the "
                                    "document should be analyzed against."
                                ),
                            },
                            "k": {
                                "type": "integer",
                                "description": (
                                    "Number of relevant document chunks."
                                ),
                                "default": 8,
                            },
                        },
                        "required": ["question"],
                    },
                },
            },
        ]

    def run(
        self,
        question: str,
        max_steps: int = 6,
    ):

        messages = [

            {
                "role": "system",
                "content": """
You are an Indian legal research agent.

Research the user's question using the available tools.

Workflow:

1. Understand the user's situation.
2. Decide what information is required.
3. Select the appropriate tool.
4. Examine the tool result.
5. Use another tool when necessary.
6. Stop when sufficient evidence has been collected.

Available tools:

- search_legal_knowledge
- search_judgments
- search_user_documents
- analyze_user_document

Rules:

- Never invent laws.
- Never invent Articles or Sections.
- Never invent judgments.
- Do not assume a judgment automatically applies.
- Distinguish user facts from legal information.
- Prefer primary legal sources when available.
- Use user documents when the question concerns them.
- Use analyze_user_document when the question depends
  on an uploaded document.
- Do not provide the final legal answer until sufficient
  research has been completed.
- This provides legal information and is not a substitute
  for a qualified lawyer.
""",
            },

            {
                "role": "user",
                "content": question,
            },
        ]

        observations = []

        # ReAct tool-use loop.
        for step in range(max_steps):

            response = self.client.chat.completions.create(
                model=settings.CHAT_MODEL,
                messages=messages,
                tools=self.tool_schemas,
                tool_choice="auto",
            )

            message = response.choices[0].message

            # Keep the assistant tool-call message.
            messages.append(message)

            # No tool call means the agent is finished.
            if not message.tool_calls:
                break

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print("\n" + "=" * 80)
                print("AGENT STEP:", step + 1)
                print("AGENT TOOL:", tool_name)
                print("ARGUMENTS:", arguments)

                tool = self.tools.get(
                    tool_name
                )

                # Unknown tool protection.
                if not tool:

                    result = json.dumps({
                        "error": (
                            f"Unknown tool: {tool_name}"
                        )
                    })

                    observations.append({
                        "tool": tool_name,
                        "query": arguments.get(
                            "query",
                            arguments.get("question")
                        ),
                        "documents": [],
                        "analysis": {
                            "error": (
                                f"Unknown tool: {tool_name}"
                            )
                        },
                    })

                else:

                    # Execute the selected tool.
                    tool_result = tool(
                        **arguments
                    )

                    # Search tools return Documents.
                    if isinstance(
                        tool_result,
                        list
                    ):

                        observations.append({
                            "tool": tool_name,
                            "query": arguments.get(
                                "query",
                                arguments.get("question")
                            ),
                            "documents": tool_result,
                        })

                        result = self._format_documents(
                            tool_result
                        )

                    # Document analysis returns a dictionary.
                    else:

                        observations.append({
                            "tool": tool_name,
                            "query": arguments.get(
                                "question",
                                arguments.get("query")
                            ),
                            "documents": [],
                            "analysis": tool_result,
                        })

                        result = json.dumps(
                            tool_result,
                            indent=2,
                            default=str,
                        )

                print("TOOL RESULT RECEIVED")

                # Send observation back to the LLM.
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        # Build structured evidence AFTER all tools finish.
        evidence = self.evidence_service.build(
            observations
        )

        print("\n" + "=" * 80)
        print("TOTAL OBSERVATIONS:", len(observations))
        print("TOTAL EVIDENCE:", len(evidence))

        return {
            "observations": observations,
            "evidence": evidence,
            "messages": messages,
        }

    def _format_documents(
        self,
        documents,
    ):

        if not documents:
            return "No relevant documents found."

        results = []

        for index, document in enumerate(
            documents
        ):

            metadata = document.metadata

            results.append(
                f"""
RESULT {index + 1}

Source:
{metadata.get("source")}

Document Type:
{metadata.get("document_type")}

Category:
{metadata.get("category")}

Court:
{metadata.get("court")}

Case:
{metadata.get("case_name")}

Year:
{metadata.get("year")}

Citation:
{metadata.get("citation")}

Page:
{metadata.get("page")}

Retrieval Source:
{metadata.get("retrieval_source")}

Content:
{document.page_content}
"""
            )

        return "\n".join(results)

    def generate_final_answer(
        self,
        question: str,
        evidence: list,
    ):

        # Convert structured evidence into LLM context.
        context = self.evidence_service.build_context(
            evidence
        )

        prompt = f"""
You are an Indian legal information assistant.

Answer the user's question using ONLY the research
evidence collected by the legal research agent.

USER QUESTION:

{question}

RESEARCH EVIDENCE:

{context}

Structure the answer as:

## Situation

## Legal Issue

## Applicable Law

## Relevant Articles / Sections

## Relevant Judgments

## Analysis

## What You Can Do

## What You Should Avoid

## Next Steps

## Evidence / Documents

## Limitations

## Sources

Rules:

- Do not invent laws.
- Do not invent Articles or Sections.
- Do not invent judgments.
- Do not claim that a judgment definitely applies unless
  supported by the evidence.
- Clearly distinguish facts from legal information.
- If evidence is insufficient, say so.
- Provide practical steps only when supported by evidence.
- Mention the source and page when evidence contains
  page information.
- This is general legal information, not legal representation.
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