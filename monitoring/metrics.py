from fastapi import APIRouter, Request
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from starlette.responses import Response
import time

router = APIRouter(prefix="/metrics", tags=["Monitoring"])



REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP Errors"
)

RESPONSE_TIME = Histogram(
    "http_response_time_seconds",
    "HTTP Response Time"
)

ACTIVE_USERS = Gauge(
    "active_users",
    "Current Active Users"
)



TOKEN_USAGE = Counter(
    "ai_token_usage_total",
    "Total AI Tokens Used"
)

RAG_RETRIEVAL_TIME = Histogram(
    "rag_retrieval_time_seconds",
    "RAG Retrieval Time"
)

AGENT_EXECUTION_TIME = Histogram(
    "agent_execution_time_seconds",
    "Agent Execution Time"
)

TOOL_CALLS = Counter(
    "tool_calls_total",
    "Total Tool Calls",
    ["tool"]
)


def track_request(method: str, endpoint: str):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()


def track_error():
    ERROR_COUNT.inc()


def track_response_time(seconds: float):
    RESPONSE_TIME.observe(seconds)


def set_active_users(count: int):
    ACTIVE_USERS.set(count)


def track_token_usage(tokens: int):
    TOKEN_USAGE.inc(tokens)


def track_rag_time(seconds: float):
    RAG_RETRIEVAL_TIME.observe(seconds)


def track_agent_time(seconds: float):
    AGENT_EXECUTION_TIME.observe(seconds)


def track_tool_call(tool_name: str):
    TOOL_CALLS.labels(tool=tool_name).inc()



async def metrics_middleware(request: Request, call_next):
    start = time.time()

    track_request(request.method, request.url.path)

    response = await call_next(request)

    duration = time.time() - start

    track_response_time(duration)

    if response.status_code >= 400:
        track_error()

    return response

@router.get("")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )