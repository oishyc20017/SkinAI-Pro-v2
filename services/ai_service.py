import streamlit as st
import google.generativeai as genai

genai.configure(
    api_key=st.secrets["API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_ai(prompt):

    language_instruction = """
    IMPORTANT LANGUAGE RULE:
    Reply in the same language as the user's message.

    - If the user writes in English, reply in English.
    - If the user writes in Bengali, reply in Bengali.
    - If the user writes in Banglish, reply in Banglish.
    - Do not switch languages unless the user asks you to.
    """

    final_prompt = f"""
    {language_instruction}

    User message:
    {prompt}
    """

    response = model.generate_content(final_prompt)

    return response.text