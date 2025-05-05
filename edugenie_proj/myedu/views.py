from django.shortcuts import render,redirect
from .forms import SignupForm, SigninForm
from .models import Student
# Create your views here.
def home(request):
    return render(request, 'home.html')
def about_us(request):
    return render(request, 'about_us.html')
def signup(request):
    if request.method == 'POST':
       form = SignupForm(request.POST or None)
       if form.is_valid():
          form.save()
          is_student = form.cleaned_data.get('school_student')
          if is_student:
            return render(request, 'stud.html', {'form': form, 'success': True})
          else:
            return render(request, 'new.html', {'form': form, 'success': True})
       else:
            return render(request, 'sign_up.html', {'form': form}) 
    else:
        form = SignupForm() 
        return render(request, 'sign_up.html', {'form': form})
    
def signin(request):
   if request.method == "POST":
      form = SigninForm(request.POST or None)
      if form.is_valid():
          name = form.cleaned_data.get('name')
          password = form.cleaned_data.get('password')
          stud = form.cleaned_data.get('stud')  # Checkbox value
          try:
             student = Student.objects.get(name=name, password=password)
             if stud:  # If checkbox is ticked
                return render(request, 'stud.html', {'form': form, 'success': True})
             else:  # If checkbox is not ticked
                return render(request, 'new.html', {'form': form, 'success': True})
          except Student.DoesNotExist:
             form.add_error(None, "Invalid username or password")
      return render(request, 'sign_in.html', {'form': form})
   else:
      form = SigninForm()
      return render(request, 'sign_in.html', {'form': form})
