from django.shortcuts import render
from .forms import SignupForm
# Create your views here.
def home(request):
    return render(request, 'home.html')
def about_us(request):
    return render(request, 'about_us.html')
def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'sign_up.html', {'form': form})
