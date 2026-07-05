import re

class HallucinationDetector:
    def detect(self, answer: str, context_chunks: list[str], similarity_score: float) -> dict:
        if not context_chunks:
            return {
                "hallucination": True,
                "confidence": 0,
                "supported_sources": 0,
                "reason": "No context provided"
            }
            
        if similarity_score < 0.5:
            return {
                "hallucination": True,
                "confidence": 30,
                "supported_sources": 0,
                "reason": "Retrieval similarity score is too low"
            }

        context_text = " ".join(context_chunks).lower()
        answer_text = answer.lower()
        
        numbers_in_answer = re.findall(r'\b\d+\b', answer_text)
        unsupported_numbers = []
        for num in numbers_in_answer:
            if num not in context_text:
                unsupported_numbers.append(num)
                
        confidence = 100
        if unsupported_numbers:
            confidence -= len(unsupported_numbers) * 15
            
        confidence = max(0, confidence)
        is_hallucinating = confidence < 70
        
        return {
            "hallucination": is_hallucinating,
            "confidence": confidence,
            "supported_sources": len(context_chunks)
        }

hallucination_detector = HallucinationDetector()
