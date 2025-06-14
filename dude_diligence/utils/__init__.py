"""Utility functions for Dude Diligence.

Johnny's accessories to make due diligence look good.
"""

import logging

from dude_diligence.utils.parsers import parse_response
from dude_diligence.utils.prompts import (
    MANAGER_AGENT_PROMPT,
)


def setup_logging(logger_name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """Set up logging with consistent formatting across the application.

    Args:
        logger_name: Optional name for the logger, uses root logger if None
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create a formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Check if any handlers already exist
    if not logger.handlers:
        # Add a console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


__all__ = [
    "MANAGER_AGENT_PROMPT",
    "parse_response",
    "setup_logging",
]
