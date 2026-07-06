import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


# -----------------------------
# AUTH MOCK (replace with real auth later)
# -----------------------------
def authenticate(user):
    if not user or "email" not in user:
        raise Exception("Authentication failed")
    return True


def authorize(user, role="user"):
    if user.get("role") not in ["admin", role]:
        raise Exception("Unauthorized access")
    return True


# -----------------------------
# RETRY DECORATOR
# -----------------------------
def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0

            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Retry {attempts+1} failed: {e}")
                    time.sleep(delay)
                    attempts += 1

            raise Exception("Max retries exceeded")

        return wrapper
    return decorator


# -----------------------------
# BASE TOOL CLASS
# -----------------------------
class BaseTool:
    def validate(self, data: dict):
        if not isinstance(data, dict):
            raise Exception("Invalid input data")
        return True

    def log(self, message: str):
        logger.info(message)
        print(f"[LOG] {message}")