from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('sign_up/', views.signup, name='sign_up'),
    path('sign_in/', views.signin, name = "sign_in" ),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('testimonials/', views.show_testimonials, name='testimonials'),
    path('chat/', views.chat_page, name='chat'),
    path('get-response/', views.chat_response, name='get_response'),
    path('stud/', views.stud, name='stud'),
    path('intern/', views.professional, name='interns'),
    path('logout/', views.logoutUser, name= 'logoutUser'),
    path('contact_us/', views.contact, name='contact_us'),
    path('pdf_summarizer/', views.pdf_summarizer, name='pdf_summarizer'),
    path('quiz_preference/', views.quiz_preference, name='quiz_preference'),
    path('render_quiz/', views.render_quiz, name='render_quiz'),
    path('resume_tester/', views.resume_tester, name='resume_tester'),
    path('submit_testimonial/', views.testimonial_submit, name='submit_testimonial'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name= 'password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'pass_set.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'set_password.html'), name='password_reset_complete'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
1. Submit email form => PasswordResetView.as_view()
2. Email sent to user with reset link => PasswordResetDoneView.as_view()
3. User clicks link, goes to reset password page => PasswordResetConfirmView.as_view()
4. Password reset successful, redirect to login page => PasswordResetCompleteView.as_view()
'''