# ruff: noqa: E501
"""Multi-agent system for company due diligence.

This module implements a hierarchical multi-agent system where specialized agents
work together to perform comprehensive UK company due diligence.

As Johnny Bravo would say: "Hey there, Pretty Companies! Let me check you out!" *hair flip*
"""

import logging
import json
from typing import Any
from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, tool, CodeAgent


from dude_diligence.tools.companies_house import (
    explore_companies_house_api,
    get_charges,
    get_company_officers,
    get_company_profile,
    get_endpoint_parameters,
    get_filing_history,
    get_persons_with_significant_control,
    get_schema_examples,
    perform_company_due_diligence,
    search_companies,
)
from dude_diligence.utils.model import get_agent_model
from dude_diligence.utils.prompts import (
    MANAGER_AGENT_PROMPT,
)

logger = logging.getLogger(__name__)


def create_finder_agent() -> ToolCallingAgent:
    """Create a specialized agent that focuses on finding company information from the web.

    This agent uses web search tools and specialized data sources to find information about companies
    from public sources like websites, news articles, LinkedIn, and business directories.

    Returns:
        ToolCallingAgent: A configured finder agent
    """
    model = get_agent_model()

    finder_agent = ToolCallingAgent(
        model=model,
        tools=[DuckDuckGoSearchTool()],
        name="finder_agent",
        description="Professional web research agent specializing in company information gathering",
    )

    return finder_agent


def create_companies_house_agent() -> ToolCallingAgent:
    """Create a specialized agent for retrieving Companies House data.

    This agent focuses on gathering comprehensive official data from
    the Companies House registry and providing detailed structured reports.

    Returns:
        ToolCallingAgent: A configured Companies House data agent
    """
    model = get_agent_model()

    companies_house_agent = ToolCallingAgent(
        model=model,
        tools=[
            search_companies,
            get_company_profile,
            get_company_officers,
            get_filing_history,
            get_persons_with_significant_control,
            get_charges,
            perform_company_due_diligence,
            explore_companies_house_api,
            get_endpoint_parameters,
            get_schema_examples,
        ],
        name="companies_house_agent",
        description="Professional Companies House data specialist providing detailed structured reports",
    )

    return companies_house_agent

# Create a placeholder tool for the additional research agent
@tool
def get_research_capabilities() -> dict[str, Any]:
    """Get information about future research capabilities.

    This tool provides information about what research capabilities
    will be added in future versions of the system.

    Returns:
        Dict containing information about future capabilities
    """
    future_capabilities = {
        "social_media_analysis": {
            "status": "planned",
            "description": "Analyze company presence on social media platforms",
            "timeline": "In development for next release",
        },
        "news_monitoring": {
            "status": "planned",
            "description": "Monitor news articles about the company for sentiment and key events",
            "timeline": "Planned for future enhancement",
        },
        "financial_analysis": {
            "status": "planned",
            "description": "Advanced financial statement analysis and trend visualization",
            "timeline": "Planned for next version",
        },
        "competitor_analysis": {
            "status": "planned",
            "description": "Comprehensive competitive landscape analysis",
            "timeline": "Future enhancement",
        },
    }

    return {
        "current_status": "Limited functionality in current version",
        "message": "This agent is a placeholder with enhanced capabilities coming in future releases",
        "future_capabilities": future_capabilities,
    }

def create_additional_research_agent() -> ToolCallingAgent:
    """Create a placeholder agent for future research capabilities.

    This agent is a placeholder for future expansion with additional
    research capabilities like social media analysis, sentiment analysis, etc.

    Returns:
        ToolCallingAgent: A configured placeholder research agent
    """
    model = get_agent_model()

    additional_research_agent = ToolCallingAgent(
        model=model,
        tools=[get_research_capabilities],
        name="additional_research_agent",
        description="Professional research agent with expanded capabilities in development",
    )

    return additional_research_agent


def create_manager_agent() -> ToolCallingAgent:
    """Create a manager agent to coordinate the other specialized agents.

    This manager agent orchestrates the overall due diligence process by delegating
    tasks to specialized agents and aggregating their outputs into a comprehensive report.

    Returns:
        ToolCallingAgent: A configured manager agent
    """
    model = get_agent_model()

    finder_agent = create_finder_agent()
    companies_house_agent = create_companies_house_agent()

    manager_agent = CodeAgent(
        model=model,
        tools=[],
        managed_agents=[finder_agent, companies_house_agent],
        name="manager_agent",
        description="Johnny Bravo himself: coordinating agents and compiling comprehensive due diligence reports with style",
        planning_interval=3,
    )

    return manager_agent


def run_due_diligence(company_name: str) -> dict:
    """Run a multi-agent due diligence process for a UK company and return a structured report."""
    from opentelemetry import trace
    tracer = trace.get_tracer("due-diligence-tracing")
    session_id = None
    try:
        current_span = trace.get_current_span()
        if current_span and hasattr(current_span, 'get_attribute'):
            session_id = current_span.get_attribute("session.id")
    except Exception as e:
        logger.warning(f"Could not access current span: {str(e)}")
    
    with tracer.start_as_current_span("Due-Diligence-Process") as span:
        # Add core attributes to the trace
        span.set_attribute("input.company_name", company_name)
        
        # Set a simplified input value
        span.set_attribute("input.value", f"Company: {company_name}")
        
        # Propagate the session ID if it was set in the parent context
        if session_id:
            span.set_attribute("langfuse.session.id", session_id)

        # Log the start of the process
        logger.info(f"Starting due diligence investigation for UK company '{company_name}'")

        # Create the manager agent
        manager_agent = create_manager_agent()

        # Task to collect data and generate report
        task = f"""Perform a comprehensive due diligence investigation on the UK company '{company_name}'

        {MANAGER_AGENT_PROMPT}
        """
        span.set_attribute("input.value", task)

        try:
            # Run the manager agent to collect data and generate report
            result = manager_agent.run(task)
            if isinstance(result, str):
                parsed_result = json.loads(result)
            else:
                parsed_result = result
            
            if parsed_result["image"] not in ["amazing.gif", "good.gif", "dubious.gif"]:
                parsed_result["image"] = "dubious.gif"
                
                
            # Record success and output
            span.set_attribute("status", "success")
            span.set_attribute("output.value", json.dumps(parsed_result))
                
            return parsed_result
                
        except Exception as e:
            # Record error in trace
            span.set_attribute("status", "error")
            span.set_attribute("error.message", str(e))
            
            # Return a properly formatted error response
            error_response = {
                "report": f"Error generating report: {str(e)}",
                "recommendation": "Unable to generate recommendation due to error",
                "image": "dubious.gif"
            }
            return error_response  # Return dictionary, not json.dumps(error_response)


def visualize_agent_structure():
    """Visualize the multi-agent structure.

    This function creates and visualizes the multi-agent structure
    without running any tasks.

    Returns:
        None
    """
    manager_agent = create_manager_agent()
    manager_agent.visualize()

    return "Multi-agent structure visualization complete. Man, I'm pretty! *hair flip*"
