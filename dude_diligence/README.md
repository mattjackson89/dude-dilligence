# Dude Diligence Core Package

*"Hey there, Pretty Data! Let me analyze you real good!"* - Johnny Bravo

This is the core package containing the implementation of the due diligence agents and tools.

## Package Structure

- **agents.py**: Multi-agent system implementation for orchestrating research
- **models.py**: Data models and schemas for structured report information
- **__init__.py**: Package exports and convenience imports
- **tools/**: API integrations and specialized research tools
- **utils/**: Helper utilities, model configuration, and prompts
- **specs/**: API specifications and schemas

## Key Components

### Agent System

The multi-agent architecture allows specialized agents to collaborate:

- Manager Agent coordinates research and compiles results
- Finder Agent performs web searches and public information gathering
- Companies House Agent retrieves official UK company registry data

### Data Models

The package uses structured data models for consistent report generation:

- CompanyBasicInfo
- LeadershipInfo
- FinancialInfo
- And other specialized information categories

### Research Tools

The tools directory provides API integrations for data gathering:

- Companies House API client for official UK company data
- Additional data sources and APIs (expandable)

## Integration

This package can be used directly in Python applications or via the Gradio UI in the `app/` directory. 