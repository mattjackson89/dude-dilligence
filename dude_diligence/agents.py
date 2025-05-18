# ruff: noqa: E501
"""Multi-agent system for company due diligence.

This module implements a hierarchical multi-agent system where specialized agents
work together to perform comprehensive UK company due diligence.

As Johnny Bravo would say: "Hey there, Pretty Companies! Let me check you out!" *hair flip*
"""

import logging
from datetime import datetime
from typing import Any
from uuid import uuid4
import json

from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, tool, ToolCallingAgent

from dude_diligence.models import (
    CompanyBasicInfo,
    CorporateStructure,
    DueDiligenceReport,
    FinancialInfo,
    LeadershipInfo,
    LegalInfo,
    MarketInfo,
    OperationalInfo,
    OwnershipInfo,
    ReportMetadata,
    RiskAssessment,
    ScoringSystem,
)
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


@tool
def get_recommendation_images() -> dict[str, str]:
    """Get the available recommendation images.
    
    Returns:
        Dict containing paths to the available recommendation images:
        - amazing: For companies with excellent prospects
        - good: For companies with solid performance
        - dubious: For companies with concerning issues
    """
    return {
        "amazing": "app/images/amazing.gif",
        "good": "app/images/good.gif",
        "dubious": "app/images/dubious.gif"
    }

def calculate_company_scores(report: DueDiligenceReport) -> ScoringSystem:
    """Calculate comprehensive scores for a company based on the due diligence report.
    
    This function evaluates different aspects of the company and assigns scores
    based on the available information. Each score is between 0 and 1, where:
    - 0 represents high risk/poor performance
    - 1 represents low risk/excellent performance
    
    Args:
        report: The due diligence report containing company information
        
    Returns:
        ScoringSystem: A scoring system object with calculated scores
    """
    # Initialize scores
    scores = ScoringSystem()
    
    # Calculate financial health score
    if report.financial_info:
        # Consider factors like profitability, debt levels, cash flow
        financial_factors = []
        if hasattr(report.financial_info, 'profitability'):
            financial_factors.append(report.financial_info.profitability)
        if hasattr(report.financial_info, 'debt_levels'):
            financial_factors.append(1 - report.financial_info.debt_levels)  # Invert debt levels
        if hasattr(report.financial_info, 'cash_flow'):
            financial_factors.append(report.financial_info.cash_flow)
        
        scores.financial_health_score = sum(financial_factors) / len(financial_factors) if financial_factors else 0.5
    
    # Calculate operational risk score
    if report.operational_info:
        # Consider factors like operational efficiency, business continuity
        operational_factors = []
        if hasattr(report.operational_info, 'operational_efficiency'):
            operational_factors.append(report.operational_info.operational_efficiency)
        if hasattr(report.operational_info, 'business_continuity'):
            operational_factors.append(report.operational_info.business_continuity)
        
        scores.operational_risk_score = sum(operational_factors) / len(operational_factors) if operational_factors else 0.5
    
    # Calculate legal compliance score
    if report.legal_info:
        # Consider factors like regulatory compliance, legal disputes
        legal_factors = []
        if hasattr(report.legal_info, 'regulatory_compliance'):
            legal_factors.append(report.legal_info.regulatory_compliance)
        if hasattr(report.legal_info, 'legal_disputes'):
            legal_factors.append(1 - report.legal_info.legal_disputes)  # Invert legal disputes
        
        scores.legal_compliance_score = sum(legal_factors) / len(legal_factors) if legal_factors else 0.5
    
    # Calculate market position score
    if report.market_info:
        # Consider factors like market share, competitive position
        market_factors = []
        if hasattr(report.market_info, 'market_share'):
            market_factors.append(report.market_info.market_share)
        if hasattr(report.market_info, 'competitive_position'):
            market_factors.append(report.market_info.competitive_position)
        
        scores.market_position_score = sum(market_factors) / len(market_factors) if market_factors else 0.5
    
    # Calculate leadership quality score
    if report.leadership:
        # Consider factors like experience, track record
        leadership_factors = []
        if hasattr(report.leadership, 'experience'):
            leadership_factors.append(report.leadership.experience)
        if hasattr(report.leadership, 'track_record'):
            leadership_factors.append(report.leadership.track_record)
        
        scores.leadership_quality_score = sum(leadership_factors) / len(leadership_factors) if leadership_factors else 0.5
    
    # Calculate overall score (weighted average)
    weights = {
        'financial_health': 0.3,
        'operational_risk': 0.2,
        'legal_compliance': 0.2,
        'market_position': 0.15,
        'leadership_quality': 0.15
    }
    
    scores.overall_score = (
        scores.financial_health_score * weights['financial_health'] +
        scores.operational_risk_score * weights['operational_risk'] +
        scores.legal_compliance_score * weights['legal_compliance'] +
        scores.market_position_score * weights['market_position'] +
        scores.leadership_quality_score * weights['leadership_quality']
    )
    
    # Calculate confidence level based on data completeness
    data_points = sum(1 for score in [
        scores.financial_health_score,
        scores.operational_risk_score,
        scores.legal_compliance_score,
        scores.market_position_score,
        scores.leadership_quality_score
    ] if score > 0)
    
    scores.confidence_level = data_points / 5.0
    
    # Generate score explanation
    score_explanations = []
    if scores.financial_health_score > 0:
        score_explanations.append(f"Financial Health: {scores.financial_health_score:.2f}")
    if scores.operational_risk_score > 0:
        score_explanations.append(f"Operational Risk: {scores.operational_risk_score:.2f}")
    if scores.legal_compliance_score > 0:
        score_explanations.append(f"Legal Compliance: {scores.legal_compliance_score:.2f}")
    if scores.market_position_score > 0:
        score_explanations.append(f"Market Position: {scores.market_position_score:.2f}")
    if scores.leadership_quality_score > 0:
        score_explanations.append(f"Leadership Quality: {scores.leadership_quality_score:.2f}")
    
    scores.score_explanation = "\n".join(score_explanations)
    
    return scores

def create_manager_agent() -> ToolCallingAgent:
    """Create a manager agent that coordinates the specialized agents.

    This agent delegates tasks to specialized agents and compiles their
    findings into a comprehensive due diligence report with Johnny Bravo's style.

    Returns:
        ToolCallingAgent: A configured manager agent with Johnny's leadership swagger
    """
    model = get_agent_model()

    # Create the specialized agents
    finder_agent = create_finder_agent()
    companies_house_agent = create_companies_house_agent()
    additional_research_agent = create_additional_research_agent()

    # Create the manager agent with the specialized agents and tools
    manager_agent = ToolCallingAgent(
        model=model,
        tools=[],
        managed_agents=[finder_agent, companies_house_agent, additional_research_agent],
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
            parsed_result = json.loads(result)
            
            if parsed_result["image"] not in ["amazing.gif", "good.gif", "dubious.gif"]:
                parsed_result["image"] = "dubious.gif"  # Default to dubious if invalid
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
            return json.dumps(error_response)


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
