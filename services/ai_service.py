import os
import streamlit as st
import google.generativeai as genai


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

def get_api_key():
    """
    Get Gemini API key from Streamlit secrets first,
    then environment variable.
    """

    api_key = None

    try:
        api_key = st.secrets.get("API_KEY")
    except Exception:
        pass

    if not api_key:
        api_key = os.environ.get("API_KEY")

    if not api_key:
        raise RuntimeError(
            "Gemini API key is not configured. "
            "Add API_KEY to Streamlit Secrets."
        )

    return api_key


# =========================================================
# GEMINI MODEL
# =========================================================

@st.cache_resource
def get_ai_model():

    api_key = get_api_key()

    genai.configure(
        api_key=api_key
    )

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    return model


# =========================================================
# AI CHAT
# =========================================================

def ask_ai(prompt):

    if not prompt:
        return "Please enter a message."

    try:

        model = get_ai_model()

        # -------------------------------------------------
        # SYSTEM INSTRUCTION
        # -------------------------------------------------

        system_instruction = """
You are SkinAI Pro's AI assistant.

Your job is to help users with:
- General skin-related questions
- Basic skincare information
- Skin disease information
- SkinAI application related questions
- General health information related to skin

Important:
- Give clear and easy-to-understand answers.
- Do not claim to make a definite medical diagnosis.
- For serious or concerning symptoms, recommend consulting a qualified doctor.
- Keep answers helpful and concise.
"""

        final_prompt = (
            system_instruction
            + "\n\n"
            + "User message:\n"
            + str(prompt)
        )

        # -------------------------------------------------
        # GEMINI REQUEST
        # -------------------------------------------------

        response = model.generate_content(
            final_prompt
        )

        # -------------------------------------------------
        # GET RESPONSE TEXT
        # -------------------------------------------------

        if response is None:
            return "Sorry, I could not generate a response."

        text = getattr(
            response,
            "text",
            None
        )

        if text:
            return text.strip()

        return (
            "Sorry, I could not generate a response "
            "right now."
        )

    # -----------------------------------------------------
    # RATE LIMIT / QUOTA
    # -----------------------------------------------------

    except Exception as e:

        error_text = str(e).lower()

        if (
            "resourceexhausted" in error_text
            or "quota" in error_text
            or "429" in error_text
        ):
            return (
                "AI service is temporarily busy because "
                "the Gemini API quota/rate limit has been "
                "reached. Please try again shortly."
            )

        # -------------------------------------------------
        # OTHER GEMINI ERROR
        # -------------------------------------------------

        print(
            "AI ERROR:",
            repr(e)
        )

        return (
            "Sorry, I couldn't process your message "
            "right now. Please try again."
        )