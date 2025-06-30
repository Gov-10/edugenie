# from django.shortcuts import render, redirect
# from .forms import SignupForm, SigninForm,PasswordResetForm, SetNewPassword
# from .models import Student
# from .utils import send_email, student_token_generator, send_reset
# from django.contrib.auth.hashers import check_password, make_password
# from django.urls import reverse
# from django.contrib import messages
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# import logging
# from django.utils.encoding import force_bytes
# from django.views.decorators.csrf import csrf_exempt 
# from django.contrib.auth.decorators import login_required


# def home(request):
#     return render(request, 'home.html')

# def about_us(request):
#     return render(request, 'about_us.html')

# def verify_email(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         student = Student.objects.get(pk=uid)

#         if str(student.email_token) == token:
#             if not student.is_verified:
#                 student.is_verified = True
#                 student.is_active = True
#                 student.save()
#                 messages.success(request, "Email verified! You can now sign in.")
#             return redirect('sign_in')
#         else:
#             messages.error(request, "Invalid verification link.")
#             return render(request, 'sign_up.html')

#     except (TypeError, ValueError, OverflowError, Student.DoesNotExist) as e:
#         logging.error(f"Verification error: {str(e)}")
#         messages.error(request, "Invalid verification link.")
#         return render(request, 'sign_up.html')

# #@csrf_exempt   #uncomment this line if you want to use locust for load testing
# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.is_active = False
#             student.save()
            
#             try:
#                 send_result = send_email(student, request)
#                 if send_result:
#                     return render(request, 'email_verification_sent.html', {'email': student.email})
#                 else:
#                     messages.error(request, "Failed to send verification email. Please try again.")
#                     return render(request, 'sign_up.html', {'form': form})
#             except Exception as e:
#                 logging.error(f"Email sending error: {str(e)}")
#                 messages.error(request, f"Failed to send verification email: {str(e)}")
#                 return render(request, 'sign_up.html', {'form': form})
#         else:
#             return render(request, 'sign_up.html', {'form': form})
#     else:
#         form = SignupForm()
#         return render(request, 'sign_up.html', {'form': form})

# def signin(request):
#     if request.method == "POST":
#         form = SigninForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data.get('name')
#             password = form.cleaned_data.get('password')
#             stud = form.cleaned_data.get('stud')  # Checkbox value

#             try:
#                 student = Student.objects.get(name=name)

#                 if not student.is_verified:
#                     form.add_error(None, "Please verify your email before signing in.")
#                     return render(request, 'sign_in.html', {'form': form})

#                 if check_password(password, student.password):
#                     if stud:
#                         return render(request, 'stud.html', {'form': form, 'success': True})
#                     else:
#                         return render(request, 'new.html', {'form': form, 'success': True})
#                 else:
#                     form.add_error(None, "Invalid username or password")

#             except Student.DoesNotExist:
#                 form.add_error(None, "Invalid username or password")

#         return render(request, 'sign_in.html', {'form': form})

#     else:
#         form = SigninForm()
#         return render(request, 'sign_in.html', {'form': form})
    
# def passwordreset(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             try:
#                 student = Student.objects.get(email = email)
#                 uid = urlsafe_base64_encode(force_bytes(student.pk))
#                 token = student_token_generator.make_token(student)
#                 reset_link = request.build_absolute_uri(
#                     reverse('reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
#                 )
#                 send_reset(
#                     student, 
#                     request, 
#                     subject = f"EduGenie password reset request",
#                     message=f"Click here to reset your password: {reset_link}"
#                 )
#                 messages.success(request, "Reset link sent to your email.")
#                 return render(request, 'pass_set.html')

#             except Student.DoesNotExist:
#                 form.add_error('email', "No account found with this email.")
#     else:
#         form = PasswordResetForm()

#     return render(request, 'password_reset.html', {'form': form})

# def reset_password_confirm(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         student = Student.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
#         student = None

#     if student and student_token_generator.check_token(student, token):
#         if request.method == "POST":
#             form = SetNewPassword(request.POST, instance=student)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Password updated! You can sign in now.")
#                 return redirect('sign_in')
#         else:
#             form = SetNewPassword(instance=student)  # <-- Fix here
#         return render(request, 'set_password.html', {'form': form})
#     else:
#         messages.error(request, "Invalid or expired reset link.")
#         return redirect('sign_in')
    

from django.conf import settings
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from .forms import SignupForm, SigninForm,PasswordResetForm, SetNewPassword, PdfSummarizerForm, QuizPreferenceForm, DynamicQuizForm, ResumeUploadForm
from .models import Student
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import logging
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render
import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz
import re
import json
from .utils.resume_parse import parse_resume
from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile
import boto3
import time
import requests
import markdown2

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")
def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def chat_page(request):
    return render(request, 'chat.html')


def professional(request):
    return render(request, 'new.html')

def chat_response(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        try:
            prompt = f"Human: {message}\nAssistant:"

            body = {
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.7,
                "stop_sequences": ["\nHuman:"]
            }

            response = bedrock.invoke_model(
                modelId="amazon.titan-text-express-v1",
                contentType="application/json",
                accept="application/json", 
                body=json.dumps({
                    "inputText": message
                })
            )

            response_body = json.loads(response['body'].read())
            reply = response_body['results'][0]['outputText'].strip()

            return JsonResponse({"response": reply})

        except Exception as e:
            print("Bedrock Error:", str(e))
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)
# def signup(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False) #commit = False prevents data from getting stored in the DB
#             student.is_active = False
#             student.save()  
#             if ActivateEmail(request, student, form.cleaned_data.get('email')):
#                 messages.success(request, f'Email activation link has been sent to <b>{student.email}</b>')
#                 return render(request, 'email_verification_sent.html') 
#             else:
#                 messages.error(request, "Failed to send email, kindly check if you typed it correct")
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)
#     else:
#         form = SignupForm()  # <-- You need this line to render form on GET

#     return render(request, 'sign_up.html', {'form': form})
def signup(request):
    if request.method == "POST":
        post_data = request.POST.copy()

        # Pass g-recaptcha-response to recaptcha_token explicitly
        if 'g-recaptcha-response' in request.POST:
            post_data['recaptcha_token'] = request.POST.get('g-recaptcha-response')

        form = SignupForm(post_data)

        if form.is_valid():
            student = form.save(commit=False)
            student.is_active = False
            student.save()

            if ActivateEmail(request, student, form.cleaned_data.get('email')):
                messages.success(request, f'Email activation link has been sent to <b>{student.email}</b>')
                return render(request, 'email_verification_sent.html')
            else:
                messages.error(request, "Failed to send email, kindly check if you typed it correct")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = SignupForm()

    return render(request, 'sign_up.html', {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})


# def signin(request):
#     if request.method == "POST":
#         post_data = request.POST.copy()
#         token = post_data.get('g-recaptcha-response')
#         # Pass g-recaptcha-response to recaptcha_token explicitly
#         if 'g-recaptcha-response' in request.POST:
#             post_data['recaptcha_token'] = request.POST.get('g-recaptcha-response')
#         form = SigninForm(request.POST)
#         if not verify_recaptcha(token):
#           form = SigninForm(post_data)
#           form.add_error(None, "Invalid reCAPTCHA. Please try again.")
#           return render(request, 'sign_in.html', {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             stud = form.cleaned_data.get('stud')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 if not user.is_verified:
#                     form.add_error(None, "Please verify your email before signing in.")
#                     return render(request, 'sign_in.html', {'form': form})
#                 login(request, user)
#                 if stud:
#                     return render(request, 'stud.html', {'form': form, 'success': True, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
#                 else:
#                     return render(request, 'new.html', {'form': form, 'success': True, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
#             else:
#                 form.add_error(None, "Invalid username or password")
#     else:
#         form = SigninForm()
#     return render(request, 'sign_in.html', {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        print(">> Form Valid:", form.is_valid())
        if not form.is_valid():
         print(">> Form Errors:", form.errors)
        if form.is_valid():
            token = request.POST.get('g-recaptcha-response')
            print(">> reCAPTCHA Token:", token)
            if not verify_recaptcha(token):
                print(">> reCAPTCHA failed")
                form.add_error(None, "Invalid reCAPTCHA. Please try again.")
                return render(request, 'sign_in.html', {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            stud = form.cleaned_data.get('stud')
            print(">> Username:", username)
            print(">> Password:", password)
            user = authenticate(request, username=username, password=password)
            print(">> Authenticated User:", user)
            if user is not None:
                print(">> User is_verified:", user.is_verified)
                if not user.is_verified:
                    print(">> User email not verified")
                    form.add_error(None, "Please verify your email before signing in.")
                    return render(request, 'sign_in.html', {'form': form})
                login(request, user)
                print(">> Login successful")
                if stud:
                    return redirect('stud')
                else:
                    return render(request, 'new.html', {'form': form, 'success': True, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
            else:
                print(">> Invalid username or password")
                form.add_error(None, "Invalid username or password")
        # If form is invalid, fall through to re-render with errors
    else:
        form = SigninForm()
    return render(request, 'sign_in.html', {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

@csrf_exempt
@login_required
def pdf_summarizer(request):
    summary = None
    if request.method == "POST":
        form = PdfSummarizerForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = request.FILES['pdf']
            text = extract_text(pdf)
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
    f"{text}"
            )
            try:
                response = model.generate_content(prompt)
                summary = response.text.strip()
            except Exception as e:
                summary = f"❌ Error: {str(e)}"
    else:
        form = PdfSummarizerForm()

    return render(request, 'pdf_summarizer.html', {
        'form': form,
        'summary': summary
    })


@login_required
def logoutUser(request):
    messages.success(request, "You’ve been logged out successfully.")
    logout(request)
    return redirect('home')

def activate(request, uidb64, token):
        try:
          uid = force_str(urlsafe_base64_decode(uidb64))
          student = Student.objects.get(pk = uid)
        except:
            student = None
        
        if student is not None and account_activation_token.check_token(student, token):
            student.is_active = True
            student.is_verified = True
            student.save()
            return redirect('sign_in')
        else:
            messages.error(request, "Activation Failed!!")
        return redirect('home')

def ActivateEmail(request,user, to_email):
    mail_subject = "Activate your account"
    message = render_to_string("template_activate.html", {
        'user' : user.username,
        'domain': get_current_site(request).domain,
         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
         'token': account_activation_token.make_token(user),
         "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    return email.send()

def testimonials(request):
    return render(request, 'testimonials.html')


def verify_recaptcha(token):
    """Helper function to verify reCAPTCHA"""
    import requests
    from django.conf import settings
    
    data = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': token
    }
    
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data,
            timeout=10
        )
        result = response.json()
        return result.get('success', False)
    except:
        return False

def stud(request):
    return render(request, 'stud.html')

def professional(request):
    return render(request, 'new.html')

def contact(request):
    return render(request, 'contact_us.html')

def extract_text(pdf):
    pdf_document = fitz.open(stream=pdf.read(), filetype="pdf")
    pages = []

    for i, page in enumerate(pdf_document):
        page_text = page.get_text()
        pages.append(f"--- Page {i + 1} ---\n{page_text}")
    
    pdf_document.close()
    return "\n\n".join(pages)

# @csrf_exempt
# @login_required
# def quiz_preference(request):
#     if request.method == "POST":
#         form = QuizPreferenceForm(request.POST)
#         if form.is_valid():
#             preferences = form.cleaned_data
#             print(">> Quiz Preferences:", preferences)
#             prompt = (
#                 "You are a quiz generator and an exam paper setter. Please be very accurate and avoid giving any wrong answers. You are allowed to use any website or any book for reference.Based on the user's preferences, "
#                 "generate a quiz with the following details:\n"
#                 f"Subject: {preferences['topic']}\n"
#                 f"Difficulty: {preferences['difficulty']}\n"
#                 f"Number of Questions: {preferences['number_of_questions']}\n"
#                 f"Question Type: {preferences['type_of_questions']}\n"
#                 f"Timer: {preferences['timer']}\n"
#                 "Please format the quiz clearly with numbered questions, "
#                 "and include the correct answer below each question as 'Answer: ...'\n"
#                 "Each option must be labeled as A. / B. / C. / D.  and mention the correct answer using the letter (e.g., Correct Answer: C)\n"
#                 "Please ensure the quiz is engaging and educational, suitable for students preparing for exams.\n\n"
#                 "Please do not include text like Time's up! Check your answers above.**   Directly provide the quiz content without any additional instructions or comments.\n"
#             )
#             try:
#                 response = model.generate_content(prompt)
#                 quiz_text = response.text.strip()
#                 print(">>> AI Raw Output:\n", quiz_text)
#                 request.session['quiz_text'] = quiz_text  # for next view
#                 return redirect('render_quiz') 
#             except Exception as e:
#                 print("Gemini Error:", str(e))
#             print(">> Quiz Preferences:", preferences)
#             messages.success(request, "Your quiz preferences have been saved successfully!")
#     else:
#         form = QuizPreferenceForm()
#     return render(request, 'quiz_custom.html', {'form': form})


def parse_ai_quiz(quiz_text):
    import re

    blocks = re.split(r"(?:\n|\A)(?:Question\s*)?\d+[:.\)]\s+", quiz_text.strip())
    questions = []

    for block in blocks:
        block = block.strip()
        if not block or len(block) < 5:
            continue

        lines = block.split('\n')
        question_lines = []
        options = []
        correct = ""

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Match options A–D
            opt_match = re.match(r"([A-Da-d])[).]?\s+(.*)", line)
            if opt_match:
                options.append((opt_match.group(1).lower(), opt_match.group(2).strip()))
                continue

            # Match correct answer
            ans_match = re.search(r"(Correct\s*)?Answer[:\s]*([A-Da-d])", line, re.IGNORECASE)
            if ans_match:
                correct = ans_match.group(2).lower()
                continue

            question_lines.append(line)

        question_text = '\n'.join(question_lines).strip()
        if question_text and len(options) == 4 and correct in ['a', 'b', 'c', 'd']:
           questions.append({
        "question": question_text,
        "options": options,
        "correct": correct
    })

    print(">> Parsed Questions:", questions)
    return questions


# def parse_ai_quiz(quiz_text):
#     import re
#     questions = []
#     blocks = re.split(r"\n\d+\.\s+", quiz_text.strip())
#     for block in blocks:
#         lines = block.strip().split('\n')
#         if not lines or len(lines) < 2:
#             continue

#         question_line = lines[0].strip()
#         question_text = question_line.replace('**', '').strip()

#         options = []
#         correct = ""

#         for line in lines[1:]:
#             line = line.strip()
#             if not line or line.startswith("```"):
#                 continue

#             # Match options like: A. Option or A) Option
#             opt_match = re.match(r"([A-Da-d])[.)]?\s+(.*)", line)
#             if opt_match:
#                 label = opt_match.group(1).lower()
#                 option_text = opt_match.group(2).strip()
#                 options.append((label, option_text))

#             elif "answer" in line.lower():
#               match = re.search(r"answer[:\s]*([A-D])", line, re.IGNORECASE)
#               if match:
#                correct = match.group(1).lower()

#         if question_text and options:
#             questions.append({
#                 "question": question_text,
#                 "options": options,
#                 "correct": correct
#             })

#     print(">> Parsed Questions:", questions)
#     return questions


@csrf_exempt
@login_required
def render_quiz(request):
    quiz_text = request.session.get('quiz_text', None)
    if not quiz_text:
        return redirect('quiz_preference')  # fallback

    questions = parse_ai_quiz(quiz_text)

    if request.method == "POST":
        form = DynamicQuizForm(questions, request.POST)
        if form.is_valid():
            score = 0
            results = []
            for i, q in enumerate(questions):
                user_ans = form.cleaned_data[f'q_{i}']
                correct_ans = q['correct']
                is_correct = (user_ans == correct_ans)
                results.append({
                    "question": q['question'],
                    "selected": user_ans,
                    "correct": correct_ans,
                    "is_correct": is_correct,
                    "options": q['options']
                })
                if is_correct:
                    score += 1
            percentage = (score / len(questions)) * 100
            return render(request, 'quiz_results.html', {
                'results': results,
                'score': score,
                'total': len(questions),
                'percentage': percentage
            })
    else:
        form = DynamicQuizForm(questions)

    return render(request, 'render_quiz.html', {
        'form': form,
        'questions': questions
    })

@login_required
@csrf_exempt
def resume_tester(request):
    parsed_text = None
    html_response = None
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(">> Form is valid")
            resume = request.FILES['resume']
            print(">> Resume file:", resume.name)
            parsed_text = parse_resume(resume)
            print(">> Parsed Text:", parsed_text)
#             prompt = f"""
# You are a professional resume reviewer and career mentor. Please analyze the following resume text and provide comprehensive feedback in a beautifully formatted, visually appealing response.

# Resume Text:
# {parsed_text}

# FORMATTING INSTRUCTIONS:
# Please structure your response using the following beautiful, professional format with proper markdown styling:

# # 📋 Resume Analysis Report

# ## 👤 **Candidate Overview**
# [Brief 2-3 sentence summary of the candidate's profile]

# ---

# ## ⭐ **Strengths & Highlights**
# ### 🎯 What's Working Well:
# - **[Strength Category]**: [Specific detail]
# - **[Strength Category]**: [Specific detail]
# - **[Strength Category]**: [Specific detail]

# ---

# ## 🔧 **Areas for Improvement**

# ### 📝 **Content Enhancement**
# | Section | Current Issue | Recommended Action |
# |---------|---------------|-------------------|
# | [Section] | [Issue] | [Specific improvement] |
# | [Section] | [Issue] | [Specific improvement] |

# ### 🎨 **Formatting & Structure**
# - **Issue**: [Problem description]
#   - *Solution*: [Specific fix]
# - **Issue**: [Problem description]
#   - *Solution*: [Specific fix]

# ---

# ## 🚀 **Action Plan for Improvement**

# ### 🎯 **Priority 1 - Critical Changes**
# 1. **[Action Item]**
#    - Why: [Explanation]
#    - How: [Specific steps]

# 2. **[Action Item]**
#    - Why: [Explanation]
#    - How: [Specific steps]

# ### 📈 **Priority 2 - Enhancement Opportunities**
# 1. **[Action Item]**
#    - Impact: [Expected benefit]
#    - Implementation: [How to do it]

# ---

# ## 🤖 **ATS Compatibility Score**

# ### 📊 **Overall ATS Score: [X]/100**

# | Criteria | Score | Status | Notes |
# |----------|-------|--------|-------|
# | **Keyword Optimization** | [X]/25 | [🟢/🟡/🔴] | [Specific feedback] |
# | **Format Compatibility** | [X]/25 | [🟢/🟡/🔴] | [Specific feedback] |
# | **Section Organization** | [X]/25 | [🟢/🟡/🔴] | [Specific feedback] |
# | **Contact Information** | [X]/25 | [🟢/🟡/🔴] | [Specific feedback] |

# **Legend:** 🟢 Excellent | 🟡 Needs Improvement | 🔴 Critical Issue

# ---

# ## 💡 **Industry-Specific Recommendations**
# [Tailored advice based on the candidate's target industry/role]

# ---

# ## ✨ **Next Steps**
# ### 📅 **30-Day Improvement Timeline**
# - **Week 1**: [Specific tasks]
# - **Week 2**: [Specific tasks]
# - **Week 3**: [Specific tasks]
# - **Week 4**: [Final review and optimization]

# ---

# ## 🎯 **Interview Readiness Prediction**
# **Current State**: [Assessment]
# **With Improvements**: [Projected outcome]

# ---

# *💪 Remember: Your resume is your personal marketing document. With these improvements, you'll be well-positioned to capture recruiters' attention and land those interview opportunities!*

# TONE GUIDELINES:
# - Be encouraging and supportive like a caring mentor
# - Use positive, constructive language
# - Provide specific, actionable advice
# - Include motivational elements
# - Be honest about weaknesses while maintaining optimism
# - Focus on growth and potential

# ANALYSIS DEPTH:
# - Provide detailed, section-by-section feedback
# - Include specific examples and suggestions
# - Give honest ATS scoring with clear explanations
# - Offer industry-specific insights where relevant
# - Create a clear action plan for improvement

# End Goal: Transform this resume into an interview-generating document that stands out to both ATS systems and human recruiters.
# """
            prompt = f"""
You are an experienced **career mentor and resume reviewer** with deep knowledge of ATS systems, recruitment best practices, and formatting standards for technical and non-technical roles.

Your task is to **analyze the following resume text** and provide a **comprehensive, visually structured, and markdown-formatted** report that is both **constructive** and **motivational**.

---

## 📄 Resume Text:
{parsed_text}

---

## 🧠 INSTRUCTIONS:
Use the following **sectioned format** and markdown layout for the response. Make it visually pleasing, with emojis, tables, and concise yet insightful suggestions.

# 📋 Resume Analysis Report

## 👤 **Candidate Overview**
Briefly summarize the candidate's background, area of expertise, and what kind of roles they may be suited for (2–3 sentences).

---

## ⭐ **Strengths & Highlights**
### 🎯 What's Working Well:
- **[Category]**: [Highlight detail]
- **[Category]**: [Highlight detail]
- **[Category]**: [Highlight detail]

Be specific and appreciative. Highlight what stands out.

---

## 🔧 **Areas for Improvement**

### 📝 Content Enhancement (Table Format)
Use this table to show weak spots and solutions:

| Section        | Current Issue                          | Recommended Action                    |
|----------------|----------------------------------------|----------------------------------------|
| [Example: Summary] | Vague wording, lacks impact         | Rewrite with role-specific language    |
| [Example: Skills]   | Too generic                        | Group by category and use keywords     |

### 🎨 Formatting & Structure
- **Issue**: [Brief formatting flaw]
  - *Fix*: [What should be improved and how]

---

## 🚀 **Action Plan for Improvement**

### 🎯 Priority 1 – Critical Fixes
1. **[Item]**
   - *Why it matters:* [Short explanation]
   - *How to fix:* [Practical next steps]

2. **[Item]**
   - *Why it matters:* [...]
   - *How to fix:* [...]

### 📈 Priority 2 – Nice-to-Have Enhancements
1. **[Item]**
   - *Benefit:* [Impact on recruiter interest or ATS]
   - *Implementation:* [Brief how-to]

---

## 🤖 **ATS Compatibility Score**

### 📊 Estimated ATS Score: **[XX]/100**

| Category               | Score | Status | Notes                          |
|------------------------|-------|--------|--------------------------------|
| Keyword Optimization   | XX/25 | 🟢🟡🔴 | [Comment]                      |
| Format Compatibility   | XX/25 | 🟢🟡🔴 | [Comment]                      |
| Section Organization   | XX/25 | 🟢🟡🔴 | [Comment]                      |
| Contact Information    | XX/25 | 🟢🟡🔴 | [Comment]                      |

🟢 = Excellent | 🟡 = Moderate | 🔴 = Needs Work

---

## 💡 **Industry-Specific Recommendations**
Give tailored advice based on the resume content. If the candidate targets tech roles, suggest relevant buzzwords, portfolio tips, etc.

---

## ✨ **Next Steps**

### 📅 30-Day Optimization Timeline

- **Week 1**: [e.g., Revise summary, fix contact info]
- **Week 2**: [e.g., Optimize project descriptions]
- **Week 3**: [e.g., Polish formatting, use ATS keywords]
- **Week 4**: [e.g., Final proofing and mock interview prep]

---

## 🎯 Interview Readiness

- **Current Status**: [Honest evaluation]
- **Post-Improvement Prediction**: [Encouraging insight]

---

🎓 *Remember*: A resume isn’t just a list — it’s your story. These changes will help you stand out to both **ATS bots** and **human reviewers**, and bring you one step closer to that **dream interview.**

Be motivational, realistic, and focused on growth. Avoid vague advice. Always give practical, specific tips.
"""
  
            try:
                response = model.generate_content(prompt)
                parsed_text = response.text.strip()
                print(">> AI Response:", parsed_text)
                html_response = markdown2.markdown(parsed_text, extras=["tables", "fenced-code-blocks"])
            except Exception as e:
                parsed_text = f"❌ Error: {str(e)}"
                print(">> Gemini Error:", str(e))
    else:
        form = ResumeUploadForm()
    return render(request, 'resume_tester.html', {
        'form': form,
        'parsed_text': html_response
    })

@csrf_exempt
@login_required
def quiz_preference(request):
    if request.method == "POST":
        form = QuizPreferenceForm(request.POST)
        if form.is_valid():
            preferences = form.cleaned_data
            try:
                lambda_api_url = "https://u9pmy5pmn4.execute-api.ap-south-1.amazonaws.com/prod/generate_quiz_function"
                response = requests.post(lambda_api_url, json=preferences)
                print("Lambda response:", response.text)
                if response.status_code == 200:
                    quiz_text = response.json().get("quiz", "")
                    request.session['quiz_text'] = quiz_text
                    return redirect('render_quiz')
                else:
                    messages.error(request, "Lambda returned error: " + response.text)
            except Exception as e:
                messages.error(request, f"❌ Error calling Lambda: {str(e)}")
                print("Exception:", str(e))
    else:
        form = QuizPreferenceForm()
    return render(request, 'quiz_custom.html', {'form': form})

# views.py
from django.shortcuts import render, redirect
from .forms import TestimonialForm
from .models import Testimonial
from .utils.ai import is_testimonial_appropriate  # import your AI moderation logic

def testimonial_submit(request):
    message = None
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            if is_testimonial_appropriate(testimonial.message):
                testimonial.approved = True
                testimonial.save()
                message = "✅ Thank you! Your testimonial has been submitted."
            else:
                message = "❌ Sorry, your message did not meet our guidelines."
    else:
        form = TestimonialForm()

    return render(request, "submit_testimonial.html", {
        'form': form,
        'message': message
    })

def show_testimonials(request):
    testimonials = Testimonial.objects.filter(approved=True).order_by('-timestamp')
    return render(request, "testimonials.html", {"testimonials": testimonials})