import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

_client = None

if API_KEY:
    try:
        _client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print("Gemini client initialization failed:", e)


def ask_gemini(prompt: str) -> str:

    if not prompt or not prompt.strip():
        return "Please enter something to ask."

    if not _client:
        return (
            "AI is not connected yet. Please add your "
            "GEMINI_API_KEY in the .env file."
        )

    last_error = None

    for attempt in range(3):

        try:

            response = _client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            answer = getattr(response, "text", None)

            if answer and answer.strip():
                return answer.strip()

            return "I couldn't generate an answer. Please try again."

        except Exception as e:

            last_error = e

            print(
                f"Gemini attempt {attempt + 1} failed:",
                e
            )

            if attempt < 2:
                time.sleep(2)

    print("Gemini final error:", last_error)

    return (
        "I'm having trouble connecting to the AI right now. "
        "Please try again in a few seconds."
    )