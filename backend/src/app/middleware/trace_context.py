"""
Middleware to add OpenTelemetry trace context to HTTP responses
"""

from collections.abc import Callable
from contextlib import suppress

from django.http import HttpRequest, HttpResponse


def trace_context_middleware(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    """
    Middleware that adds trace ID to response headers
    """

    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)

        with suppress(ImportError):
            from opentelemetry import trace

            span = trace.get_current_span()
            if span and span.get_span_context().is_valid:
                span_context = span.get_span_context()

                # Add trace ID in hex format (standard W3C format)
                trace_id = format(span_context.trace_id, "032x")
                span_id = format(span_context.span_id, "016x")
                trace_flags = "01" if span_context.trace_flags.sampled else "00"

                response["X-Trace-Id"] = trace_id
                response["X-Span-Id"] = span_id
                response["traceparent"] = f"00-{trace_id}-{span_id}-{trace_flags}"

        return response

    return middleware
