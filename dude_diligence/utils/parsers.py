#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parsers for LLM responses and external API data."""

import json
import logging
from typing import Dict, Any, List, Optional, Union

logger = logging.getLogger(__name__)


def parse_response(
    response: str,
    expected_format: str = "json",
    fallback_to_text: bool = True
) -> Union[Dict[str, Any], List[Any], str]:
    """Parse a response from an LLM into the expected format.
    
    Args:
        response: The raw text response from the LLM
        expected_format: Expected format of the response ("json", "list", "text")
        fallback_to_text: Whether to return the raw text if parsing fails
        
    Returns:
        Parsed response in the requested format, or raw text if parsing fails
    """
    logger.debug("Parsing LLM response")
    
    if expected_format == "text":
        return response
    
    # Try to extract JSON from the response
    try:
        # Look for JSON-like content (between ```json and ```, or just {})
        json_content = response
        
        # Check if JSON is wrapped in code blocks
        if "```json" in response and "```" in response.split("```json", 1)[1]:
            json_content = response.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in response and "```" in response.split("```", 1)[1]:
            json_content = response.split("```", 1)[1].split("```", 1)[0].strip()
        
        # Parse the JSON content
        parsed_data = json.loads(json_content)
        
        # Validate format
        if expected_format == "json" and not isinstance(parsed_data, dict):
            raise ValueError("Expected a JSON object but got a different format")
        elif expected_format == "list" and not isinstance(parsed_data, list):
            raise ValueError("Expected a list but got a different format")
            
        return parsed_data
    
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"Failed to parse response as {expected_format}: {e}")
        
        if fallback_to_text:
            logger.info("Falling back to raw text response")
            return response
        
        raise


def extract_structured_data(text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    """Extract structured data from text based on a schema.
    
    This is a placeholder implementation. In a real implementation, this would likely
    use an LLM to extract data according to the schema.
    
    Args:
        text: The text to extract data from
        schema: The schema defining the expected structure
        
    Returns:
        Structured data extracted from the text
    """
    # Placeholder implementation
    return {} 