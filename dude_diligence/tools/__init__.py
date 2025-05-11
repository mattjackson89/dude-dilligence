"""Tools for Dude Diligence data gathering.

Johnny's gadgets for checking out pretty companies.
"""

from dude_diligence.tools.companies_house import get_company_profile
from dude_diligence.tools.linkedin import fetch_linkedin_data

__all__ = ["get_company_profile", "fetch_linkedin_data"]
