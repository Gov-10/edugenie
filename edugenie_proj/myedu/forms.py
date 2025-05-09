from django import forms
from .models import Student

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    school_student = forms.BooleanField(required=False,label="Are you a school student?")
    class Meta:
        model = Student
        fields = [
            'name', 
            'email', 
            'password', 
            'school_student'
        ]

class SigninForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    stud = forms.BooleanField(required=False, label= "Are you a school student?")

