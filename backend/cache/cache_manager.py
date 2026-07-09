import json
import time
import redis

# Redis Connection
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


class CacheManager:

    # -------------------------
    # Save Data
    # -------------------------
    @staticmethod
    def set_cache(key, value, ttl=300):
        redis_client.setex(
            key,
            ttl,
            json.dumps(value)
        )

    # -------------------------
    # Get Data
    # -------------------------
    @staticmethod
    def get_cache(key):
        data = redis_client.get(key)

        if data:
            return json.loads(data)

        return None

    # -------------------------
    # Delete Cache
    # -------------------------
    @staticmethod
    def delete_cache(key):
        redis_client.delete(key)

    # -------------------------
    # Clear All Cache
    # -------------------------
    @staticmethod
    def clear_cache():
        redis_client.flushdb()

    # -------------------------
    # Authentication Sessions
    # -------------------------
    @staticmethod
    def cache_session(user_id, token):

        key = f"session:{user_id}"

        CacheManager.set_cache(
            key,
            {"token": token},
            ttl=3600
        )

    @staticmethod
    def get_session(user_id):

        return CacheManager.get_cache(
            f"session:{user_id}"
        )

    # -------------------------
    # User Profile
    # -------------------------
    @staticmethod
    def cache_user_profile(user_id, profile):

        CacheManager.set_cache(
            f"profile:{user_id}",
            profile,
            ttl=1800
        )

    @staticmethod
    def get_user_profile(user_id):

        return CacheManager.get_cache(
            f"profile:{user_id}"
        )

    # -------------------------
    # Chat History
    # -------------------------
    @staticmethod
    def cache_chat(chat_id, messages):

        CacheManager.set_cache(
            f"chat:{chat_id}",
            messages,
            ttl=3600
        )

    @staticmethod
    def get_chat(chat_id):

        return CacheManager.get_cache(
            f"chat:{chat_id}"
        )

    # -------------------------
    # Embeddings
    # -------------------------
    @staticmethod
    def cache_embedding(text, embedding):

        CacheManager.set_cache(
            f"embedding:{text}",
            embedding,
            ttl=86400
        )

    @staticmethod
    def get_embedding(text):

        return CacheManager.get_cache(
            f"embedding:{text}"
        )

    # -------------------------
    # RAG Search Results
    # -------------------------
    @staticmethod
    def cache_rag(query, result):

        CacheManager.set_cache(
            f"rag:{query}",
            result,
            ttl=1800
        )

    @staticmethod
    def get_rag(query):

        return CacheManager.get_cache(
            f"rag:{query}"
        )

    # -------------------------
    # Prompt Templates
    # -------------------------
    @staticmethod
    def cache_prompt(name, prompt):

        CacheManager.set_cache(
            f"prompt:{name}",
            prompt,
            ttl=86400
        )

    @staticmethod
    def get_prompt(name):

        return CacheManager.get_cache(
            f"prompt:{name}"
        )

    # -------------------------
    # Frequently Accessed Docs
    # -------------------------
    @staticmethod
    def cache_document(doc_id, document):

        CacheManager.set_cache(
            f"doc:{doc_id}",
            document,
            ttl=7200
        )

    @staticmethod
    def get_document(doc_id):

        return CacheManager.get_cache(
            f"doc:{doc_id}"
        )

    # -------------------------
    # Cache Invalidation
    # -------------------------
    @staticmethod
    def invalidate(prefix):

        keys = redis_client.keys(f"{prefix}:*")

        if keys:
            redis_client.delete(*keys)

    # -------------------------
    # Cache Warming
    # -------------------------
    @staticmethod
    def warm_cache():

        CacheManager.cache_prompt(
            "default",
            {
                "system":
                "You are an AI assistant."
            }
        )

        CacheManager.cache_document(
            "doc1",
            {
                "title": "AI Guide",
                "content": "Introduction to AI"
            }
        )

        print("Cache warmed successfully.")