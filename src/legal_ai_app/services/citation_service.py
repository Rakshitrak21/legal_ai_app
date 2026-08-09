class CitationService:

    def build_sources(self, documents):

        sources = []
        seen = set()

        for doc in documents:

            metadata = doc.metadata

            source = {
                "source": metadata.get("source"),
                "document_type": metadata.get("document_type"),
                "category": metadata.get("category"),
                "court": metadata.get("court"),
                "case_name": metadata.get("case_name"),
                "year": metadata.get("year"),
                "citation": metadata.get("citation"),
                "page": metadata.get("page"),
                "retrieval_source": metadata.get(
                    "retrieval_source"
                ),
            }

            key = (
                source["source"],
                source["page"],
                source["retrieval_source"],
            )

            if key not in seen:

                seen.add(key)

                sources.append(source)

        return sources