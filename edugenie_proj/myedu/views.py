from django.shortcuts import render, redirect
from .forms import SignupForm, SigninForm,PasswordResetForm, SetNewPassword
from .models import Student
from .utils import send_email, student_token_generator, send_reset
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import logging
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        student = Student.objects.get(pk=uid)

        if str(student.email_token) == token:
            if not student.is_verified:
                student.is_verified = True
                student.is_active = True
                student.save()
                messages.success(request, "Email verified! You can now sign in.")
            return redirect('sign_in')
        else:
            messages.error(request, "Invalid verification link.")
            return render(request, 'sign_up.html')

    except (TypeError, ValueError, OverflowError, Student.DoesNotExist) as e:
        logging.error(f"Verification error: {str(e)}")
        messages.error(request, "Invalid verification link.")
        return render(request, 'sign_up.html')

#@csrf_exempt   #uncomment this line if you want to use locust for load testing
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.is_active = False
            student.save()
            
            try:
                send_result = send_email(student, request)
                if send_result:
                    return render(request, 'email_verification_sent.html', {'email': student.email})
                else:
                    messages.error(request, "Failed to send verification email. Please try again.")
                    return render(request, 'sign_up.html', {'form': form})
            except Exception as e:
                logging.error(f"Email sending error: {str(e)}")
                messages.error(request, f"Failed to send verification email: {str(e)}")
                return render(request, 'sign_up.html', {'form': form})
        else:
            return render(request, 'sign_up.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'sign_up.html', {'form': form})

def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            stud = form.cleaned_data.get('stud')  # Checkbox value

            try:
                student = Student.objects.get(name=name)

                if not student.is_verified:
                    form.add_error(None, "Please verify your email before signing in.")
                    return render(request, 'sign_in.html', {'form': form})

                if check_password(password, student.password):
                    if stud:
                        return render(request, 'stud.html', {'form': form, 'success': True})
                    else:
                        return render(request, 'new.html', {'form': form, 'success': True})
                else:
                    form.add_error(None, "Invalid username or password")

            except Student.DoesNotExist:
                form.add_error(None, "Invalid username or password")

        return render(request, 'sign_in.html', {'form': form})

    else:
        form = SigninForm()
        return render(request, 'sign_in.html', {'form': form})
    
def passwordreset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                student = Student.objects.get(email = email)
                uid = urlsafe_base64_encode(force_bytes(student.pk))
                token = student_token_generator.make_token(student)
                reset_link = request.build_absolute_uri(
                    reverse('reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                send_reset(
                    student, 
                    request, 
                    subject = f"EduGenie password reset request",
                    message=f"Click here to reset your password: {reset_link}"
                )
                messages.success(request, "Reset link sent to your email.")
                return redirect('sign_in')

            except Student.DoesNotExist:
                form.add_error('email', "No account found with this email.")
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        student = Student.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
        student = None

    if student and student_token_generator.check_token(student, token):
        if request.method == "POST":
            form = SetNewPassword(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated! You can sign in now.")
                return redirect('sign_in')
        else:
            form = SetNewPassword(instance=student)  # <-- Fix here
        return render(request, 'set_password.html', {'form': form})
    else:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('sign_in')