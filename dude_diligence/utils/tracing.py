"""Tracing utility for integrating Langfuse with Dude Diligence.

Provides initialization and helper functions for tracing agent activities.
"""

import os
import base64
import logging
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry import trace

logger = logging.getLogger(__name__)

# Singleton pattern for the tracer provider
_tracer_provider = None
_tracing_initialized = False

def initialize_tracing(force=False) -> TracerProvider:
    """Initialize OpenTelemetry tracing for Langfuse.
    
    Args:
        force: If True, reinitialize tracing even if it was already initialized.
              Useful for examples and tests that need fresh tracing.
    
    Returns:
        TracerProvider: The configured tracer provider
    """
    global _tracer_provider, _tracing_initialized
    
    # Return existing provider if already initialized and not forced
    if _tracing_initialized and not force:
        logger.debug("Tracing already initialized, returning existing tracer provider")
        return _tracer_provider
    
    # Check for required environment variables
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

    if not all([public_key, secret_key, endpoint]):
        logger.warning("Missing required environment variables for Langfuse tracing.")
        logger.warning("Ensure LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and OTEL_EXPORTER_OTLP_ENDPOINT are set IN THE CONTAINER'S ENVIRONMENT.")
        logger.warning("SmolagentsInstrumentor will NOT be initialized.")
        _tracer_provider = TracerProvider()
        _tracing_initialized = True
        return _tracer_provider
    
    # Construct the authorization header if not already set
    if not os.getenv("OTEL_EXPORTER_OTLP_HEADERS"):
        auth = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth}"
        logger.warning("OTEL_EXPORTER_OTLP_HEADERS constructed from LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")

    # Create a tracer provider with context propagation
    _tracer_provider = TracerProvider()
    
    # Use BatchSpanProcessor for better performance in production
    _tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    # _tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    SmolagentsInstrumentor().instrument(tracer_provider=_tracer_provider)

    # Set the trace provider as the global provider
    trace.set_tracer_provider(_tracer_provider)
    logger.info(f"Langfuse tracing initialized with endpoint: {endpoint}")
    logger.info("Model calls will now be automatically captured by SmolagentsInstrumentor")
    
    _tracing_initialized = True
    return _tracer_provider
