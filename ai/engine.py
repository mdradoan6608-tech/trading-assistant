import google.generativeai as genai

from config.settings import GEMINI_API_KEY
from ai.prompts import SYSTEM_PROMPT
from core.response import success, error
from utils.logger import logger

genai.configure(api_key=GEMINI_API_KEY)


def ask_ai(user_prompt):
    if not GEMINI_API_KEY:
        logger.error("Gemini API key not configured.")
        return error("Gemini API key not configured.")

    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPT,
        )

        response = model.generate_content(user_prompt)

        return success("AI response", {"text": response.text.strip()})

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        if "429" in str(e):
            return error("AI analysis is temporarily rate-limited. Please try again shortly.")
        return error("AI analysis is temporarily unavailable. Please try again in a few minutes.")
