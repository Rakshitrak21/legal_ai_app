class DocumentCitationService:

    def build_document_citations(
        self,
        pages: list[dict],
        evidence: list[str],
    ):

        citations = []

        for item in evidence:

            text = item.lower()

            for page in pages:

                page_text = page["text"].lower()

                if text and text in page_text:

                    citations.append({
                        "page": page["page"],
                        "evidence": item,
                    })

                    break

        return citations