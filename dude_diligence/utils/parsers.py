#!/usr/bin/env python3

"""Parsers for LLM responses and external API data."""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def parse_response(
    response: str
) -> dict[str, Any] | list[Any] | str:
    """Parse a response from an LLM into the expected format.

    Args:
        response: The raw text response from the LLM

    Returns:
        Parsed response in the requested format, or raw text if parsing fails
    """
    logger.debug("Parsing LLM response")

    # Look for JSON-like content (between ```json and ```, or just {})
    json_content = response

    # Check if JSON is wrapped in code blocks
    if "```json" in response and "```" in response.split("```json", 1)[1]:
        json_content = response.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in response and "```" in response.split("```", 1)[1]:
        json_content = response.split("```", 1)[1].split("```", 1)[0].strip()

    # Parse the JSON content
    parsed_data = json.loads(json_content)
    return parsed_data
