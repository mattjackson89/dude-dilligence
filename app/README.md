# Dude Diligence Web UI

*"Hey there, Pretty User! Welcome to my slick interface!"* - Johnny Bravo

This directory contains the Gradio web interface for Dude Diligence, allowing users to interact with the due diligence system through a user-friendly UI.

## Components

- **main.py**: Entry point that initializes and launches the Gradio app
- **ui.py**: Defines the user interface components and callbacks
- **images/**: Contains image assets for the UI

## Features

The Gradio UI provides the following functionality:

1. **Company Research Form**: Enter a UK company name to start due diligence
2. **Research Results Display**: View structured findings with Johnny's commentary
3. **Recommendation Summary**: Get a quick assessment with a Johnny-themed rating
4. **Interactive Chat**: Ask follow-up questions about the company research
5. **Custom Styling**: Johnny Bravo-themed visuals and interactions
6. **OpenTelemetry Tracing**: Built-in observability for monitoring and debugging

## Running the UI

### Using Docker:

```bash
docker-compose up --build
```

### Direct Python execution:

```bash
# From repository root
python -m app.main
```

Once running, the UI is accessible at: http://localhost:7860

## UI Architecture

The UI implements a `ReportContextAgent` wrapper that maintains the context of the report between interactions, allowing the chat functionality to reference previously generated due diligence data. This agent:

1. Stores the generated report content and company name
2. Provides context to the base agent for each chat interaction
3. Uses OpenTelemetry tracing to monitor chat performance
4. Formats responses in Johnny Bravo's distinctive style

## Development

To modify the UI:

1. Edit `ui.py` to change layout or functionality
2. Edit CSS in the `gr.Blocks()` call to modify styling
3. Update prompts in `ReportContextAgent.run()` to change Johnny's personality

The UI uses Gradio's reactive components model, so most changes will be automatically reflected when you refresh the browser. 