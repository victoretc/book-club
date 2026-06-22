"""
Observability configuration for Pyroscope and Tempo
"""

import logging
import os


logger = logging.getLogger(__name__)


# Pyroscope continuous profiling
PYROSCOPE_ENABLED = os.getenv("PYROSCOPE_ENABLED", "false").lower() == "true"
PYROSCOPE_SERVER_ADDRESS = os.getenv("PYROSCOPE_SERVER_ADDRESS", "http://pyroscope.monitoring.svc.cluster.local:4040")
PYROSCOPE_APPLICATION_NAME = os.getenv("PYROSCOPE_APPLICATION_NAME", "book-club-backend")

logger.info("Pyroscope enabled: %s", PYROSCOPE_ENABLED)

if PYROSCOPE_ENABLED:
    try:
        import pyroscope  # type: ignore[import-untyped]

        pyroscope.configure(
            application_name=PYROSCOPE_APPLICATION_NAME,
            server_address=PYROSCOPE_SERVER_ADDRESS,
            tags={
                "environment": os.getenv("ENVIRONMENT", "production"),
                "version": os.getenv("APP_VERSION", "unknown"),
            },
        )
        logger.info("Pyroscope configured: %s", PYROSCOPE_SERVER_ADDRESS)
    except ImportError as e:
        logger.warning("Pyroscope not available: %s", e)


# tracing
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
OTEL_ENABLED = bool(OTEL_ENDPOINT)

logger.info("OpenTelemetry enabled: %s, endpoint: %s", OTEL_ENABLED, OTEL_ENDPOINT)

if OTEL_ENABLED:
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.django import DjangoInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        # resource with service information
        resource = Resource.create(
            {
                "service.name": os.getenv("OTEL_SERVICE_NAME", "book-club-backend"),
                "service.version": os.getenv("APP_VERSION", "unknown"),
                "deployment.environment": os.getenv("ENVIRONMENT", "production"),
            }
        )

        # tracer provider
        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)

        # OTLP exporter
        otlp_exporter = OTLPSpanExporter(
            endpoint=OTEL_ENDPOINT,
            insecure=True,  # Use TLS in production
        )

        # span processor
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        # Instrument Django
        DjangoInstrumentor().instrument()

        # Try to instrument psycopg (v3) - this project uses psycopg, not psycopg2
        try:
            from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor

            PsycopgInstrumentor().instrument()
            logger.info("Psycopg instrumentation enabled")
        except ImportError:
            # Psycopg instrumentation not available, continue without it
            logger.info("Psycopg instrumentation not available (install opentelemetry-instrumentation-psycopg)")

        logger.info("OpenTelemetry configured successfully")

    except ImportError as e:
        logger.warning("OpenTelemetry not available: %s", e)
