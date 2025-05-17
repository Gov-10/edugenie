
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('sign_up/', views.signup, name='sign_up'),
    path('sign_in/', views.signin, name = "sign_in" ),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]