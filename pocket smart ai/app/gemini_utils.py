import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

try:
    from google import genai as google_genai

    if API_KEY:
        client = google_genai.Client(api_key=API_KEY)
except ImportError:
    try:
        import google.generativeai as google_genai

        if API_KEY:
            google_genai.configure(api_key=API_KEY)
            client = google_genai
    except ImportError:
        client = None


def generate_recommendation(category, budget, details):

    if not client:
        return None

    prompt = f"""
You are PocketSmart AI, a helpful budget planning assistant.

Category:
{category}

Budget:
₹{budget}

User requirements:
{details}

Give a practical recommendation.

Rules:
- Stay within the given budget.
- Give approximate costs.
- Keep the response easy to understand.
- Include a total estimated cost.
- Suggest alternatives if necessary.
- Do not invent exact product availability.
"""

    try:
        if hasattr(client, "models"):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return getattr(response, "text", None) or str(response)

        model = client.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return getattr(response, "text", None) or str(response)
    except Exception:
        return None