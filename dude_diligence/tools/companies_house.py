#!/usr/bin/env python3

"""Companies House API interface for UK company information.

Access official UK company registry data through the Companies House API.
"Hey there, Pretty Company! Let me check out those UK company records!"
"""

import base64
import logging
import os
from typing import Any

import httpx
from smolagents import tool
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
)

# Import schema utilities
from dude_diligence.utils.companies_house_utils import (
    get_endpoint_definitions,
    load_schema,
)

logger = logging.getLogger(__name__)

# Get API key from environment variables
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY", "")
BASE_URL = "https://api.company-information.service.gov.uk"


def _get_auth_header():
    """Create the authentication header for Companies House API."""
    if not API_KEY:
        raise ValueError("COMPANIES_HOUSE_API_KEY environment variable not set")

    auth_str = f"{API_KEY}:"
    auth_bytes = auth_str.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")

    return {"Authorization": f"Basic {auth_b64}", "Accept": "application/json"}


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException)),
)
def _make_request(method: str, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Make a request to the Companies House API with error handling and retries.

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Full URL to request
        params: Optional query parameters

    Returns:
        Dictionary containing the response or error information
    """
    try:
        headers = _get_auth_header()
        with httpx.Client(timeout=30.0) as client:
            response = client.request(method, url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error: {e}")
        if e.response.status_code == 404:
            return {"error": "Resource not found", "status_code": 404}
        elif e.response.status_code == 401:
            return {"error": "Authentication failed", "status_code": 401}
        else:
            return {"error": str(e), "status_code": e.response.status_code}
    except Exception as e:
        logger.error(f"Error making request: {e}")
        return {"error": str(e)}


@tool
def search_companies(company_name: str, items_per_page: int = 20) -> dict[str, Any]:
    """Search for UK companies by name.

    This tool searches the Companies House database to find UK companies matching the provided name.
    It returns a list of matching companies with their basic details.

    Args:
        company_name: Name or partial name of the UK company to search for
        items_per_page: Number of results to return per page (max 100)
    """
    logger.info(f"Searching for UK companies matching '{company_name}'")

    url = f"{BASE_URL}/search/companies"
    params = {"q": company_name, "items_per_page": items_per_page}

    return _make_request("GET", url, params=params)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _search_company(company_name: str) -> str | None:
    """Search for a company by name to get its company number.

    Args:
        company_name: Name of the company to search for

    Returns:
        Company number if found, None otherwise
    """
    search_results = search_companies(company_name)

    if "error" in search_results:
        logger.error(f"Error searching for company: {search_results['error']}")
        return None

    items = search_results.get("items", [])
    if not items:
        logger.warning(f"No companies found matching '{company_name}'")
        return None

    # Return the company number of the first match
    return items[0].get("company_number")


@tool
def get_company_profile(company_name: str, search_first: bool = True) -> dict[str, Any]:
    """Get company profile information from Companies House (UK).

    This tool fetches official company information from Companies House, the UK's company registry.
    It returns registration details, status, registered address, and other official information.

    Args:
        company_name: Name or number of the UK company
        search_first: Whether to search for the company first to get the company number
    """
    logger.info(f"Getting profile for UK company {company_name} from Companies House")

    company_number = company_name

    # If we need to search first and the input doesn't look like a company number
    if search_first and not (company_name.isalnum() and len(company_name) <= 8):
        company_number = _search_company(company_name)
        if not company_number:
            return {
                "error": f"Could not find company number for UK company '{company_name}'",
                "company_name": company_name,
            }

    # Get the company profile by number
    url = f"{BASE_URL}/company/{company_number}"
    profile = _make_request("GET", url)

    # If there was an error, include the company name in the response
    if "error" in profile:
        profile["company_name"] = company_name

    return profile


@tool
def get_company_officers(company_number: str, items_per_page: int = 20) -> dict[str, Any]:
    """Get the officers (directors, secretaries, etc.) of a company.

    This tool fetches the list of officers associated with a company from Companies House.
    It returns details about directors, secretaries, and other official positions.

    Args:
        company_number: The Companies House company number
        items_per_page: Number of results to return per page (max 100)
    """
    logger.info(f"Getting officers for company number {company_number}")

    url = f"{BASE_URL}/company/{company_number}/officers"
    params = {"items_per_page": items_per_page}

    return _make_request("GET", url, params=params)


@tool
def get_filing_history(company_number: str, items_per_page: int = 20) -> dict[str, Any]:
    """Get the filing history of a company.

    This tool fetches the list of filings made by a company to Companies House.
    It returns information about annual returns, accounts, and other regulatory filings.

    Args:
        company_number: The Companies House company number
        items_per_page: Number of results to return per page (max 100)
    """
    logger.info(f"Getting filing history for company number {company_number}")

    url = f"{BASE_URL}/company/{company_number}/filing-history"
    params = {"items_per_page": items_per_page}

    return _make_request("GET", url, params=params)


@tool
def get_persons_with_significant_control(
    company_number: str, items_per_page: int = 20
) -> dict[str, Any]:
    """Get persons with significant control (PSC) over a company.

    This tool fetches information about individuals or entities with significant control
    or influence over a company, as required by UK transparency regulations.

    Args:
        company_number: The Companies House company number
        items_per_page: Number of results to return per page (max 100)
    """
    logger.info(f"Getting PSCs for company number {company_number}")

    url = f"{BASE_URL}/company/{company_number}/persons-with-significant-control"
    params = {"items_per_page": items_per_page}

    return _make_request("GET", url, params=params)


@tool
def get_charges(company_number: str, items_per_page: int = 20) -> dict[str, Any]:
    """Get the charges (mortgages, etc.) registered against a company.

    This tool fetches information about charges and mortgages registered against a company.
    It returns details of security provided by a company over its assets.

    Args:
        company_number: The Companies House company number
        items_per_page: Number of results to return per page (max 100)
    """
    logger.info(f"Getting charges for company number {company_number}")

    url = f"{BASE_URL}/company/{company_number}/charges"
    params = {"items_per_page": items_per_page}

    return _make_request("GET", url, params=params)


@tool
def perform_company_due_diligence(
    company_name: str, include_sections: list[str] | None = None
) -> dict[str, Any]:
    """Perform comprehensive due diligence on a UK company.

    This tool conducts a thorough investigation of a UK registered company by:
    1. Searching for the company by name in the UK Companies House registry
    2. Retrieving its official profile, officers, and filing history
    3. Checking persons with significant control (PSCs)
    4. Checking charges (mortgages etc.) against the company

    Args:
        company_name: Name of the UK company to investigate
        include_sections: List of sections to include in the report
                          Options: ["profile", "officers", "filing_history", "pscs", "charges"]
                          If None, all sections are included
    """
    logger.info(f"Performing due diligence on UK company '{company_name}'")

    # Default to including all sections if not specified
    if include_sections is None:
        include_sections = ["profile", "officers", "filing_history", "pscs", "charges"]

    # Validate section names
    valid_sections = ["profile", "officers", "filing_history", "pscs", "charges"]
    invalid_sections = [s for s in include_sections if s not in valid_sections]
    if invalid_sections:
        return {
            "error": f"Invalid section(s): {', '.join(invalid_sections)}",
            "valid_sections": valid_sections,
        }

    # Step 1: Find company by name
    search_results = search_companies(company_name)
    if "error" in search_results or not search_results.get("items"):
        return {"error": f"UK company '{company_name}' not found in Companies House registry"}

    # Get the company number from the first match
    company_number = search_results["items"][0]["company_number"]
    company_info = {"company_search": search_results}

    # Step 2: Gather requested company information
    if "profile" in include_sections:
        company_info["profile"] = get_company_profile(company_number, search_first=False)

    if "officers" in include_sections:
        company_info["officers"] = get_company_officers(company_number)

    if "filing_history" in include_sections:
        company_info["filing_history"] = get_filing_history(company_number)

    if "pscs" in include_sections:
        company_info["pscs"] = get_persons_with_significant_control(company_number)

    if "charges" in include_sections:
        company_info["charges"] = get_charges(company_number)

    return company_info


@tool
def explore_companies_house_api() -> dict[str, Any]:
    """Explore the Companies House API schema to discover available endpoints.

    This tool returns a list of all available endpoints in the Companies House API,
    along with their descriptions. Use this to understand what data you can retrieve.
    """
    logger.info("Exploring Companies House API schema")

    endpoints = get_endpoint_definitions()
    if not endpoints:
        return {"error": "Could not load API schema"}

    # Create a simplified overview of available endpoints
    endpoint_overview = {}
    for name, details in endpoints.items():
        endpoint_overview[name] = {
            "path": details["path"],
            "method": details["method"],
            "description": details["description"],
        }

    return {
        "available_endpoints": list(endpoint_overview.keys()),
        "endpoint_details": endpoint_overview,
    }


@tool
def get_endpoint_parameters(endpoint_name: str) -> dict[str, Any]:
    """Get detailed information about a specific Companies House API endpoint.

    This tool provides detailed information about a specific endpoint, including
    required and optional parameters, and their descriptions.

    Args:
        endpoint_name: Name of the endpoint to get details for (e.g., "search-companies")
    """
    logger.info(f"Getting parameter details for endpoint: {endpoint_name}")

    endpoints = get_endpoint_definitions()
    if not endpoints:
        return {"error": "Could not load API schema"}

    if endpoint_name not in endpoints:
        return {
            "error": f"Endpoint '{endpoint_name}' not found",
            "available_endpoints": list(endpoints.keys()),
        }

    endpoint_info = endpoints[endpoint_name]
    parameters = endpoint_info.get("parameters", [])

    # Organize parameters by required/optional
    required_params = []
    optional_params = []

    for param in parameters:
        param_info = {
            "name": param.get("name", ""),
            "description": param.get("description", ""),
            "type": param.get("type", "string"),
            "in": param.get("in", "query"),  # Where the parameter appears (path, query, etc.)
        }

        if param.get("required", False):
            required_params.append(param_info)
        else:
            optional_params.append(param_info)

    return {
        "endpoint_name": endpoint_name,
        "path": endpoint_info["path"],
        "method": endpoint_info["method"],
        "description": endpoint_info["description"],
        "required_parameters": required_params,
        "optional_parameters": optional_params,
    }


@tool
def get_schema_examples(endpoint_name: str) -> dict[str, Any]:
    """Get example requests and responses for a Companies House API endpoint.

    This tool provides example request parameters and expected response structures
    for a specific endpoint, helping you understand how to use it.

    Args:
        endpoint_name: Name of the endpoint to get examples for (e.g., "search-companies")
    """
    logger.info(f"Getting examples for endpoint: {endpoint_name}")

    schema = load_schema()
    if not schema:
        return {"error": "Could not load API schema"}

    endpoints = get_endpoint_definitions()
    if endpoint_name not in endpoints:
        return {
            "error": f"Endpoint '{endpoint_name}' not found",
            "available_endpoints": list(endpoints.keys()),
        }

    endpoint_info = endpoints[endpoint_name]
    path = endpoint_info["path"]
    method = endpoint_info["method"].lower()

    # Extract examples from schema
    path_obj = schema.get("paths", {}).get(path, {})
    method_obj = path_obj.get(method, {})

    # Get example parameters
    example_params = {}
    for param in method_obj.get("parameters", []):
        if "example" in param:
            example_params[param["name"]] = param["example"]

    # Get example responses
    example_responses = {}
    for status_code, response in method_obj.get("responses", {}).items():
        example = None
        schema_obj = response.get("schema", {})

        # Try to find an example
        if "example" in schema_obj:
            example = schema_obj["example"]
        elif "examples" in response:
            example = response["examples"]

        if example:
            example_responses[status_code] = example

    return {
        "endpoint_name": endpoint_name,
        "path": path,
        "method": method.upper(),
        "example_parameters": example_params,
        "example_responses": example_responses,
    }
