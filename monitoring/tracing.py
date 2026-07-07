from fastapi import Request
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
import time


resource = Resource.create(
    {
        "service.name": "enterprise-backend"
    }
)

provider = TracerProvider(resource=resource)

trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces"
)

provider.add_span_processor(
    BatchSpanProcessor(exporter)
)

tracer = trace.get_tracer(__name__)


async def tracing_middleware(request: Request, call_next):

    with tracer.start_as_current_span(
        f"{request.method} {request.url.path}"
    ) as span:

        start = time.time()

        span.set_attribute(
            "http.method",
            request.method
        )

        span.set_attribute(
            "http.route",
            request.url.path
        )

        try:

            response = await call_next(request)

            span.set_attribute(
                "http.status_code",
                response.status_code
            )

            span.set_attribute(
                "latency_ms",
                round((time.time() - start) * 1000, 2)
            )

            return response

        except Exception as e:

            span.record_exception(e)

            span.set_attribute(
                "error",
                True
            )

            raise


def trace_gateway():

    return tracer.start_as_current_span(
        "Gateway"
    )


def trace_rag():

    return tracer.start_as_current_span(
        "RAG"
    )



def trace_llm():

    return tracer.start_as_current_span(
        "LLM"
    )


def trace_agent():

    return tracer.start_as_current_span(
        "Agent"
    )


def trace_database():

    return tracer.start_as_current_span(
        "Database"
    )