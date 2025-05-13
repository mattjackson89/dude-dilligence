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


def initialize_tracing() -> TracerProvider:
    """Initialize OpenTelemetry tracing for Langfuse.
    
    Sets up the environment variables required for OTLP export if they're not already set,
    using the LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables.
    
    Returns:
        TracerProvider: The configured tracer provider
    """
    # Check for required environment variables
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    
    if not all([public_key, secret_key, endpoint]):
        logger.warning("Missing required environment variables for Langfuse tracing.")
        logger.warning("Ensure LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and OTEL_EXPORTER_OTLP_ENDPOINT are set.")
        return TracerProvider()
    
    # Construct the authorization header if not already set
    if not os.getenv("OTEL_EXPORTER_OTLP_HEADERS"):
        auth = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth}"
        logger.info("OTEL_EXPORTER_OTLP_HEADERS constructed from LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")

    # Create a tracer provider
    trace_provider = TracerProvider()
    
    # Create an OTLP exporter
    otlp_exporter = OTLPSpanExporter()
    

    trace_provider.add_span_processor(SimpleSpanProcessor(otlp_exporter)) # BatchSpanProcessor maybe?
    
    # Set the trace provider as the global provider
    trace.set_tracer_provider(trace_provider)
    
    # Instrument smolagents with the tracer provider
    # This is the crucial part that will automatically capture model calls
    SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)
    
    logger.info(f"Langfuse tracing initialized with endpoint: {endpoint}")
    logger.info("Model calls will now be automatically captured by SmolagentsInstrumentor")
    
    return trace_provider
