class ContextBuilder:

    def build(self, documents):

        contexts = []
        seen = set()

        for document in documents:

            text = document.page_content.strip()

            if text in seen:
                continue

            seen.add(text)

            metadata = document.metadata

            source = metadata.get(
                "retrieval_source",
                "unknown"
            )

            page = metadata.get("page")

            context = f"""
SOURCE: {source}
PAGE: {page}

{text}
"""

            contexts.append(context)

        return "\n\n---\n\n".join(contexts)