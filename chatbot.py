import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use central gemini configuration and model chooser
from gemini_config import get_gemini_model

model = get_gemini_model()


def get_chat_response(user_message):
    """
    AI Software Project Consultant Chatbot
    """

    try:

        prompt = f"""
        You are an AI-Powered Software Project Consultant.

        Your responsibility is to help clients gather software project requirements.

        Ask relevant questions related to:

        - Project Name
        - Project Type
        - Budget
        - Timeline
        - Target Users
        - Required Features
        - Technology Preferences

        Rules:
        1. Keep responses short and professional.
        2. Ask one or two questions at a time.
        3. Guide the client step-by-step.
        4. If enough information is collected, tell the client they can generate the proposal.
        5. Focus only on software development projects.

        Client Message:
        {user_message}
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"


def get_welcome_message():
    """
    Initial chatbot message
    """

    return """
Hello! 👋

I am your AI Software Project Consultant.

I can help you gather project requirements and generate a professional software project proposal.

Let's start.

What is the name of your project?
"""