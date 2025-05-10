#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Companies House API interface for UK company information.

"Hey there, Company House! Let me check out that pretty company's records!"
"""

import os
import logging
from typing import Dict, Any, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from smolagents import tool

logger = logging.getLogger(__name__)

# Placeholder for actual API implementation
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY", "")
BASE_URL = "https://api.company-information.service.gov.uk"


@tool
def get_company_profile(company_name: str, search_first: bool = True) -> Dict[str, Any]:
    """Get company profile information from Companies House.
    
    This tool fetches official company information from Companies House (UK).
    It returns registration details, status, address, and other official information.
    
    Args:
        company_name: Name or number of the company
        search_first: Whether to search for the company first to get the company number
    """
    logger.info(f"Getting profile for {company_name} from Companies House")
    
    # This is a placeholder for the actual implementation
    # In a real implementation, you would authenticate and call the Companies House API

    # Placeholder company profile data
    company_profile = {
        "company_name": company_name,
        "company_number": "12345678",
        "company_status": "active",
        "company_type": "private-limited-company",
        "registered_office_address": {
            "address_line_1": "123 Business Street",
            "locality": "London",
            "postal_code": "EC1A 1BB",
            "country": "United Kingdom"
        },
        "date_of_creation": "2020-01-01",
        "last_full_members_list_date": "2022-12-31",
        "has_charges": False,
        "has_insolvency_history": False,
        "has_super_secure_pscs": False,
        "sic_codes": ["62020"],
        "jurisdiction": "united-kingdom",
    }
    
    return company_profile


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _search_company(company_name: str) -> Optional[str]:
    """Search for a company by name to get its company number.
    
    Args:
        company_name: Name of the company to search for
        
    Returns:
        Company number if found, None otherwise
    """
    # Placeholder implementation
    return "12345678"


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _get_company_by_number(company_number: str) -> Dict[str, Any]:
    """Get detailed company information by company number.
    
    Args:
        company_number: The Companies House company number
        
    Returns:
        Dict containing company information
    """
    # Placeholder implementation
    return {} 