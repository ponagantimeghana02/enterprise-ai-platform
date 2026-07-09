import os
import time
from datetime import datetime

import psutil
import requests

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

BASE_URL = "http://127.0.0.1:8000"

LOGIN_URL = "/auth/login"

LOGIN_PAYLOAD = {
    "email": "admin@example.com",
    "password": "admin123"
}

API_ENDPOINTS = {
    "Authentication API": {
        "url": "/auth/login",
        "method": "POST",
        "payload": LOGIN_PAYLOAD
    },

    "Chat API": {
        "url": "/chat",
        "method": "POST",
        "payload": {
            "message": "Hello",
            "session_id": "test-session",
            "department": "HR",
            "stream": False
        }
    },

    "Knowledge Search API": {
        "url": "/documents/search",
        "method": "POST",
        "payload": {
            "query": "leave policy",
            "department": "HR",
            "limit": 5
        }
    },

    "Health API": {
        "url": "/health",
        "method": "GET"
    }
}

REPORT_PATH = "docs/api_performance_report.md"

process = psutil.Process()


# -------------------------------------------------------
# Login
# -------------------------------------------------------

print("Logging in...")

token = None

try:

    response = requests.post(
        BASE_URL + LOGIN_URL,
        json=LOGIN_PAYLOAD,
        timeout=10
    )

    print("Login Status:", response.status_code)

    if response.status_code == 200:

        token = response.json().get("access_token")

        print("Login Successful")

    else:

        print(response.text)

except Exception as e:

    print("Login Failed")
    print(e)

headers = {}

if token:
    headers["Authorization"] = f"Bearer {token}"


# -------------------------------------------------------
# Profiling
# -------------------------------------------------------

results = []

for api_name, api in API_ENDPOINTS.items():

    url = BASE_URL + api["url"]

    print(f"\nTesting {url}")

    memory_before = process.memory_info().rss / (1024 * 1024)
    cpu_before = psutil.cpu_percent(interval=None)

    start = time.perf_counter()

    try:

        if api["method"] == "POST":

            response = requests.post(
                url,
                json=api.get("payload", {}),
                headers=headers if api_name != "Authentication API" else {},
                timeout=20
            )

        else:

            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

        status = response.status_code

    except Exception as e:

        print(e)

        status = "Failed"

        response = None

    end = time.perf_counter()

    cpu_after = psutil.cpu_percent(interval=None)
    memory_after = process.memory_info().rss / (1024 * 1024)

    token_usage = "N/A"

    if response:

        try:

            data = response.json()

            if "usage" in data:
                token_usage = data["usage"].get("total_tokens", "N/A")

        except:
            pass

    results.append({

        "API": api_name,
        "Status": status,
        "Response": round((end - start) * 1000, 2),
        "CPU Before": cpu_before,
        "CPU After": cpu_after,
        "Memory Before": round(memory_before, 2),
        "Memory After": round(memory_after, 2),
        "DB Queries": "N/A",
        "Token Usage": token_usage

    })


# -------------------------------------------------------
# Markdown Report
# -------------------------------------------------------

os.makedirs("docs", exist_ok=True)

with open(REPORT_PATH, "w", encoding="utf-8") as f:

    f.write("# API Performance Report\n\n")

    f.write(f"Generated: {datetime.now()}\n\n")

    f.write("| API | Status | Response Time (ms) | CPU Before | CPU After | Memory Before (MB) | Memory After (MB) | DB Queries | Token Usage |\n")

    f.write("|-----|--------|-------------------:|-----------:|----------:|-------------------:|------------------:|-----------:|------------:|\n")

    for r in results:

        f.write(
            f"| {r['API']} | "
            f"{r['Status']} | "
            f"{r['Response']} | "
            f"{r['CPU Before']} | "
            f"{r['CPU After']} | "
            f"{r['Memory Before']} | "
            f"{r['Memory After']} | "
            f"{r['DB Queries']} | "
            f"{r['Token Usage']} |\n"
        )

print("\nReport generated successfully.")
print(REPORT_PATH)