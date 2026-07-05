import time
import uuid

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.dimension = 384
        if "bge" in model_name.lower():
            self.dimension = 768
        self.init_model()

    def init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
        except Exception:
            self.model = None

    def get_embeddings(self, texts: list[str]) -> tuple[list[list[float]], float]:
        start_time = time.time()
        if self.model:
            try:
                embeddings = self.model.encode(texts).tolist()
                duration = time.time() - start_time
                return embeddings, duration
            except Exception:
                pass
        
        import random
        embeddings = [[random.uniform(-1, 1) for _ in range(self.dimension)] for _ in texts]
        duration = time.time() - start_time
        return embeddings, duration

    def get_embedding(self, text: str) -> tuple[list[float], float]:
        embs, duration = self.get_embeddings([text])
        return embs[0], duration
