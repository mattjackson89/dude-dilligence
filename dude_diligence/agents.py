# ruff: noqa: E501
"""Multi-agent system for company due diligence.

This module implements a hierarchical multi-agent system where specialized agents
work together to perform comprehensive UK company due diligence.

As Johnny Bravo would say: "Hey there, Pretty Companies! Let me check you out!" *hair flip*
"""

import logging
from typing import Any

from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, tool, ToolCallingAgent

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
    ADDITIONAL_RESEARCH_AGENT_PROMPT,
    COMPANIES_HOUSE_AGENT_PROMPT,
    FINDER_AGENT_PROMPT,
    MANAGER_AGENT_PROMPT,
)

logger = logging.getLogger(__name__)


def create_finder_agent() -> ToolCallingAgent:
    """Create a specialized agent that focuses on finding company information from the web.

    This agent uses web search tools to find information about companies
    from public sources like websites, news articles, and business directories.

    Returns:
        ToolCallingAgent: A configured finder agent
    """
    model = get_agent_model()

    finder_agent = ToolCallingAgent(
        model=model,
        tools=[DuckDuckGoSearchTool()],
        name="finder_agent",
        description="Johnny Bravo's web searcher: finding company info with style and flair",
    )

    return finder_agent


def create_companies_house_agent() -> ToolCallingAgent:
    """Create a specialized agent for retrieving Companies House data.

    This agent focuses on gathering comprehensive official data from
    the Companies House registry.

    Returns:
        ToolCallingAgent: A configured Companies House data agent with Johnny's swagger
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
        description="Johnny's official data collector: retrieving UK company data with flair",
    )

    return companies_house_agent


# Create a placeholder tool for the additional research agent
@tool
def get_research_capabilities() -> dict[str, Any]:
    """Get information about future research capabilities.

    This tool provides information about what research capabilities
    will be added in future versions of the system.

    Returns:
        Dict containing information about future capabilities with Johnny's optimism
    """
    future_capabilities = {
        "social_media_analysis": {
            "status": "planned",
            "description": "Analyze company presence on social media - Johnny style!",
            "timeline": "In development - getting my hair ready for the cameras!",
        },
        "news_monitoring": {
            "status": "planned",
            "description": "Monitor news articles about the company - the way Johnny monitors the ladies!",
            "timeline": "Future enhancement - working on my pickup lines!",
        },
        "financial_analysis": {
            "status": "planned",
            "description": "Advanced financial statement analysis - Johnny knows numbers too, baby!",
            "timeline": "Planned for next version - flexing my analytical muscles!",
        },
        "competitor_analysis": {
            "status": "planned",
            "description": "Analysis of company competitors - Johnny always checks out the competition!",
            "timeline": "Future enhancement - gotta stay ahead of those other guys!",
        },
    }

    return {
        "current_status": "Just warming up, baby! *hair flip*",
        "message": "This agent is a placeholder but will be as impressive as Johnny's biceps soon!",
        "future_capabilities": future_capabilities,
    }


def create_additional_research_agent() -> ToolCallingAgent:
    """Create a placeholder agent for future research capabilities.

    This agent is a placeholder for future expansion with additional
    research capabilities like social media analysis, sentiment analysis, etc.

    Returns:
        ToolCallingAgent: A configured placeholder research agent with Johnny's optimism
    """
    model = get_agent_model()

    additional_research_agent = ToolCallingAgent(
        model=model,
        tools=[get_research_capabilities],
        name="additional_research_agent",
        description="Johnny's future research muscles - not yet flexed but full of potential!",
    )

    return additional_research_agent


def create_manager_agent() -> ToolCallingAgent:
    """Create a manager agent that coordinates the specialized agents.

    This agent delegates tasks to specialized agents and compiles their
    findings into a comprehensive due diligence report.

    Returns:
        ToolCallingAgent: A configured manager agent with Johnny's leadership swagger
    """
    model = get_agent_model()

    # Create the specialized agents
    finder_agent = create_finder_agent()
    companies_house_agent = create_companies_house_agent()
    additional_research_agent = create_additional_research_agent()

    # Create the manager agent with the specialized agents
    manager_agent = ToolCallingAgent(
        model=model,
        tools=[],  # Manager doesn't need direct tools
        managed_agents=[finder_agent, companies_house_agent, additional_research_agent],
        name="manager_agent",
        description="Johnny Bravo himself: coordinating agents and flexing analytical muscles",
        planning_interval=3,  # Plan after every 3 steps - Johnny likes to keep things moving!
    )

    return manager_agent


def run_due_diligence(
    company_name: str,
    research_areas: list[str] | None = None,
) -> str:
    """Run a multi-agent due diligence process for a UK company.

    This function coordinates multiple specialized agents to perform
    comprehensive due diligence on a UK company.

    Args:
        company_name: Name of the UK company to research (the "pretty lady" of the hour)
        research_areas: Specific areas to research (Johnny's pickup lines)

    Returns:
        str: Formatted markdown report with research findings and Johnny's commentary
    """
    # Get the tracer
    from opentelemetry import trace
    tracer = trace.get_tracer("due-diligence-tracing")
    
    # Safely get the session ID if available
    session_id = None
    try:
        current_span = trace.get_current_span()
        # Check if the span is valid and has the attribute
        if current_span and hasattr(current_span, 'get_attribute'):
            session_id = current_span.get_attribute("session.id")
    except Exception as e:
        # Fail silently if there's an issue with span access
        logger.warning(f"Could not access current span: {str(e)}")
    
    with tracer.start_as_current_span("Due-Diligence-Process") as span:
        # Add core attributes to the trace
        span.set_attribute("input.company_name", company_name)
        
        # Only add research_areas if not None
        if research_areas:
            span.set_attribute("input.research_areas", ", ".join(research_areas))
        
        # Set a simplified input value
        span.set_attribute("input.value", f"Company: {company_name}")
        
        # Propagate the session ID if it was set in the parent context
        if session_id:
            span.set_attribute("langfuse.session.id", session_id)
        
        if research_areas is None:
            research_areas = ["Basic Info"]

        # Log the start of the process
        logger.info(f"Johnny Bravo is checking out UK company '{company_name}' *hair flip*")

        # Create the manager agent
        manager_agent = create_manager_agent()

        # Format the task instructions, including the MANAGER_AGENT_PROMPT
        task = f"""
        {MANAGER_AGENT_PROMPT}

        Coordinate a comprehensive due diligence investigation on the UK company '{company_name}'.
        Focus on these research areas: {", ".join(research_areas)}.

        Follow this workflow:
        1. First use the finder_agent to gather information about the company from public web sources
           When using the finder_agent, instruct it with: "{FINDER_AGENT_PROMPT}"

        2. Then use the companies_house_agent to gather comprehensive official data from the UK registry
           When using the companies_house_agent, instruct it with: "{COMPANIES_HOUSE_AGENT_PROMPT}"

        3. Also check with the additional_research_agent about future research capabilities
           When using the additional_research_agent, instruct it with: "{ADDITIONAL_RESEARCH_AGENT_PROMPT}"

        4. Finally, analyze all the information and compile a detailed due diligence report

        Your final report should include:
        - Executive summary with key findings (with Johnny's enthusiasm)
        - Company overview and structure (delivered with confidence)
        - Leadership analysis (with comments on which executives have "style")
        - Financial assessment (presented with Johnny-style flair)
        - Risk analysis and opportunities (with Johnny's optimism)
        - Suggestions for future research (based on the additional_research_agent's capabilities)

        Return the final report in professional markdown format with Johnny Bravo's unique flair,
        including occasional catchphrases like "Hey there, pretty data!", "Oh mama!", and "*does hair flip*"
        action markers when presenting particularly important findings.
        """
        span.set_attribute("input.value", task)

        try:
            # Run the manager agent with this task
            result = manager_agent.run(task)
            
            # Record success and output
            span.set_attribute("status", "success")
            span.set_attribute("output.value", result)
            span.set_attribute("output.summary", result[:500] + "..." if len(result) > 500 else result)
            span.set_attribute("report.length", len(result))
            
            return result
            
        except Exception as e:
            # Record error in trace
            span.set_attribute("status", "error")
            span.set_attribute("error.message", str(e))
            
            # Re-raise the exception for proper error handling upstream
            raise


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
