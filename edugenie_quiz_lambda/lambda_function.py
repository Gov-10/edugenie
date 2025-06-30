import json
import boto3
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def lambda_handler(event, context):
    preferences = json.loads(event['body'])
    topic = preferences.get("topic", "General Knowledge")
    difficulty = preferences.get("difficulty", "medium")
    num_questions = preferences.get("number_of_questions", 5)
    type_qs = preferences.get("type_of_questions", "mcq")
    
   
#     prompt = (
#     f"You are an expert quiz generator. Generate exactly {preferences['number_of_questions']} "
#     f"{preferences['difficulty']} level {preferences['type_of_questions']} questions on the topic '{preferences['topic']}'.\n\n"
#     "Format each question as:\n"
#     "1. <Question>\n"
#     "A. ...\nB. ...\nC. ...\nD. ...\nCorrect Answer: <letter>\n\n"
#     "Do not include any explanation or extra text."
# )
    prompt = (
    f"""
You are an expert quiz generator.

Generate exactly {preferences['number_of_questions']} {preferences['difficulty']} level {preferences['type_of_questions']} questions on the topic: "{preferences['topic']}".

⚠️ Important Rules:
- Each question must have exactly **four options** labeled as A., B., C., and D.
- Do **not** repeat or skip options.
- Do **not** use slashes (e.g., A./B./C./D.).
- The correct answer must be written **only** as: Correct Answer: <letter>
- Do NOT write explanations or full sentences after the correct answer.
- Do not include filler text like "Here is a quiz", "Answer: ...", or any extra commentary.

✅ Example:
1. What is the capital of France?
A. Berlin
B. London
C. Paris
D. Rome
Correct Answer: C

Now generate the quiz.
"""
)


    print(">> PROMPT:\n", prompt)



    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    payload = {
    "contents": [{"parts": [{"text": prompt}]}],
}
    print(">> RAW QUIZ TEXT:\n", quiz_text)
    if quiz_text.count("Correct Answer:") < int(preferences['number_of_questions']):
        raise Exception("Incomplete quiz returned by Gemini.")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        quiz_text = data['candidates'][0]['content']['parts'][0]['text']
        return {
            "statusCode": 200,
            "body": json.dumps({"quiz": quiz_text})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }