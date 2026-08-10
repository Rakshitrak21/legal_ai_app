from legal_ai_app.services.citation_service import CitationService


class EvidenceService:

    def __init__(self):
        self.citation_service = CitationService()

    def build(self, observations: list):

        evidence = []
        seen = set()

        for observation in observations:

            documents = observation.get(
                "documents",
                []
            )

            for document in documents:

                content = document.page_content.strip()

                if content in seen:
                    continue

                seen.add(content)

                metadata = document.metadata

                evidence.append({
                    "text": content,
                    "source": metadata.get("source"),
                    "document_type": metadata.get(
                        "document_type"
                    ),
                    "category": metadata.get(
                        "category"
                    ),
                    "court": metadata.get(
                        "court"
                    ),
                    "case_name": metadata.get(
                        "case_name"
                    ),
                    "year": metadata.get(
                        "year"
                    ),
                    "citation": metadata.get(
                        "citation"
                    ),
                    "page": metadata.get(
                        "page"
                    ),
                    "chunk_id": metadata.get(
                        "chunk_id"
                    ),
                    "retrieval_source": metadata.get(
                        "retrieval_source"
                    ),
                })

        return evidence

    def build_context(
        self,
        evidence: list,
    ):

        context = []

        for index, item in enumerate(
            evidence
        ):

            context.append(
                f"""
[EVIDENCE {index + 1}]

Source: {item["source"]}
Document Type: {item["document_type"]}
Category: {item["category"]}
Court: {item["court"]}
Case: {item["case_name"]}
Year: {item["year"]}
Citation: {item["citation"]}
Page: {item["page"]}
Chunk: {item["chunk_id"]}
Retrieval Source: {item["retrieval_source"]}

Text:
{item["text"]}
"""
            )

        return "\n".join(context)