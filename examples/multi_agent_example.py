"""Example script demonstrating the multi-agent due diligence system.

This example shows how to use the multi-agent architecture for
company due diligence with specialized agents.
"""

import logging
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dude_diligence import run_due_diligence, visualize_agent_structure

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_api_key():
    """Check if the Companies House API key is set."""
    api_key = os.getenv("COMPANIES_HOUSE_API_KEY")
    if not api_key:
        logger.error("COMPANIES_HOUSE_API_KEY environment variable not set")
        print("\nERROR: Please set the COMPANIES_HOUSE_API_KEY environment variable")
        print("You can get an API key from https://developer.company-information.service.gov.uk/")
        print("\nExample: export COMPANIES_HOUSE_API_KEY=your_api_key_here")
        sys.exit(1)
    return api_key


def check_openai_api_key():
    """Check if the OpenAI API key is set."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        print("\nWARNING: OPENAI_API_KEY environment variable not set")
        print("The system will fall back to Hugging Face models, which may be slower")
        print("\nExample: export OPENAI_API_KEY=your_api_key_here")
    return api_key


def visualize_multi_agent_structure():
    """Visualize the multi-agent structure without running a task."""
    print("\n=== Multi-Agent Structure Visualization ===\n")

    visualize_agent_structure()

    print("\nVisualization complete. The structure shows how multiple specialized agents")
    print("work together under the coordination of a manager agent.")


def run_example():
    """Run a multi-agent due diligence example."""
    print("\n=== Running Multi-Agent Due Diligence ===\n")

    # Example UK company to research
    company_name = "Scrubmarine"
    research_areas = ["Company Overview", "Officers", "Financial Status"]

    print(f"Starting multi-agent due diligence for '{company_name}'...")
    print(f"Research areas: {', '.join(research_areas)}")
    print("\nThis will use multiple specialized agents:")
    print("1. Finder Agent: To locate and identify the company")
    print("2. Companies House Agent: To retrieve official company data")
    print("3. Additional Research Agent: Placeholder for future capabilities")
    print("4. Manager Agent: To coordinate and compile findings")

    print("\nRunning multi-agent process (this may take a few minutes)...")

    # Run the multi-agent due diligence
    # Note: research_areas are determined internally by the agent system
    report = run_due_diligence(company_name)

    print("\n=== Multi-Agent Due Diligence Report ===\n")
    print(report)


if __name__ == "__main__":
    # Check if the API keys are set
    check_api_key()
    check_openai_api_key()

    print("Multi-Agent Due Diligence System Example")
    print("---------------------------------------\n")

    # First, visualize the multi-agent structure
    visualize_multi_agent_structure()

    # Ask if the user wants to run the full example
    response = input("\nDo you want to run the full multi-agent due diligence example? (y/n): ")

    if response.lower() in ["y", "yes"]:
        run_example()
    else:
        print("\nSkipping the full example. You can run it later by running this script again.")

    print("\nExample complete!")
