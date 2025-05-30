from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('sign_up/', views.signup, name='sign_up'),
    path('sign_in/', views.signin, name = "sign_in" ),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('reset_password/', views.passwordreset, name='reset_password_request'),
    path('reset/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
 
]


'''
1. Submit email form => PasswordResetView.as_view()
2. Email sent to user with reset link => PasswordResetDoneView.as_view()
3. User clicks link, goes to reset password page => PasswordResetConfirmView.as_view()
4. Password reset successful, redirect to login page => PasswordResetCompleteView.as_view()
'''