from django import forms
from .models import Student

class SignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 
            'email', 
            'password', 
            'school_student'
        ]
