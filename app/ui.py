"""Gradio interface for Dude Diligence.

Johnny Bravo's stylish UI for company research.
"""

import gradio as gr
from smolagents import GradioUI

from dude_diligence.agents import create_manager_agent
from dude_diligence import run_due_diligence

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
    
    # Store the report for context in subsequent chat
    report_state = gr.State("")
    company_state = gr.State("")
    
    with gr.Blocks(theme=gr.themes.Base(), css="footer {visibility: hidden}") as ui:
        # Header
        gr.HTML(
            f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h1 style="color: {JOHNNY_BLUE};">Dude Diligence</h1>
                <h3 style="color: {JOHNNY_BLACK};">Johnny Bravo's UK Company Research Tool</h3>
            </div>
            """
        )
        
        # Due Diligence Form (initially visible)
        with gr.Group(visible=True) as dd_section:
            gr.HTML("<h2>Run Due Diligence Report</h2>")
            with gr.Row():
                with gr.Column():
                    company_input = gr.Textbox(
                        label="Company Name",
                        placeholder="Enter UK company name (e.g., Tesla Motors UK)",
                    )
                    research_areas = gr.Textbox(
                        label="Research Areas (comma-separated)",
                        placeholder="Company Overview, Officers, Financial Status",
                        value="Company Overview, Officers, Financial Status"
                    )
                    
                    # Status indicator for the report generation
                    status_html = gr.HTML("")
                    
                    run_button = gr.Button("Run Due Diligence", variant="primary")
                
                with gr.Column():
                    report_output = gr.Markdown(label="Report")
                    chat_button = gr.Button("Discuss this report with Johnny", visible=False)
        
        # Chat Section (initially hidden)
        with gr.Group(visible=False) as chat_section:
            # Create a chat interface without displaying it yet
            gr.HTML("<h2>Chat with Johnny about the report</h2>")
            
            # We'll create a custom chat interface since we can't directly manipulate GradioUI
            chatbot = gr.Chatbot(height=500)
            msg = gr.Textbox(
                placeholder="Ask me anything about the report...",
                label="Your Message"
            )
            clear = gr.Button("Clear Chat")
            
            # Initialize with the report summary
            report_summary = gr.Markdown()
        
        # Functions for the UI
        def start_processing():
            """Show that processing has started."""
            return """
            <div style="text-align: center; margin-top: 10px;">
                <p style="color: #1E90FF; font-weight: bold;">
                    <img src="https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif" alt="loading" width="20" height="20" style="vertical-align: middle;"> 
                    Johnny is flexing his research muscles... This might take a minute!
                </p>
            </div>
            """
        
        def run_due_diligence_report(company_name, research_areas_text):
            """Run the due diligence report and store it for context."""
            if not company_name:
                return (
                    "Hey there! I need a company name to flex my research muscles!", 
                    "", 
                    company_name, 
                    False,
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #FF4500; font-weight: bold;">❌ Please enter a company name</p>
                       </div>"""
                )
            
            research_areas = [area.strip() for area in research_areas_text.split(",") if area.strip()]
            try:
                result = run_due_diligence(company_name, research_areas)
                
                # Clear the status and make the chat button visible
                return (
                    result, 
                    result, 
                    company_name, 
                    True,
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #008000; font-weight: bold;">✅ Report generated successfully!</p>
                       </div>"""
                )
            except Exception as e:
                return (
                    f"Whoops! Johnny couldn't complete the research: {str(e)}", 
                    "", 
                    company_name, 
                    False,
                    """<div style="text-align: center; margin-top: 10px;">
                       <p style="color: #FF4500; font-weight: bold;">❌ There was an error generating the report</p>
                       </div>"""
                )
        
        def prepare_chat(report, company):
            """Prepare the chat interface with the report context."""
            summary = f"## Due Diligence Report for {company}\n\nI've completed a full report on {company}. You can ask me specific questions about it now!"
            return True, False, summary, [[None, f"Hey there! I've completed the due diligence report for {company}. What would you like to know about it?"]]
        
        def chat(message, history, report):
            """Process chat messages with report context."""
            # Add user message to history
            history.append([message, None])
            
            # Prepare prompt with context from the report
            prompt = f"""
            The user is asking about a company due diligence report. Here's the report for context:
            
            {report}
            
            Their question is: {message}
            
            Answer their question based on the information in the report. If the information isn't in the report,
            you can explain that it wasn't covered in the initial research but you can help look into it.
            """
            
            # Get response from agent
            response = agent.run(prompt)
            
            # Update history with assistant response
            history[-1][1] = response
            return history
        
        def clear_chat(report, company):
            """Clear the chat history but keep context."""
            summary = f"## Due Diligence Report for {company}\n\nI've completed a full report on {company}. You can ask me specific questions about it now!"
            return summary, [[None, f"Hey there! I've completed the due diligence report for {company}. What would you like to know about it?"]]
            
        # Connect UI components
        run_button.click(
            fn=start_processing,
            inputs=None,
            outputs=status_html
        ).then(
            fn=run_due_diligence_report,
            inputs=[company_input, research_areas],
            outputs=[report_output, report_state, company_state, chat_button, status_html]
        )
        
        chat_button.click(
            fn=prepare_chat,
            inputs=[report_state, company_state],
            outputs=[chat_section, dd_section, report_summary, chatbot]
        )
        
        msg.submit(
            fn=chat,
            inputs=[msg, chatbot, report_state],
            outputs=[chatbot]
        ).then(
            lambda: "",
            None,
            msg
        )
        
        clear.click(
            fn=clear_chat,
            inputs=[report_state, company_state],
            outputs=[report_summary, chatbot]
        )
    
    return ui
