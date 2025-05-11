#!/usr/bin/env python3

"""Utility functions for Companies House API integration.

Helper functions to manage Companies House API schemas, endpoints, and parsing.
Johnny says, "Knowledge is power, and this schema's got the muscle!"
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Path to the Companies House API schema
SCHEMA_PATH = Path(__file__).parent.parent / "specs" / "companies_house_api.json"


def load_schema() -> Optional[Dict[str, Any]]:
    """Load the Companies House API schema from the specs directory.

    Returns:
        Dictionary containing the API schema if loaded successfully, None otherwise
    """
    try:
        logger.debug(f"Loading Companies House API schema from {SCHEMA_PATH}")
        
        if not SCHEMA_PATH.exists():
            logger.error(f"Schema file not found at {SCHEMA_PATH}")
            return None
            
        with open(SCHEMA_PATH, "r") as f:
            schema = json.load(f)
            
        logger.debug("Companies House API schema loaded successfully")
        return schema
        
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to load Companies House API schema: {e}")
        return None


def get_endpoint_definitions() -> Dict[str, Any]:
    """Extract endpoint definitions from the Companies House API schema.

    This function parses the OpenAPI schema for Companies House and extracts
    a simplified representation of the available endpoints.

    Returns:
        Dictionary mapping endpoint names to their definitions
    """
    schema = load_schema()
    if not schema:
        logger.error("Could not load schema for endpoint definitions")
        return {}
        
    endpoints = {}
    
    # Extract paths and their operations
    for path, path_obj in schema.get("paths", {}).items():
        # For each HTTP method in the path
        for method, method_obj in path_obj.items():
            if method not in ("get", "post", "put", "delete"):
                continue
                
            # If it's a reference, just use the last part of the path as the name
            if "$ref" in method_obj:
                ref_path = method_obj["$ref"]
                
                # Create a simplified name based on the path
                # Strip any leading/trailing slashes and replace internal ones with dashes
                path_name = path.strip("/").replace("/", "-")
                endpoint_name = f"{method}-{path_name}"
                
                # Get the operation from the reference if possible
                operation_name = ref_path.split("/")[-1].split("#")[-1]
                if operation_name and operation_name != "":
                    endpoint_name = operation_name
                
                # Store the endpoint info
                endpoints[endpoint_name] = {
                    "path": path,
                    "method": method.upper(),
                    "description": f"{method.upper()} {path}",
                    "parameters": [],  # We don't have detailed info for references
                }
            else:
                # It's a direct operation definition
                operation_id = method_obj.get("operationId", "")
                if not operation_id:
                    # Create a name from the path if no operationId
                    path_name = path.strip("/").replace("/", "-")
                    operation_id = f"{method}-{path_name}"
                
                # Store the endpoint info
                endpoints[operation_id] = {
                    "path": path,
                    "method": method.upper(),
                    "description": method_obj.get("summary", "") or method_obj.get("description", ""),
                    "parameters": method_obj.get("parameters", []),
                }
    
    logger.debug(f"Extracted {len(endpoints)} endpoint definitions from Companies House API schema")
    return endpoints 