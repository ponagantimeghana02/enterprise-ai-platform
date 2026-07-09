class ContextBuilder:
    @staticmethod
    def build_context(documents: list[dict], max_tokens: int = 2000) -> dict:
        seen_texts = set()
        merged_chunks = []
        sources = []
        current_token_estimate = 0
        
        for doc in documents:
            text = doc["text"]
            if text in seen_texts:
                continue
            seen_texts.add(text)
            
            est_tokens = int(len(text.split()) * 1.3)
            if current_token_estimate + est_tokens > max_tokens:
                break
                
            merged_chunks.append(text)
            current_token_estimate += est_tokens
            
            meta = doc.get("metadata", {})
            sources.append({
                "doc_id": meta.get("doc_id"),
                "file_name": meta.get("file_name"),
                "page_number": meta.get("page_number")
            })

        return {
            "context": merged_chunks,
            "sources": sources,
            "token_count": current_token_estimate
        }
context_builder = ContextBuilder()
