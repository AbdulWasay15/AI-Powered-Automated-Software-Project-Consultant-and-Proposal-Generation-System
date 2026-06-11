from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session
)

from dotenv import load_dotenv
import secrets

from gemini_config import get_gemini_model
from proposal_generator import generate_simple_proposal
from pdf_generator import create_proposal_pdf

# Load Environment Variables
load_dotenv()

# Gemini Model
model = get_gemini_model()

# Flask App
app = Flask(__name__)

# Session Key (Required For Memory)
app.secret_key = secrets.token_hex(16)


# ==========================================
# HOME PAGE
# ==========================================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# AI CHATBOT WITH MEMORY
# ==========================================
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get(
            "message",
            ""
        )

        # Create memory
        if "chat_history" not in session:
            session["chat_history"] = []

        chat_history = session["chat_history"]

        # Store user message
        chat_history.append(
            f"User: {user_message}"
        )

        # Keep last 10 messages only
        chat_history = chat_history[-10:]

        conversation_context = "\n".join(
            chat_history
        )

        prompt = f"""
        You are an AI Software Project Consultant.

        Your job is to collect complete
        software project requirements.

        Previous Conversation:
        {conversation_context}

        Latest User Message:
        {user_message}

        Collect:
        - Project Name
        - Project Type
        - Budget
        - Timeline
        - Features
        - Technologies

        Rules:
        - Ask one question at a time.
        - Remember previous answers.
        - Be professional.
        - If enough details are collected,
          tell the client they can generate
          the proposal.
        """

        response = model.generate_content(
            prompt
        )

        bot_reply = response.text

        # Save bot reply in memory
        chat_history.append(
            f"Assistant: {bot_reply}"
        )

        session["chat_history"] = chat_history

        return jsonify({
            "reply": bot_reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })


# ==========================================
# CLEAR CHAT MEMORY
# ==========================================
@app.route("/clear_chat", methods=["POST"])
def clear_chat():

    session.pop(
        "chat_history",
        None
    )

    return jsonify({
        "success": True
    })


# ==========================================
# PROPOSAL GENERATOR
# ==========================================
@app.route("/generate_proposal", methods=["POST"])
def generate_proposal():

    try:

        data = request.get_json()

        client_name = data.get(
            "client_name",
            ""
        )

        project_name = data.get(
            "project_name",
            "Proposal"
        )

        project_type = data.get(
            "project_type",
            ""
        )

        budget = data.get(
            "budget",
            ""
        )

        timeline = data.get(
            "timeline",
            ""
        )

        features = data.get(
            "features",
            ""
        )

        proposal_prompt = f"""
        Generate a professional
        software project proposal.

        Client Name:
        {client_name}

        Project Name:
        {project_name}

        Project Type:
        {project_type}

        Budget:
        {budget}

        Timeline:
        {timeline}

        Features:
        {features}

        Include:

        1. Project Title
        2. Introduction
        3. Objectives
        4. Scope
        5. Features
        6. Technology Stack
        7. Timeline
        8. Budget
        9. Deliverables
        10. Conclusion

        Use a professional tone.
        """

        try:

            response = model.generate_content(
                proposal_prompt
            )

            proposal_text = response.text

        except Exception:

            proposal_text = (
                generate_simple_proposal(
                    project_name,
                    budget,
                    timeline,
                    features
                )
            )

            proposal_text += (
                "\n\n[Notice: AI service unavailable — Local Proposal Used]"
            )

        # Generate PDF
        pdf_file = create_proposal_pdf(
            proposal_text,
            project_name
        )

        return jsonify({
            "proposal": proposal_text,
            "pdf_url":
            f"/static/generated_pdfs/{pdf_file}"
        })

    except Exception as e:

        return jsonify({
            "proposal":
            f"Error: {str(e)}"
        })


# ==========================================
# RUN APPLICATION
# ==========================================
if __name__ == "__main__":

    app.run(
        debug=True
    )

