from django.shortcuts import render, redirect
from .forms import SignupForm, SigninForm
from .models import Student
from .utils import send_email, student_token_generator
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import logging
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt

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

# @csrf_exempt   #uncomment this line if you want to use locust for load testing
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
    
