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

class PasswordResetForm(forms.Form):
    email = forms.EmailField(required = True, max_length= 200)

class SetNewPassword(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = []  # No direct model fields here, password handled manually

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        student = self.instance
        student.password = make_password(self.cleaned_data["new_password"])
        if commit:
            student.save()
        return student





