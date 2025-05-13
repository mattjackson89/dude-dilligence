"""Minimal example demonstrating Langfuse tracing with smolagents.

This example shows how to use the tracing utility from dude_diligence
to trace a simple smolagents-based task with Langfuse.
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dude_diligence.utils.tracing import initialize_tracing
from opentelemetry import trace
from smolagents import CodeAgent, ToolCallingAgent, OpenAIServerModel, DuckDuckGoSearchTool

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



def run_simple_agent_with_tracing():
    """Run a simple agent with Langfuse tracing enabled."""
    print("\n=== Running Simple Agent with Langfuse Tracing ===\n")
    
    # Initialize tracing
    _ = initialize_tracing()
    tracer = trace.get_tracer("simple_agent_example")
    model = OpenAIServerModel(model_id="gpt-4o-mini")
    
    # Create a search agent using DuckDuckGo
    search_agent = ToolCallingAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        name="search_agent",
        description="This agent can search the web using DuckDuckGo."
    )
    
    # Query to be used
    query = "What is the Langfuse Python SDK and how can I use it to trace a function call? Use webserarch to find information and then show me a simple example."
    
    # Create and run the agent with tracing
    with tracer.start_as_current_span("Example-Tracing-Task") as span:
        # Add custom attributes for better tracing
        span.set_attribute("langfuse.user.id", "example-user")
        span.set_attribute("langfuse.session.id", "example-session")
        span.set_attribute("langfuse.tags", ["tutorial", "code-agent", "duckduckgo"])
        
        # Set the input value for the top-level trace
        span.set_attribute("input.value", query)  # This adds the input to the top-level trace
        
        # Create the main Code Agent that manages the search agent
        manager_agent = CodeAgent(
            tools=[],
            model=model,
            managed_agents=[search_agent],
            name="manager_agent",
            description="This agent manages the search agent and can write code based on search results."
        )
        
        # Run the agent on a simple task
        print(f"Asking agent: {query}")
        result = manager_agent.run(query)
        
        # span.set_attribute("gen_ai.completion", result)
        span.set_attribute("output.value", result)
        # span.set_attribute("output", result)
        # span.end()
        print("\n=== Agent Response ===\n")
        print(result)
        print("\n=== Agent task complete ===")
        print("Check your Langfuse dashboard to see the trace!")


if __name__ == "__main__":
    print("Langfuse Tracing Example")
    print("------------------------\n")
    run_simple_agent_with_tracing()
