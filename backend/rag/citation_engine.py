class CitationEngine:
    @staticmethod
    def format_citations(sources: list[dict], scores: list[float] = None) -> str:
        if not sources:
            return "No citations available."
            
        citation_lines = ["According to:"]
        for idx, source in enumerate(sources):
            file_name = source.get("file_name", "Unknown Document")
            page = source.get("page_number", "N/A")
            sec = source.get("section", "General")
            score = scores[idx] if scores and idx < len(scores) else 0.85
            
            citation_lines.append(
                f"- {file_name} | Section: {sec} | Page: {page} (Similarity: {score:.2f})"
            )
        return "\n".join(citation_lines)
