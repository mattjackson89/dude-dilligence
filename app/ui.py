# ruff: noqa: E501
"""Gradio interface for Dude Diligence.

Johnny Bravo's stylish UI for company research.
"""

import gradio as gr

from dude_diligence import run_due_diligence
from dude_diligence.agents import create_manager_agent

# Johnny's signature colors
JOHNNY_YELLOW = "#FFD700"
JOHNNY_BLACK = "#000000"
JOHNNY_BLUE = "#1E90FF"


class ReportContextAgent:
    """Wrapper around the agent to ensure report context is included with each interaction."""

    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.report = ""
        self.company_name = ""
        self.name = "Johnny Bravo"  # Add name attribute for GradioUI compatibility

    def set_report_context(self, report, company_name):
        """Set the report context for future interactions."""
        self.report = report
        self.company_name = company_name

    def run(self, user_message):
        """Run the agent with the report context included."""
        if not self.report:
            return "No report has been generated yet. Please run due diligence first."

        prompt = f"""
        You are Johnny Bravo, a charismatic and knowledgeable assistant who helps with company research.
        You have completed a due diligence report for {self.company_name}.

        Here is the report for context:
        {self.report}

        The user's question is: {user_message}

        Answer their question based on this report. If information isn't in the report,
        explain that it wasn't covered in the initial research but you can help look into it.

        Always maintain Johnny Bravo's confident and slightly flamboyant personality.
        """

        return self.base_agent.run(prompt)


def create_ui():
    """Create and return the Gradio UI interface.

    Returns:
        gr.Blocks: The Gradio interface
    """
    # Get the manager agent for the UI
    base_agent = create_manager_agent()
    # Wrap it to include context
    context_agent = ReportContextAgent(base_agent)

    # Create the UI
    with gr.Blocks(
        theme=gr.themes.Base(),
        css="""
        footer {visibility: hidden}
        .contain {height: 600px; overflow-y: auto;}
    """,
    ) as ui:
        # Header
        gr.HTML(
            f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h1 style="color: {JOHNNY_BLUE};">Dude Diligence</h1>
                <h3 style="color: {JOHNNY_BLACK};">Johnny Bravo's UK Company Research Tool</h3>
            </div>
            """
        )

        # Due Diligence Form
        with gr.Row():
            company_input = gr.Textbox(
                label="Company Name",
                placeholder="Enter UK company name (e.g., Tesla Motors UK)",
            )
            research_areas = gr.Textbox(
                label="Research Areas (comma-separated)",
                placeholder="Company Overview, Officers, Financial Status",
                value="Company Overview, Officers, Financial Status",
            )

        # Status indicator
        status_html = gr.HTML("")

        # Submit button
        submit_btn = gr.Button("Run Due Diligence", variant="primary")

        # Results section with report and chat side by side
        with gr.Row(visible=False) as results_row:
            # Report on left (75% width)
            with gr.Column(scale=3):
                gr.Markdown("## Due Diligence Report")
                report_output = gr.Markdown(elem_classes=["contain"])

            # Chat on right (25% width)
            with gr.Column(scale=1):
                gr.Markdown("## Chat with Johnny")
                # Built-in Gradio Chatbot component
                chatbot = gr.Chatbot(
                    height=500,
                    bubble_full_width=False,
                    show_copy_button=True,
                    avatar_images=(
                        None,
                        "https://www.clipartmax.com/png/middle/112-1127678_johnny-bravo-logo-png-transparent-johnny-bravo.png",
                    ),
                )
                chat_input = gr.Textbox(
                    placeholder="Ask Johnny about the report...", label="Your message"
                )
                clear_btn = gr.Button("Clear Chat")

        # Functions
        def start_processing():
            """Show that processing has started."""
            return """
            <div style="text-align: center; margin: 20px auto;">
                <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2RnbzZyOHB2Y2lrMGxzemR2YTlnMGJxa2t6cWw4ZHpyODQzY3B3NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1KUdeIpGxXAdi/giphy.gif"
                     alt="Johnny Bravo flexing"
                     width="150"
                     style="display: block; margin: 0 auto 15px auto;">
                <p style="color: #1E90FF; font-weight: bold; font-size: 18px;">
                    Johnny is flexing his research muscles... This might take a minute!
                </p>
            </div>
            """

        def run_due_diligence_report(company_name, research_areas_text):
            """Run the due diligence report and return results."""
            if not company_name:
                return (
                    "Hey there! I need a company name to flex my research muscles!",
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #FF4500; font-weight: bold;"> Please enter a company name</p>
                       </div>""",
                    gr.update(visible=False),
                    [],
                )

            research_areas = [
                area.strip() for area in research_areas_text.split(",") if area.strip()
            ]
            try:
                result = run_due_diligence(company_name, research_areas)

                # Set report context for the agent
                context_agent.set_report_context(result, company_name)

                # Create initial chat message
                initial_message = f"Hey there, hot stuff! I've just completed the due diligence on {company_name}. Ask me anything about it! *flexes muscles*"

                # Make results container visible
                return (
                    result,
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #008000; font-weight: bold;"> Report generated successfully!</p>
                       </div>""",
                    gr.update(visible=True),
                    [[None, initial_message]],
                )
            except Exception as e:
                return (
                    f"Whoops! Johnny couldn't complete the research: {str(e)}",
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #FF4500; font-weight: bold;"> There was an error generating the report</p>
                       </div>""",
                    gr.update(visible=False),
                    [],
                )

        def respond_to_chat(message, chat_history):
            """Process a chat message and return Johnny's response."""
            if message.strip() == "":
                return "", chat_history

            # Get response from our context-aware agent
            response = context_agent.run(message)

            # Update chat history
            chat_history.append([message, response])

            return "", chat_history

        def clear_chat_history():
            """Clear the chat history."""
            company_name = context_agent.company_name or "the company"
            initial_message = f"Hey there, hot stuff! I've just completed the due diligence on {company_name}. Ask me anything about it! *flexes muscles*"
            return [[None, initial_message]]

        # Connect UI components
        submit_btn.click(fn=start_processing, inputs=None, outputs=status_html).then(
            fn=run_due_diligence_report,
            inputs=[company_input, research_areas],
            outputs=[report_output, status_html, results_row, chatbot],
        )

        # Handle chat interactions
        chat_input.submit(
            fn=respond_to_chat, inputs=[chat_input, chatbot], outputs=[chat_input, chatbot]
        )

        # Clear chat button
        clear_btn.click(fn=clear_chat_history, inputs=None, outputs=chatbot)

    return ui
