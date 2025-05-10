"""Utility functions for Dude Diligence.

Johnny's accessories to make due diligence look good.
"""

from dude_diligence.utils.prompts import SYSTEM_PROMPT, REPORT_TEMPLATE, EXTRACT_INFO_TEMPLATE
from dude_diligence.utils.parsers import parse_response, extract_structured_data

__all__ = [
    "SYSTEM_PROMPT", 
    "REPORT_TEMPLATE", 
    "EXTRACT_INFO_TEMPLATE",
    "parse_response",
    "extract_structured_data"
] 