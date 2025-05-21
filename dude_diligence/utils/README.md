# Dude Diligence Utilities

*"Hey there, Pretty Helpers! Let's make Johnny look good!"* - Johnny Bravo

This directory contains utility modules that support the core functionality of Dude Diligence.

## Available Utilities

### Model Configuration (`model.py`)

Functions for setting up and configuring the language models:

- `get_agent_model()`: Gets the appropriate model for agents
- Model selection based on environment variables
- Default fallbacks for when API keys aren't available

### Prompts (`prompts.py`) 

System prompts and templates for the agent system:

- `MANAGER_AGENT_PROMPT`: Main prompt for the manager agent
- Other specialized agent prompts
- Johnny Bravo-themed instructions and formatting guidelines

### Tracing (`tracing.py`)

Telemetry and observability utilities:

- `initialize_tracing()`: Set up OpenTelemetry tracing
- Components to track agent performance and interactions
- Debugging and monitoring tools

## Example Usage

Using the model utilities:

```python
from dude_diligence.utils.model import get_agent_model

# Get the configured model
model = get_agent_model()

# Use the model with the agents
# (The agents will typically handle this for you)
```

Setting up tracing:

```python
from dude_diligence.utils.tracing import initialize_tracing
from opentelemetry import trace

# Initialize tracing
initialize_tracing()

# Get a tracer for your component
tracer = trace.get_tracer("my-component")

# Create spans for operations
with tracer.start_as_current_span("my-operation") as span:
    # Set attributes
    span.set_attribute("operation.name", "example")
    
    # Your code here
    result = perform_operation()
    
    # Record the result
    span.set_attribute("operation.result", str(result))
``` 