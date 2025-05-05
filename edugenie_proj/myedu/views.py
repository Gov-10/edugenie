from django.shortcuts import render
from .forms import SignupForm, SigninForm
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