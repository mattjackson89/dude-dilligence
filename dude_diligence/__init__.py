"""Dude Diligence package for company research and analysis.

As Johnny would say, "Heyyy there, Pretty Company Data!"
"""

__version__ = "0.1.0"

from dude_diligence.agents import run_dude_diligence, create_dude_diligence_agent
from dude_diligence.tools import search_company, get_company_profile, fetch_linkedin_data

__all__ = [
    "run_dude_diligence", 
    "create_dude_diligence_agent",
    "search_company", 
    "get_company_profile", 
    "fetch_linkedin_data"
] 