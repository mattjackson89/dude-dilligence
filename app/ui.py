"""Gradio interface for Dude Diligence.

Johnny Bravo's stylish UI for company research.
"""

from smolagents import GradioUI

from dude_diligence.agents import create_manager_agent

# Johnny's signature colors
JOHNNY_YELLOW = "#FFD700"
JOHNNY_BLACK = "#000000"
JOHNNY_BLUE = "#1E90FF"


def create_ui():
    """Create and return the Gradio UI interface.

    Johnny Bravo's slick and stylish interface for due diligence.

    Returns:
        gr.Blocks: The Gradio interface
    """
    # Get the manager agent for the UI
    agent = create_manager_agent()

    # Create the smolagents GradioUI
    ui = GradioUI(
        agent,
    )

    return ui
