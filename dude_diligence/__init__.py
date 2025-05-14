"""Dude Diligence package for company research and analysis.

As Johnny would say, "Heyyy there, Pretty Company Data!"
"""

__version__ = "0.1.0"

# Import tracing utilities first, but DO NOT initialize yet
from dude_diligence.utils.tracing import initialize_tracing

# Import other modules
from dude_diligence.agents import (
    create_additional_research_agent,
    create_companies_house_agent,
    create_finder_agent,
    create_manager_agent,
    run_due_diligence,
    visualize_agent_structure,
)

# Keep necessary tool imports
from dude_diligence.tools.companies_house import (
    get_charges,
    get_company_officers,
    get_company_profile,
    get_filing_history,
    get_persons_with_significant_control,
    search_companies,
)

__all__ = [
    # Main function
    "run_due_diligence",
    # Multi-agent components
    "create_manager_agent",
    "create_finder_agent",
    "create_companies_house_agent",
    "create_additional_research_agent",
    "visualize_agent_structure",
    # Core tools
    "search_companies",
    "get_company_profile",
    "get_company_officers",
    "get_filing_history",
    "get_persons_with_significant_control",
    "get_charges",
    # Tracing utilities
    "initialize_tracing",
]
