import os
import json
import uuid

class VectorStore:
    def __init__(self):
        self.client = None
        self.mock_store = {}
        self.init_chroma()

    def init_chroma(self):
        try:
            import chromadb
            from backend.settings.config import settings
            os.makedirs(settings.chroma_db_path, exist_ok=True)
            self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        except Exception:
            self.client = None

    def get_collection(self, department: str):
        col_name = department.lower().strip()
        if self.client:
            try:
                return self.client.get_or_create_collection(col_name)
            except Exception:
                pass
        if col_name not in self.mock_store:
            self.mock_store[col_name] = []
        return self.mock_store[col_name]

    def insert(self, department: str, text: str, embedding: list[float], metadata: dict, doc_id: str) -> str:
        col = self.get_collection(department)
        chunk_id = f"chunk_{uuid.uuid4().hex}"
        if self.client:
            try:
                col.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    metadatas=[metadata],
                    documents=[text]
                )
                return chunk_id
            except Exception:
                pass
        
        col.append({
            "id": chunk_id,
            "embedding": embedding,
            "metadata": metadata,
            "document": text,
            "doc_id": doc_id
        })
        return chunk_id

    def delete(self, department: str, doc_id: str):
        col = self.get_collection(department)
        if self.client:
            try:
                col.delete(where={"doc_id": str(doc_id)})
                return
            except Exception:
                pass
        
        cleaned = [item for item in col if str(item.get("metadata", {}).get("doc_id")) != str(doc_id)]
        self.mock_store[department.lower().strip()] = cleaned

    def search(self, department: str, query_embedding: list[float], top_k: int = 5, metadata_filter: dict = None) -> list[dict]:
        col = self.get_collection(department)
        if self.client:
            try:
                where_filter = metadata_filter or {}
                results = col.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=where_filter if where_filter else None
                )
                hits = []
                if results and "documents" in results and results["documents"]:
                    docs = results["documents"][0]
                    ids = results["ids"][0]
                    metas = results["metadatas"][0]
                    distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)
                    for i in range(len(docs)):
                        score = 1.0 - distances[i] if distances[i] <= 1.0 else 0.0
                        hits.append({
                            "id": ids[i],
                            "text": docs[i],
                            "metadata": metas[i],
                            "score": score
                        })
                return hits
            except Exception:
                pass

        hits = []
        for item in col:
            match = True
            if metadata_filter:
                for k, v in metadata_filter.items():
                    if item["metadata"].get(k) != v:
                        match = False
                        break
            if match:
                score = 0.85
                hits.append({
                    "id": item["id"],
                    "text": item["document"],
                    "metadata": item["metadata"],
                    "score": score
                })
        return sorted(hits, key=lambda x: x["score"], reverse=True)[:top_k]

vector_store = VectorStore()
