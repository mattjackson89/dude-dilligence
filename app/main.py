"""Entry point for the Dude Diligence Gradio application.

As Johnny Bravo would say: "Enough talk, let's launch this app, baby!"
"""

import logging

from app.ui import create_ui

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Launch the Gradio interface.

    Johnny Bravo style entrance to the web app.
    """
    logger.info("Hey there, pretty user! Launching Dude Diligence...")

    ui = create_ui()
    ui.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )

    logger.info("Dude Diligence is ready to flex those research muscles!")


if __name__ == "__main__":
    main()


