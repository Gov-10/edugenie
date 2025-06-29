# from docx import Document
# from pdfminer.high_level import extract_text
# import os

# def parse_resume(resume_file):
#     extension = os.path.splitext(resume_file.name)[1].lower()
#     try:
#         if extension == ".pdf":
#             from pdfminer.high_level import extract_text
#             resume_file.open('rb')  # Ensure file is binary stream
#             text = extract_text(resume_file)
#         elif extension == ".docx":
#             from docx import Document
#             doc = Document(resume_file)
#             text = "\n".join([para.text for para in doc.paragraphs])
#         elif extension == ".txt":
#             text = resume_file.read().decode("utf-8")
#         else:
#             return "Unsupported format"
#         return text.strip() or "[No readable text found]"
#     except Exception as e:
#         print("Error during parsing:", e)
#         return "[Parsing failed]"
    



# from tika import parser
# def parse_resume(resume_file):
#     parsed = parser.from_file(resume_file)
#     return parsed['content'] or "[No readable text found]"


# from tika import parser
# import tempfile
# import os

# def parse_resume(resume_file):
#     try:
#         # Ensure we work with a real file path for tika
#         with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as temp:
#             for chunk in resume_file.chunks():
#                 temp.write(chunk)
#             temp_path = temp.name

#         parsed = parser.from_file(temp_path)
#         content = parsed.get('content', '').strip()

#         os.remove(temp_path)

#         return content if content else "[No readable text found]"
#     except Exception as e:
#         return f"[Parsing failed]: {str(e)}"


import os
import tempfile
import re
from tika import parser

def clean_text(text):
    lines = text.splitlines()
    cleaned = [
        line for line in lines
        if line.strip() and not line.strip().lower().endswith(('.png', '.svg'))
    ]
    result = '\n'.join(cleaned)
    result = re.sub(r'\.MsftOfcThm.*?\{.*?\}', '', result)
    return result.strip()

def parse_resume(resume_file):
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as temp:
            for chunk in resume_file.chunks():
                temp.write(chunk)
            temp_path = temp.name

        parsed = parser.from_file(temp_path)
        content = parsed.get('content', '').strip()

        return clean_text(content) if content else "[No readable text found]"
    except Exception as e:
        return f"[Parsing failed]: {str(e)}"
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
