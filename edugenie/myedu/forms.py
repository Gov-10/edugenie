# from django import forms
# from .models import Student
# from django.contrib.auth.hashers import make_password

# class SignupForm(forms.ModelForm):
#     password = forms.CharField(max_length=128,widget=forms.PasswordInput, label="Password")
#     school_student = forms.BooleanField(required=False,label="Are you a school student?")
#     class Meta:
#         model = Student
#         fields = [
#             'name', 
#             'email', 
#             'password', 
#             'school_student'
#         ]
#     def save(self, commit=True):
#         student = super().save(commit=False)
#         student.password = make_password(self.cleaned_data['password'])
#         if not student.email_token:
#             import uuid
#             student.email_token = uuid.uuid4()
#         student.is_verified = False
#         if commit:
#             student.save()
#         return student
        
# class SigninForm(forms.Form):
#     name = forms.CharField(max_length=100, required=True)
#     password = forms.CharField(required=True, widget=forms.PasswordInput)
#     stud = forms.BooleanField(required=False, label= "Are you a school student?")

# class PasswordResetForm(forms.Form):
#     email = forms.EmailField(required = True, max_length= 200)

# class SetNewPassword(forms.ModelForm):
#     new_password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = Student
#         fields = []  # No direct model fields here, password handled manually

#     def clean(self):
#         cleaned_data = super().clean()
#         new_password = cleaned_data.get("new_password")
#         confirm_password = cleaned_data.get("confirm_password")
#         if new_password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")
#         return cleaned_data

#     def save(self, commit=True):
#         student = self.instance
#         student.password = make_password(self.cleaned_data["new_password"])
#         if commit:
#             student.save()
#         return student





from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm
import uuid
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.conf import settings
import requests


class RecaptchaWidget(forms.Widget):
   def render(self, name, value, attrs=None, renderer=None):
        return f'''
        <script src="https://www.google.com/recaptcha/api.js" async defer></script>
        <button class="submit-btn g-recaptcha"
                data-sitekey="{settings.RECAPTCHA_PUBLIC_KEY}"
                data-callback="onSubmit"
                data-action="submit">
            Register
        </button>
        '''

class RecaptchaField(forms.CharField):
    widget = RecaptchaWidget
    
    def __init__(self, *args, **kwargs):
        kwargs['required'] = True
        super().__init__(*args, **kwargs)
    
    def validate(self, value):
        super().validate(value)
        if not self.verify_recaptcha(value):
            raise ValidationError('reCAPTCHA verification failed')
    
    def verify_recaptcha(self, token):
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
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    school_student = forms.BooleanField(required=False,label="Are you a school student?" )
    recaptcha_token = RecaptchaField(required=True)
    class Meta:
        model  = Student
        fields = ('username', 'email', 'password1', 'password2', 'school_student')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email_token = uuid.uuid4()
        user.is_verified = False
        user.school_student = self.cleaned_data.get('school_student', False)
        if commit: 
            user.save()
        return user
    
class SigninForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    stud = forms.BooleanField(required=False, label="Are you a school student?")


class PasswordResetForm(forms.Form):
    email = forms.EmailField(required = True, max_length= 200)

class SetNewPassword(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, student):
        student.password = make_password(self.cleaned_data["new_password"])
        student.save()
        return student
    
class PdfSummarizerForm(forms.Form):
    pdf = forms.FileField(required=True, label="Please upload your PDF")



class QuizPreferenceForm(forms.Form):
    topic = forms.CharField(
        label="Enter Topic",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'like: Python, Aviation, History, etc...'
    }),
    )

    number_of_questions = forms.IntegerField(
        label="Number of Questions",
        required=True,
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 5, 10, 15'
        })
    )

    timer = forms.IntegerField(
        label="Quiz Duration (minutes)",
        required=False,
        min_value=1,
        max_value=60,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 5, 10 (optional)'
        })
    )

    difficulty = forms.ChoiceField(
        label="Select Difficulty",
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    type_of_questions = forms.ChoiceField(
        label="Type of Questions",
        choices=[
            ('mcq', 'Multiple Choice'),
            ('true_false', 'True/False'),
            ('fill_blank', 'Fill in the Blank')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )



# class DynamicQuizForm(forms.Form):
#     def __init__(self, questions, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i, q in enumerate(questions):
#             choices = [(opt, opt) for opt in q['options']]
#             self.fields[f'q_{i}'] = forms.ChoiceField(
#                 label=q['question'],
#                 choices=choices,
#                 widget=forms.RadioSelect,
#                 required=True
#             )

class DynamicQuizForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, q in enumerate(questions):
            self.fields[f'q_{i}'] = forms.ChoiceField(
                label=q['question'],
                choices=q['options'],  # already (value, label)
                widget=forms.RadioSelect,
                required=True
            )

