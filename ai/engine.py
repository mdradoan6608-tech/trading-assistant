import google.generativeai as genai

from config.settings import GEMINI_API_KEY
from ai.prompts import SYSTEM_PROMPT
from core.response import success, error

genai.configure(api_key=GEMINI_API_KEY)


def ask_ai(user_prompt):
    if not GEMINI_API_KEY:
        return error("Gemini API key not configured.")

    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPT,
        )

        response = model.generate_content(user_prompt)

        return success("AI response", {"text": response.text.strip()})

    except Exception as e:
        return error(str(e))
