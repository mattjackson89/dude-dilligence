# Dude Diligence Examples

*"Hey there, Pretty Coder! Check out these awesome examples!"* - Johnny Bravo

This directory contains example scripts demonstrating how to use the Dude Diligence package for company research.

## Available Examples

### 1. Multi-Agent Example (`multi_agent_example.py`)

Demonstrates the full multi-agent due diligence system in action:

- Agent structure visualization
- Complete due diligence process on a sample company
- Results formatting and display

To run:

```bash
# From repository root
python examples/multi_agent_example.py
```

Required environment variables:
- `COMPANIES_HOUSE_API_KEY`: Your Companies House API key
- `OPENAI_API_KEY`: Optional, for faster model inference (falls back to HF models)

### 2. OpenTelemetry Tracing Example (`tracing_example.py`)

Shows how to use the telemetry and tracing capabilities:

- OpenTelemetry integration
- Agent interaction tracing
- Performance monitoring

To run:

```bash
# From repository root
python examples/tracing_example.py
```

Additional requirements:
- OpenTelemetry collector (optional for visualization)

## Running the Examples

Before running examples:

1. Ensure you have installed the package:
   ```bash
   # From repository root
   uv pip install -e .
   ```

2. Set up required environment variables:
   ```bash
   export COMPANIES_HOUSE_API_KEY=your_key_here
   export OPENAI_API_KEY=your_key_here  # Optional
   ```

3. Run the desired example script:
   ```bash
   python examples/multi_agent_example.py
   ```

## Creating Your Own Examples

You can use these examples as templates for your own research scripts:

1. Import the necessary components:
   ```python
   from dude_diligence import run_due_diligence, visualize_agent_structure
   ```

2. Configure and run the due diligence:
   ```python
   # The function automatically determines which research areas to cover
   result = run_due_diligence(company_name="Your Company Name")
   ```

3. Process and use the results as needed:
   ```python
   # Access specific sections
   basic_info = result.get("basic_info", {})
   leadership = result.get("leadership", {})
   
   # Display or store the data
   print(f"Company: {basic_info.get('name')}")
   ```

See the example scripts for more detailed usage patterns. 