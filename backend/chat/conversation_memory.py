import time

class ConversationMemory:
    def __init__(self):
        self.sessions = {}
        self.redis_client = None
        self.init_redis()

    def init_redis(self):
        try:
            import redis
            from backend.settings.config import settings
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True
            )
        except Exception:
            self.redis_client = None

    def add_message(self, session_id: str, role: str, content: str):
        timestamp = time.time()
        if self.redis_client:
            try:
                self.redis_client.rpush(f"session:{session_id}:history", f"{role}:{content}")
                self.redis_client.hset(f"session:{session_id}:meta", "last_updated", str(timestamp))
                self.redis_client.expire(f"session:{session_id}:history", 3600)
                self.redis_client.expire(f"session:{session_id}:meta", 3600)
                return
            except Exception:
                pass
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "history": [],
                "meta": {"last_updated": timestamp}
            }
        self.sessions[session_id]["history"].append({"role": role, "content": content, "timestamp": timestamp})
        self.sessions[session_id]["meta"]["last_updated"] = timestamp

    def get_history(self, session_id: str) -> list[dict]:
        if self.redis_client:
            try:
                items = self.redis_client.lrange(f"session:{session_id}:history", 0, -1)
                history = []
                for item in items:
                    role, content = item.split(":", 1)
                    history.append({"role": role, "content": content})
                return history
            except Exception:
                pass
        
        if session_id in self.sessions:
            return [{"role": m["role"], "content": m["content"]} for m in self.sessions[session_id]["history"]]
        return []

    def clear(self, session_id: str):
        if self.redis_client:
            try:
                self.redis_client.delete(f"session:{session_id}:history")
                self.redis_client.delete(f"session:{session_id}:meta")
                return
            except Exception:
                pass
        if session_id in self.sessions:
            del self.sessions[session_id]

conversation_memory = ConversationMemory()
