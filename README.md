# Dude Diligence

*"Hey there, Pretty Company! Wanna see me flex my due diligence muscles?"* - Johnny Bravo, Corporate Researcher

An AI-powered due diligence tool that does the hard work of researching companies, so you can spend more time combing your hair.

## What's This All About, Pretty Mama?

Dude Diligence helps you gather intel faster than Johnny can strike a pose:
- Web search results *(Johnny checking the internet)*
- Companies House data *(official records, man)*
- LinkedIn profiles *(professional networking, oh yeah!)*
- Other public information *(Johnny's got connections everywhere)*

## Getting Started (Oh Mama!)

### What You'll Need
- Docker and Docker Compose *(as slick as Johnny's hair)*
- Python 3.13+ *(smart like Johnny's... well, not Johnny)*
- uv for Python package management *(faster than Johnny's pickup lines)*

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dude-diligence.git
cd dude-diligence
```

2. Create a `.env` file with your API keys (see .env.example for required variables)

3. Build and start the application with Docker:
```bash
docker-compose up --build
```

### Development Setup

For local development without Docker (Johnny prefers it this way):

1. Set up a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
uv pip install -e .
```

3. Run the application:
```bash
python -m app.main
```

## Agent-powered Research (Johnny's Secret Technique)

Dude Diligence is powered by smol-agents, a lightweight LLM agent framework that lets Johnny Bravo flex his research muscles:

- **Code Agents**: Johnny writes Python code to analyze companies
- **Tool Integration**: Johnny can search the web, check company registries, and look up LinkedIn profiles
- **Interactive UI**: Watch Johnny do his research in real-time with cool visualizations

### Using the Agent from Python

You can also use the agent programmatically:

```python
from dude_diligence.agents import create_dude_diligence_agent

# Create the agent
agent = create_dude_diligence_agent()

# Run due diligence on a company
result = agent.run(
    "Perform due diligence research on the company 'Acme Ltd' based in United Kingdom. "
    "Focus on leadership and financial information."
)

# Print the results
print(result)
```

## The Blueprint (Johnny's Workout Plan)

```
dude-diligence/
├── .env                  # Secret stuff (Johnny's hair products)
├── .gitignore            # What to ignore (like Johnny ignores rejection)
├── Dockerfile            # Docker config (container as strong as Johnny)
├── docker-compose.yml    # Docker Compose (Johnny's choreography)
├── README.md             # This file (Johnny's pickup manual)
├── pyproject.toml        # Project config (Johnny's workout regimen)
├── app/                  # Gradio UI (Johnny's good looks)
│   ├── main.py           # Entry point (Johnny's entrance)
│   └── ui.py             # Interface (Johnny's style)
├── notebooks/            # Development notebooks (Johnny's practice lines)
│   └── dev.ipynb         # For prototyping (Johnny rehearsing)
└── dude_diligence/       # Core package (Johnny's muscles)
    ├── __init__.py       # Package marker (Johnny was here)
    ├── agents.py         # Agent orchestration (Johnny's moves)
    ├── tools/            # Agent tools (Johnny's gadgets)
    │   ├── __init__.py
    │   ├── web_search.py
    │   ├── companies_house.py
    │   └── linkedin.py
    └── utils/            # Utilities (Johnny's accessories)
        ├── __init__.py
        ├── prompts.py    # LLM prompts (Johnny's pickup lines)
        └── parsers.py    # Response parsers (Johnny's translators)
```

## Usage

Once running, navigate to http://localhost:7860 to access the Gradio interface.

*"Man, I'm pretty! Let's do some due diligence!"*

## License

[MIT License](LICENSE) *(Even Johnny respects the law)*