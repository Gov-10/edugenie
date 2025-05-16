from django import forms
from .models import Student
from django.contrib.auth.hashers import make_password

class SignupForm(forms.ModelForm):
    password = forms.CharField(max_length=128,widget=forms.PasswordInput)
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
        if commit:
            student.save()
        return True
        

class SigninForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    stud = forms.BooleanField(required=False, label= "Are you a school student?")


