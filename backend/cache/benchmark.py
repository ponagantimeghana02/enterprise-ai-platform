import time

from cache_manager import CacheManager


def expensive_operation():

    time.sleep(2)

    return {
        "answer": "Generated from database"
    }


def without_cache():

    start = time.time()

    data = expensive_operation()

    end = time.time()

    print("Without Cache")
    print(data)
    print("Time:", round(end - start, 3), "seconds")


def with_cache():

    start = time.time()

    data = CacheManager.get_cache("benchmark")

    if not data:

        data = expensive_operation()

        CacheManager.set_cache(
            "benchmark",
            data,
            ttl=300
        )

    end = time.time()

    print("With Cache")
    print(data)
    print("Time:", round(end - start, 3), "seconds")


if __name__ == "__main__":

    print("\nFirst Call")
    with_cache()

    print("\nSecond Call")
    with_cache()

    print("\nWithout Cache")
    without_cache()