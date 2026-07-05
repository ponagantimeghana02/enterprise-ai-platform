from rank_bm25 import BM25Okapi
from backend.rag.vector_store import vector_store
from backend.rag.embedding_service import EmbeddingService
from backend.database import db

class HybridSearchEngine:
    def __init__(self):
        self.emb_service = EmbeddingService()

    def search(
        self,
        query: str,
        department: str,
        top_k: int = 5,
        semantic_weight: float = 0.65,
        keyword_weight: float = 0.35,
        metadata_filter: dict = None
    ) -> list[dict]:
        emb, _ = self.emb_service.get_embedding(query)
        semantic_results = vector_store.search(
            department=department,
            query_embedding=emb,
            top_k=30,
            metadata_filter=metadata_filter
        )
        
        chunk_rows = db.execute(
            "SELECT c.id, c.chunk_text, c.embedding_id, c.page_number, d.file_name, d.id FROM document_chunks c JOIN documents d ON c.document_id = d.id WHERE d.department = %s AND d.status = 'Approved'",
            (department,),
            fetch=True
        )
        if not chunk_rows:
            return semantic_results[:top_k]

        corpus = [r[1] for r in chunk_rows]
        tokenized_corpus = [doc.lower().split() for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)
        
        tokenized_query = query.lower().split()
        bm25_scores = bm25.get_scores(tokenized_query)
        
        max_bm25 = max(bm25_scores) if len(bm25_scores) > 0 else 0.0
        
        keyword_results = []
        for i, row in enumerate(chunk_rows):
            raw_score = bm25_scores[i]
            norm_score = raw_score / max_bm25 if max_bm25 > 0 else 0.0
            keyword_results.append({
                "id": f"chunk_{row[0]}",
                "text": row[1],
                "metadata": {
                    "doc_id": row[5],
                    "file_name": row[4],
                    "page_number": row[3]
                },
                "score": norm_score
            })
            
        semantic_map = {r["text"]: r for r in semantic_results}
        keyword_map = {r["text"]: r for r in keyword_results}
        
        all_texts = set(semantic_map.keys()).union(set(keyword_map.keys()))
        combined = []
        for text in all_texts:
            s_res = semantic_map.get(text)
            k_res = keyword_map.get(text)
            
            s_score = s_res["score"] if s_res else 0.0
            k_score = k_res["score"] if k_res else 0.0
            
            final_score = (semantic_weight * s_score) + (keyword_weight * k_score)
            
            meta = s_res["metadata"] if s_res else k_res["metadata"]
            cid = s_res["id"] if s_res else k_res["id"]
            
            combined.append({
                "id": cid,
                "text": text,
                "metadata": meta,
                "score": final_score
            })
            
        return sorted(combined, key=lambda x: x["score"], reverse=True)[:top_k]

hybrid_search_engine = HybridSearchEngine()
