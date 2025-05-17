from django import forms
from .models import Student
from django.contrib.auth.hashers import make_password

class SignupForm(forms.ModelForm):
    password = forms.CharField(max_length=128,widget=forms.PasswordInput, label="Password")
    school_student = forms.BooleanField(required=False,label="Are you a school student?")
    class Meta:
        model = Student
        fields = [
            'name', 
            'email', 
            'password', 
            'school_student'
        ]
    def save(self, commit=True):
        student = super().save(commit=False)
        student.password = make_password(self.cleaned_data['password'])
        if not student.email_token:
            import uuid
            student.email_token = uuid.uuid4()
        student.is_verified = False
        if commit:
            student.save()
        return student
        
class SigninForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    stud = forms.BooleanField(required=False, label= "Are you a school student?")


