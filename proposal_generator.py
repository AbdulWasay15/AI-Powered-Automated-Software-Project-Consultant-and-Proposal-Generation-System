import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use central gemini configuration and model chooser
from gemini_config import get_gemini_model
model = get_gemini_model()


def generate_project_proposal(project_data):
    """
    Generate Software Project Proposal using Gemini AI
    """

    try:

        client_name = project_data.get("client_name", "")
        project_name = project_data.get("project_name", "")
        project_type = project_data.get("project_type", "")
        budget = project_data.get("budget", "")
        timeline = project_data.get("timeline", "")
        features = project_data.get("features", "")

        prompt = f"""
        You are a professional Software Business Analyst and Proposal Writer.

        Generate a professional software project proposal using the following information.

        CLIENT INFORMATION

        Client Name: {client_name}

        PROJECT INFORMATION

        Project Name: {project_name}

        Project Type: {project_type}

        Budget: {budget}

        Timeline: {timeline}

        Required Features:
        {features}

        Generate a professional proposal with the following sections:

        1. Project Title

        2. Introduction

        3. Project Objectives

        4. Project Scope

        5. Key Features

        6. Proposed Technology Stack

        7. Development Methodology

        8. Estimated Timeline

        9. Estimated Budget

        10. Deliverables

        11. Conclusion

        Requirements:
        - Professional tone
        - Clear headings
        - Easy to understand
        - Suitable for software development clients
        - Do not use markdown symbols
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Proposal Generation Error: {str(e)}"


def generate_simple_proposal(project_name, budget, timeline, features):
    """
    Backup Proposal Generator
    If Gemini API fails
    """

    proposal = f"""
PROJECT TITLE

{project_name}

INTRODUCTION

This proposal outlines the development plan for the {project_name} project.
The objective is to design and develop a high-quality software solution
that meets the client's business requirements.

PROJECT OBJECTIVES

- Develop a reliable software solution
- Improve operational efficiency
- Deliver a user-friendly experience
- Ensure scalability and security

KEY FEATURES

{features}

ESTIMATED TIMELINE

{timeline}

ESTIMATED BUDGET

{budget}

CONCLUSION

The proposed solution will be developed according to the provided
requirements while maintaining quality, performance, and usability.
"""

    return proposal