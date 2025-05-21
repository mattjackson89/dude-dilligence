# Dude Diligence Tools

*"Hey there, Pretty APIs! Let me access your data!"* - Johnny Bravo

This directory contains the specialized tools and API integrations used by the Dude Diligence agents to gather company information.

## Available Tools

### Companies House API (`companies_house.py`)

Functions for accessing the UK's official company registry:

- `search_companies`: Search for companies by name
- `get_company_profile`: Get detailed company profile by company number
- `get_company_officers`: Get directors and officers
- `get_filing_history`: Get company filing history
- `get_persons_with_significant_control`: Get PSCs (owners)
- `get_charges`: Get secured loans and charges
- `perform_company_due_diligence`: Run a complete due diligence process on a UK company

### Authentication

These tools require a Companies House API key, which should be set in the `COMPANIES_HOUSE_API_KEY` environment variable.

You can obtain an API key from:
https://developer.company-information.service.gov.uk/

## Example Usage

Basic usage with the Companies House API:

```python
from dude_diligence.tools.companies_house import search_companies, get_company_profile

# Search for a company
search_results = search_companies("Tesla")

# Get a company's profile
if search_results:
    company_number = search_results[0]["company_number"]
    profile = get_company_profile(company_number)
    print(f"Company Name: {profile['company_name']}")
    print(f"Status: {profile['company_status']}")
```

## API Response Models

All API responses are parsed into consistent Python dictionaries that maintain the original structure from Companies House.

For example, a company profile response will include:
- Company name
- Company number
- Status
- Type
- Creation date
- Registered address
- SIC codes
- And more...

## Error Handling

All tools include proper error handling for:
- Authentication failures
- Rate limiting
- Company not found
- Invalid inputs
- Network errors

Errors are raised as exceptions with descriptive messages. 