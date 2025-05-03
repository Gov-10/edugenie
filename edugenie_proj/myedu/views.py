from django.shortcuts import render
from .forms import SignupForm, SigninForm
# Create your views here.
def home(request):
    return render(request, 'home.html')
def about_us(request):
    return render(request, 'about_us.html')
def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'home.html', {'form': form, 'success': True})
    else:
        return render(request, 'sign_up.html', {'form': form})
