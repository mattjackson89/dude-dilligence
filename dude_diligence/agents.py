#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Core agent orchestration for Dude Diligence.

As Johnny would say: "Hey there, Pretty Data! I'm gonna analyze you real good!"
"""

import logging
import os
from typing import Dict, List, Any, Optional

from dude_diligence.tools.web_search import search_company
from dude_diligence.tools.companies_house import get_company_profile
from dude_diligence.tools.linkedin import fetch_linkedin_data
from dude_diligence.utils.prompts import SYSTEM_PROMPT, REPORT_TEMPLATE
from dude_diligence.utils.parsers import parse_response

from smolagents import (
    CodeAgent, 
    OpenAIServerModel, 
    HfApiModel, 
    PromptTemplates,
    PlanningPromptTemplate,
    ManagedAgentPromptTemplate,
    FinalAnswerPromptTemplate
)

# Set up logging (Johnny keeps track of his pickup attempts)
logger = logging.getLogger(__name__)

def get_agent_model():
    """Get the appropriate LLM model for the agent based on environment variables.
    
    Johnny's checking what model he can flirt with today!
    
    Returns:
        An initialized model for the smolagents
    """
    # Check for OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        logger.info("Using OpenAI model for the agent")
        return OpenAIServerModel(
            model_id="gpt-4o",
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    # Fallback to Hugging Face model
    logger.info("Using Hugging Face model for the agent")
    return HfApiModel(
        model_id="meta-llama/Llama-3.3-70B-Instruct",
        temperature=0.2,
    )

def create_dude_diligence_agent():
    """Create and return the due diligence agent with all necessary tools.
    
    Johnny's assembling his research toolkit!
    
    Returns:
        CodeAgent: An initialized agent with all due diligence tools
    """
    # Get the model for the agent
    model = get_agent_model()
    
    # Create the agent with our tools - using default prompts
    agent = CodeAgent(
        model=model,
        tools=[
            get_company_profile,
            search_company,
            fetch_linkedin_data
        ]
        # No custom prompt_templates, using defaults
    )
    
    return agent

def run_dude_diligence(
    company_name: str,
    country: str = "United Kingdom",
    research_areas: Optional[List[str]] = None,
) -> str:
    """Run the due diligence process for a given company.
    
    Johnny's approach to company research - flex those investigative muscles!
    
    Args:
        company_name: Name of the company to research
        country: Country where the company is registered
        research_areas: Specific areas to research
        
    Returns:
        str: Formatted markdown report with research findings
    """
    if research_areas is None:
        research_areas = ["Basic Info"]
    
    # Johnny announces his intentions
    logger.info(f"Starting due diligence for {company_name} in {country}")
    
    # Create the agent
    agent = create_dude_diligence_agent()
    
    # Format the task with your domain-specific instructions
    task = f"""
    Perform due diligence research on the company '{company_name}' based in {country}.
    Focus on these areas: {', '.join(research_areas)}.
    
    {SYSTEM_PROMPT}
    
    Collect information from available sources, analyze the data, and generate a comprehensive
    due diligence report that includes company profile, market analysis, leadership team, 
    financials, and risks/opportunities assessment.
    
    Return the final report in markdown format.
    """
    
    # Run the agent with this task
    result = agent.run(task)
    
    return result 