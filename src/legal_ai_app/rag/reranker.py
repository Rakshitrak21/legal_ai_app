from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        question: str,
        documents,
        top_k: int = 5,
    ):

        if not documents:
            return []

        pairs = [
            [question, document.page_content]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        ranked_documents = sorted(
            zip(documents, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        results = []

        for document, score in ranked_documents[:top_k]:

            document.metadata["rerank_score"] = float(score)

            results.append(document)

        return results