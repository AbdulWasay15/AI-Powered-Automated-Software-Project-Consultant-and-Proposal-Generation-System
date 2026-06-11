import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check API Key
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


def choose_model():
    """Choose a supported model dynamically.

    Priority:
    1. Use `GEMINI_MODEL` env var if provided and valid.
    2. Otherwise list available models and pick the first one that
       supports `generateContent`.
    """

    env_model = os.getenv("GEMINI_MODEL")
    # Try env model first
    if env_model:
        try:
            m = genai.GenerativeModel(env_model)
            # quick smoke test (do not send user-visible requests)
            return m
        except Exception:
            pass

    # Fallback: list models and pick one that supports generateContent
    try:
        for mdl in genai.list_models():
            methods = getattr(mdl, "supported_generation_methods", []) or []
            if "generateContent" in methods or "generateMessage" in methods:
                try:
                    return genai.GenerativeModel(mdl.name)
                except Exception:
                    # try without prefix
                    try:
                        return genai.GenerativeModel(mdl.base_model_id)
                    except Exception:
                        continue
    except Exception:
        # If listing models fails, re-raise later when model is used.
        return None


_MODEL = choose_model()


def get_gemini_model():
    """Return the chosen GenerativeModel instance or raise if unavailable."""
    if _MODEL is None:
        raise RuntimeError("No available Gemini model found. Check your API key and account.")
    return _MODEL


def test_connection():
    try:
        m = get_gemini_model()
        _ = m.generate_content("Hello")
        return {"success": True, "message": "Gemini API Connected Successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}