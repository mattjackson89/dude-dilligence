"""Minimal example demonstrating OpenTelemetry tracing with agent-based systems.

This example shows how to use the tracing utility from dude_diligence
to trace a simple agent-based task with OpenTelemetry.
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dude_diligence.utils.tracing import initialize_tracing
from opentelemetry import trace
from smolagents import ToolCallingAgent, OpenAIServerModel, DuckDuckGoSearchTool, CodeAgent

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_simple_agent_with_tracing():
    """Run a simple agent with OpenTelemetry tracing enabled."""
    print("\n=== Running Simple Agent with OpenTelemetry Tracing ===\n")
    
    # Force initialize tracing for this example (important for standalone examples)
    _ = initialize_tracing(force=True)
    tracer = trace.get_tracer("simple_agent_example")
    
    # Initialize model - check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set, example may run slower")
        print("Warning: OPENAI_API_KEY environment variable not set")
        print("The example will still run, but may be slower\n")
    
    model = OpenAIServerModel(model_id="gpt-4o-mini")
    
    # Create a search agent using DuckDuckGo
    search_agent = ToolCallingAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        name="search_agent",
        description="This agent can search the web using DuckDuckGo."
    )

    summarizer_agent = ToolCallingAgent(
        tools=[],
        model=model,
        name="summarizer_agent",
        description="This agent can summarize text."
    )

    # Query to be used
    query = "First, search the web for 'OpenTelemetry context propagation'. Then, summarize the findings in one sentence."
    
    # Create the main manager agent with tracing
    with tracer.start_as_current_span("Example-Tracing-Task") as span:
        # Add custom attributes for better tracing
        span.set_attribute("example.user.id", "example-user")
        span.set_attribute("example.session.id", "example-session")
        span.set_attribute("example.tags", ["tutorial", "agent", "duckduckgo"])
        
        # Set the input value for the top-level trace
        span.set_attribute("input.value", query)
            
        # Create the main manager agent that orchestrates the other agents
        manager_agent = CodeAgent(
            tools=[],
            model=model,
            managed_agents=[search_agent, summarizer_agent],
            name="manager_agent",
            description="This agent manages the search and summarizer agents to complete tasks."
        )
        
        # Run the agent on a simple task
        print(f"Asking agent: {query}")
        result = manager_agent.run(query)
        
        # Record the output in the trace
        span.set_attribute("output.value", result)
        
    print("\n=== Agent Response ===\n")
    print(result)
    print("\n=== Agent task complete ===")
    print("Check your OpenTelemetry collector to see the trace!")


if __name__ == "__main__":
    print("OpenTelemetry Tracing Example")
    print("-----------------------------\n")
    run_simple_agent_with_tracing()
