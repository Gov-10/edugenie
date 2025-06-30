import fitz
import json
import io
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bedrock = boto3.client('bedrock-runtime', region_name='ap-south-1')
    bucket= event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    file_stream = s3.get_object(Bucket = bucket, Key= key)['Body'].read()
    pdf = fitz.open(stream = io.BytesIO(file_stream), filetype='pdf')
    text = ""
    for page in pdf:
        text += page.get_text()
    
    prompt = (
    "/human\n\n"
    "Can you summarize this PDF in simple, understandable points?\n\n"
    "Imagine you're a top-level teacher explaining this topic to students preparing for a final exam.\n\n"
    "🎯 Goals:\n"
    "- Help students understand the content as if you’re personally tutoring them.\n"
    "- Explain important concepts with clarity.\n"
    "- Don’t skip over crucial implementation steps or subtle details.\n\n"
    "📘 Style Requirements:\n"
    "- Your tone should be warm, engaging, and explanatory, like a teacher in class.\n"
    "- Use analogies and real-world comparisons where appropriate.\n"
    "- Begin with a warm introduction, e.g., “👩‍🏫 Welcome to class!” and end with a motivating closing line.\n\n"
    "💡 Output Format Instructions (HTML only):\n"
    "- Wrap content using <div> and <section> for structure.\n"
    "- Use semantic HTML:\n"
    "  - <h2> and <h3> for headings\n"
    "  - <ul><li> for bullet points\n"
    "  - <b> for key phrases\n"
    "  - <hr> to break major sections\n"
    "- Wrap sections in styled blocks like:\n"
    "<div style=\"background-color:#f9f9f9;padding:12px;border-left:4px solid #4CAF50;border-radius:8px;margin-bottom:12px;\">\n"
    "  <!-- Insert content here -->\n"
    "</div>\n\n"
    "📌 Extra Features:\n"
    "- Insert a <b>🧠 Mind Map</b> as a structured HTML list near the end with yellow background like:\n"
    "<div style=\"background-color:#fff8dc;padding:10px;border-left:6px solid #ffa500;border-radius:6px;\">\n"
    "  <h3>🧠 Mind Map: [Topic Name]</h3>\n"
    "  <ul>\n"
    "    <li><b>📌 Concept 1:</b> Summary</li>\n"
    "    <li><b>📌 Concept 2:</b> Summary</li>\n"
    "  </ul>\n"
    "</div>\n\n"
    "- Add a “Quick Recap” section with bold bullet points and emojis for visual retention.\n\n"
    "Here is the full text from the PDF you should work with:\n\n"
    f"{text[:3000]}"
)


    response = bedrock.invoke_model(
        modelId="amazon.titan-text-express-v1",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "inputText": prompt
        })
    )

    response_body = json.loads(response['body'].read())
    summary_text = response_body.get("results", [{}])[0].get("outputText", "No summary returned.")
    output_key = key.replace('.pdf', '_summary.html')  # or add a folder like 'summaries/'

    s3.put_object(
    Bucket=bucket,
    Key=output_key,
    Body=summary_text,
    ContentType='text/html'
    )
