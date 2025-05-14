#!/usr/bin/env python3

"""Model utility functions for Dude Diligence.

Provides model initialization and configuration for all agents in the system.
Johnny Bravo knows how to pick the best models, just like he picks the best hair gel!
"""

import logging
import os
# opentelemetry.trace is not strictly needed here anymore unless you add other custom spans
# from opentelemetry import trace 
# SmolagentsInstrumentor is not called from here anymore
# from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from smolagents import HfApiModel, OpenAIServerModel

# Set up logging
logger = logging.getLogger(__name__)

def get_agent_model():
    """Get the appropriate LLM model for the agent based on environment variables.

    Returns:
        An initialized model for the smolagents, with Johnny's stamp of approval
    """    
    # Check for OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        logger.info("Using OpenAI model for the agent - Johnny likes the smart ones!")
        
        model = OpenAIServerModel(
            model_id="gpt-4o", 
            temperature=0.2, 
            api_key=os.getenv("OPENAI_API_KEY")
        )
        return model

    # Fallback to Hugging Face model
    logger.info("Using Hugging Face model for the agent - Johnny says 'Hello, pretty Llama!'")
    
    model = HfApiModel(
        model_id="meta-llama/Llama-3.3-70B-Instruct", # Example, adjust if needed
        temperature=0.2,
    )
    return model
