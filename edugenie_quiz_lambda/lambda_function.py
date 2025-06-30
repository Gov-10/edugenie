import json
import boto3

def lambda_handler(event, context):
    body = event.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception as e:
            print("JSON decode error:", str(e))
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON body"})
            }


    topic = body.get("topic", "")
    num_questions = body.get("number_of_questions", 5)
    difficulty = body.get("difficulty", "medium")
    type_qs = body.get("type_of_questions", "mcq")

    prompt = (
    "You are an experienced exam paper setter and quiz generator. Your task is to create an accurate, factual, and well-structured quiz based on the following user preferences:\n\n"
    f"- Subject: {topic}\n\n"
    f"- Difficulty: {difficulty}\n\n"
    f"-Number of Questions to generate: {num_questions} (strictly this number)\n\n"
    f"- Type of Questions: {type_qs}\n\n"
    "⚠️ Important Guidelines:\n\n"
    "1. Do NOT hallucinate facts. Only include questions with clear, verifiable answers.\n\n"
    "2. The correct answer must be 100% accurate and based on commonly accepted knowledge.\n\n"
    "3. Format strictly as:\n"
    "   - Question number.\n"
    "   - Four options (A., B., C., D.)\n"
    "   - Below each question, write `Correct Answer: <letter>`\n"
    "4. Do NOT include instructions, explanations, comments, or filler text.\n"
    "5. Make sure the quiz is suitable for high school/college-level students.\n\n"
    "💡 Example format: (just for structure, do not repeat):\n"
    "1. What is the capital of France?\n"
    "A. Berlin\n"
    "B. Madrid\n"
    "C. Paris\n"
    "D. Rome\n"
    "Correct Answer: C\n\n"
    "6. Ensure the questions are diverse and cover different aspects of the topic.\n\n"
    "7. Do NOT include any questions that are too easy or too difficult for the specified difficulty level.\n\n"
    "8. Do NOT include any questions that are too similar to each other.\n\n"
    "9. Do NOT include any questions that are too vague or ambiguous.\n\n"
    "Do NOT show answers in the response.\n\n"
    "⚠️ Important: Do NOT include any additional text, explanations, or comments. Only provide the questions in the specified format.\n\n"
    f"Generate exactly {num_questions} questions now, strictly following the format above.\n"
)


    bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

    try:
        response = bedrock.invoke_model(
            modelId="amazon.titan-text-express-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "inputText": prompt
            })
        )
        result = json.loads(response["body"].read())
        quiz_text = result["results"][0]["outputText"]
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"quiz": quiz_text})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
