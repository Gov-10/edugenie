# utils/ai.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
def is_testimonial_appropriate(text):
    prompt = f"""
You are an AI moderation assistant. Your job is to check whether the following user testimonial is safe and appropriate for public display on a professional educational website.

Rules:
- APPROVE testimonials that are short, kind, and neutral (e.g., "Great features", "Loved it", "Nice platform", etc.)
- REJECT testimonials that include hate speech, offensive language, personal attacks, NSFW content, or spam.
- DO NOT reject messages just because they are short or generic.

Respond strictly with:
- APPROVED — if safe and polite
- REJECTED — if harmful, inappropriate, or irrelevant

Testimonial:
\"\"\"{text.strip()}\"\"\"
    """
    try:
        response = model.generate_content(prompt)
        decision = response.text.strip().upper()
        return decision == "APPROVED"
    except Exception as e:
        print("AI Moderation Error:", str(e))
        return False  # Safer to reject if AI fails
