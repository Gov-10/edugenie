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
        "You are a quiz generator and an exam paper setter. Please be very accurate and avoid giving any wrong answers. You are allowed to use any website or any book for reference.Based on the user's preferences, "
                "generate a quiz with the following details:\n"
                f"Subject: {topic}\n"
                f"Difficulty: {difficulty}\n"
                f"Number of Questions: {num_questions}\n"
                f"Question Type: {type_qs}\n"
                "Please format the quiz clearly with numbered questions, "
                "and include the correct answer below each question as 'Answer: ...'\n"
                "Each option must be labeled as A. / B. / C. / D.  and mention the correct answer using the letter (e.g., Correct Answer: C)\n"
                "Please ensure the quiz is engaging and educational, suitable for students preparing for exams.\n\n"
                "Please do not include text like Time's up! Check your answers above.**   Directly provide the quiz content without any additional instructions or comments.\n"
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
