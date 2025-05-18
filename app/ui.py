# ruff: noqa: E501
"""Gradio interface for Dude Diligence.

Johnny Bravo's stylish UI for company research.
"""

import gradio as gr
import uuid
import logging
import markdown
from pathlib import Path

from dude_diligence import run_due_diligence
from dude_diligence.agents import create_manager_agent

# Johnny's signature colors
JOHNNY_YELLOW = "#FFD700"
JOHNNY_BLACK = "#000000"
JOHNNY_BLUE = "#1E90FF"

logger = logging.getLogger(__name__)


class ReportContextAgent:
    """Wrapper around the agent to ensure report context is included with each interaction."""

    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.report_markdown = ""
        self.report_raw = None
        self.company_name = ""
        self.name = "Johnny Bravo"  # Add name attribute for GradioUI compatibility
        self.session_id = str(uuid.uuid4())

    def set_report_context(self, report_markdown, company_name):
        """Set the report context for future interactions."""
        self.report_markdown = report_markdown
        self.company_name = company_name

    def run(self, user_message):
        """Run the agent with the report context included."""
        if not self.report_markdown:
            return "No report has been generated yet. Please run due diligence first."

        from opentelemetry import trace
        tracer = trace.get_tracer("due-diligence-tracing")
        with tracer.start_as_current_span("Agent-Chat-Interaction") as span:
            # Add attributes to the trace that match our due diligence naming pattern
            span.set_attribute("langfuse.session.id", self.session_id)
            span.set_attribute("langfuse.tags", ["chat", "johnny-bravo"])
            span.set_attribute("company.name", self.company_name)
            
            # Add input/output attributes for consistency with Due-Diligence-Process
            span.set_attribute("input.value", user_message)

            prompt = f"""
            You are Johnny Bravo, a charismatic, confident, and slightly narcissistic cartoon character who's now an expert in company due diligence.

            You have completed a due diligence report for {self.company_name} and you're ready to flex your knowledge muscles.

            HERE'S THE REPORT CONTEXT (read this carefully, it's as important as my hair):
            {self.report_markdown}

            The user's question is: {user_message}

            First, determine if you can answer the question using ONLY the existing report.
            If the information is in the report:
            - Answer the question directly using that information
            - Format your response in Johnny Bravo's distinctive style:
              * Use catchphrases like "Hey there, pretty data!", "Oh mama!", and "Man, I'm pretty!"
              * Frequently reference your good looks, muscles, and hair
              * Add "*does hair flip*" or "*strikes pose*" action markers when presenting important information
              * Speak in confident, punchy sentences with lots of enthusiasm
              * Always maintain your swagger while providing accurate information

            If the information is NOT in the report, use your available tools to find it:
            - Use the finder_agent to search for web-based information
            - Use the companies_house_agent to retrieve official registry data
               
            After using any tools, analyze the results and provide a helpful answer with Johnny Bravo's unique flair.
            """

            try:
                response = self.base_agent.run(prompt)
                # Add output attributes like in due diligence
                span.set_attribute("status", "success")
                span.set_attribute("output.value", response)
                return response
            except Exception as e:
                # Record error in trace
                span.set_attribute("status", "error") 
                span.set_attribute("error.message", str(e))
                # Log the error
                logger.error(f"Error in chat interaction: {str(e)}")
                # Return an error message
                return f"Whoops! Something went wrong. Can you try asking differently?"


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
        /* Base styling */
        footer {visibility: hidden}
        
        /* Define a spacing system */
        :root {
            --spacing-xs: 0.25rem;
            --spacing-sm: 0.5rem;
            --spacing-md: 1rem;
            --spacing-lg: 2rem;
            --spacing-xl: 3rem;
        }
        
        /* Typography improvements */
        body {
            line-height: 1.6;
            letter-spacing: 0.01em;
        }
        h1, h2, h3 { 
            letter-spacing: -0.02em; 
        }
        
        /* Button enhancements */
        button {
            transition: transform 0.1s, box-shadow 0.1s;
        }
        button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        button:active {
            transform: translateY(1px);
        }
        
        /* Form focus states */
        input:focus, textarea:focus {
            border-color: #1E90FF !important;
            box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.25) !important;
            outline: none !important;
        }
        
        /* Loading animation */
        .loading { 
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        
        /* Scrollbar customization */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: #888; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #555; }
        
        /* Responsive design for recommendation section */
        @media (max-width: 768px) {
            div[style*="display: flex"] {
                flex-direction: column !important;
            }
            div[style*="flex: 1"] {
                text-align: center !important;
                margin-top: var(--spacing-md);
            }
        }
        
        /* Enhance chatbot UI */
        [data-testid="chatbot"] {
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        /* List item styling */
        ul li {
            margin-bottom: var(--spacing-xs);
            position: relative;
        }
        
        /* Card-like effect for report sections */
        .gradio-html {
            border-radius: 8px;
            overflow: hidden;
            transition: box-shadow 0.3s ease;
        }
        .gradio-html:hover {
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Animation for new content */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out forwards;
        }
        """,
    ) as ui:
        # Set the absolute path to your images directory
        image_dir = Path.cwd() / "app" / "images"
        gr.set_static_paths([image_dir])
        
        # Header
        gr.HTML(
            f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h1 style="color: {JOHNNY_BLUE};">Dude Diligence</h1>
                <h3 style="color: {JOHNNY_YELLOW};">Johnny Bravo's UK Company Research Tool</h3>
            </div>
            """
        )

        # Due Diligence Form
        with gr.Row():
            company_input = gr.Textbox(
                label="Company Name",
                placeholder="Enter UK company name (e.g., Tesla Motors UK)",
            )

        # Status indicator
        status_html = gr.HTML("")

        # Submit button
        submit_btn = gr.Button("Run Due Diligence", variant="primary")

        # Results section with report and chat side by side
        with gr.Row(visible=False) as results_row:
            # Report on left (75% width)
            with gr.Column(scale=3):
                # Add new recommendation section first
                gr.Markdown("## Johnny's Recommendation")
                recommendation_output = gr.HTML(value="")

                # Add details section
                gr.Markdown("## Due Diligence Report")
                report_output = gr.HTML()

                # Add JSON expander
                with gr.Accordion("Raw Report Data", open=False):
                    json_output = gr.JSON(label="Report Data")

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
                <p style="color: #1E90FF; font-weight: bold; font-size: 18px;" class="loading">
                    Johnny is flexing his research muscles... This might take a minute!
                </p>
            </div>
            """

        def run_due_diligence_report(company_name):
            """Run the due diligence report and return results."""
            if not company_name:
                return (
                    "Hey there! I need a company name to flex my research muscles!",
                    "",
                    None,
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #FF4500; font-weight: bold;"> Please enter a company name</p>
                       </div>""",
                    gr.update(visible=False),
                    [],
                    None,
                )

            try:
                logger.info(f"Starting due diligence for company: {company_name}")
                parsed_result = run_due_diligence(company_name)
                logger.info("Due diligence completed successfully")
                
                # Extract components
                report_markdown = parsed_result["report"]
                recommendation_data = parsed_result["recommendation"]
                image_name = parsed_result["image"]
                
                # Format recommendation with strengths and risks
                formatted_recommendation = f"""
                <div style="display: flex; align-items: flex-start; gap: 2rem;" class="animate-fade-in">
                    <div style="color: {JOHNNY_BLUE}; font-size: 1.1em; line-height: 1.5; padding: 1rem; border-left: 4px solid {JOHNNY_BLUE}; background-color: rgba(30, 144, 255, 0.1); flex: 2;">
                        <h3 style="color: {JOHNNY_BLUE}; margin-top: 0;">Overall Assessment</h3>
                        {recommendation_data['overall_assessment']}
                        
                        <h4 style="color: {JOHNNY_BLUE}; margin-top: 1rem;">Key Strengths</h4>
                        <ul>
                            {''.join(f'<li>{strength}</li>' for strength in recommendation_data['key_strengths'])}
                        </ul>
                        
                        <h4 style="color: {JOHNNY_BLUE}; margin-top: 1rem;">Key Risks</h4>
                        <ul>
                            {''.join(f'<li>{risk}</li>' for risk in recommendation_data['key_risks'])}
                        </ul>
                        
                        <h4 style="color: {JOHNNY_BLUE}; margin-top: 1rem;">Final Recommendation</h4>
                        {recommendation_data['final_recommendation']}
                    </div>
                    <div style="flex: 1; text-align: left;">
                        <img src='/gradio_api/file=app/images/{image_name}' alt='A gif representing Johnny's feelings' style='max-width: 150px; border-radius: 8px;'/>
                        <div style="font-size: 0.9em; color: #888; margin-top: 0.5em;">Johnny's Reaction</div>
                    </div>
                </div>
                """

                # Convert markdown to HTML and then wrap in styled container
                report_html = markdown.markdown(report_markdown)
                formatted_report = f"""
                <div style="color: {JOHNNY_YELLOW}; font-size: 1.1em; line-height: 1.5; padding: 1rem; border-left: 4px solid {JOHNNY_YELLOW}; background-color: rgba(255, 215, 0, 0.1);" class="animate-fade-in">
                    {report_html}
                </div>
                """
                
                # Set the report context for chat
                context_agent.set_report_context(report_markdown, company_name)
                logger.info("Successfully set report context")

                # Create initial chat message
                initial_message = f"Hey there, hot stuff! I've just completed the due diligence on {company_name}. Ask me anything about it! *flexes muscles*"

                # Make results container visible
                return (
                    formatted_report,
                    formatted_recommendation,
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #008000; font-weight: bold;"> Report generated successfully!</p>
                       </div>""",
                    gr.update(visible=True),
                    [[None, initial_message]],
                    parsed_result,
                )
            except Exception as e:
                logger.error(f"Error in run_due_diligence_report: {str(e)}", exc_info=True)
                return (
                    f"Whoops! Johnny couldn't complete the research: {str(e)}",
                    "",
                    None,
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #FF4500; font-weight: bold;"> There was an error generating the report</p>
                       </div>""",
                    gr.update(visible=False),
                    [],
                    None,
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
            inputs=[company_input],
            outputs=[report_output, recommendation_output, status_html, results_row, chatbot, json_output],
        )

        # Handle chat interactions
        chat_input.submit(
            fn=respond_to_chat, inputs=[chat_input, chatbot], outputs=[chat_input, chatbot]
        )

        # Clear chat button
        clear_btn.click(fn=clear_chat_history, inputs=None, outputs=chatbot)

    return ui
