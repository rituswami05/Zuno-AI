# ============================================================
# ZUNO CREATIVE MODE
# ============================================================

import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY was not found. "
        "Check your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# CREATIVE MODE
# ============================================================

def creative_mode(request: str) -> str:
    """
    Generate creative content using Gemini.

    Supports:
    - stories
    - movie scenes
    - scripts
    - characters
    - dialogue
    - plots
    - worldbuilding
    - continuing stories
    - modifying existing stories
    """

    if not request or not request.strip():
        return "ERROR: Creative request is empty."

    request = request.strip()

    prompt = f"""
You are Zuno Creative Mode.

Create high-quality original creative content based on the
user's request.

The user may ask for:
- a short story
- a long story
- a movie scene
- a screenplay
- a character
- dialogue
- a plot
- worldbuilding
- a continuation of an existing story
- modifications to an existing story

Follow the user's requested format and tone.

Do not explain what you are doing.
Do not mention that you are an AI.
Just produce the requested creative content.

USER REQUEST:
{request}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        if not response:
            return "ERROR: Gemini returned no response."

        text = getattr(response, "text", None)

        if not text:
            return "ERROR: Gemini returned an empty response."

        return text.strip()

    except Exception as e:

        return (
            "ERROR: Creative Mode could not reach Gemini: "
            f"{type(e).__name__}: {e}"
        )