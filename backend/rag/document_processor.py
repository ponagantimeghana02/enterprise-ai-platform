class DocumentProcessor:
    @staticmethod
    def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
        words = text.split()
        if not words:
            return []
        chunks = []
        step = chunk_size - chunk_overlap
        if step <= 0:
            step = chunk_size
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
        return chunks
