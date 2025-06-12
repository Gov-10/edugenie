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
from .forms import SignupForm, SigninForm,PasswordResetForm, SetNewPassword
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


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def chat_page(request):
    return render(request, 'chat.html')

def chat_response(request):
    if request.method == "POST":
        message = request.POST.get("message")
        try:
            response = model.generate_content(message)
            reply = response.text.strip()
            return JsonResponse({"response": reply})
        except Exception as e:
             print("Gemini Error:", str(e))
             return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

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
                    return render(request, 'stud.html', {'form': form, 'success': True})
                else:
                    return render(request, 'new.html', {'form': form, 'success': True})
            else:
                print(">> Invalid username or password")
                form.add_error(None, "Invalid username or password")
        # If form is invalid, fall through to re-render with errors
    else:
        form = SigninForm()
    return render(request, 'sign_in.html', {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

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

def intern(request):
    return render(request, 'new.html')