class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.model = None
        self.init_model()

    def init_model(self):
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(self.model_name)
        except Exception:
            self.model = None

    def rerank(self, query: str, documents: list[dict], top_k: int = 5) -> list[dict]:
        if not documents:
            return []
        
        if self.model:
            try:
                pairs = [[query, doc["text"]] for doc in documents]
                scores = self.model.predict(pairs).tolist()
                for i, score in enumerate(scores):
                    documents[i]["rerank_score"] = float(score)
                return sorted(documents, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
            except Exception:
                pass

        for doc in documents:
            doc["rerank_score"] = doc["score"]
        return sorted(documents, key=lambda x: x["rerank_score"], reverse=True)[:top_k]

reranker = Reranker()
