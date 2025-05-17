from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging

# Create a custom token generator for the Student model
class StudentTokenGenerator:
    def make_token(self, student):
        """
        Creates a token for a Student instance
        """
        return student.email_token.hex
    
    def check_token(self, student, token):
        """
        Checks if the token matches the student's email token
        """
        return student.email_token.hex == token

student_token_generator = StudentTokenGenerator()

def send_email(student, request):
    try:
        uid = urlsafe_base64_encode(force_bytes(student.pk))
        
        token = str(student.email_token)
        
        verification_url = request.build_absolute_uri(f'/verify/{uid}/{token}/')
        
        subject = "Welcome to EduGenie, verify your email"
        message = (
            f"Hi {student.name}, thanks for choosing EduGenie!\n\n"
            f"Please click the link below to verify your email and activate your account:\n"
            f"{verification_url}\n\n"
            f"If you did not sign up, please ignore this email."
        )
        
        email_from = settings.EMAIL_HOST_USER
        
        recipient_list = [student.email]
        
        logging.info(f"Sending verification email to {student.email}")
        logging.info(f"Verification URL: {verification_url}")
        
        # Send the email
        send_result = send_mail(
            subject=subject,
            message=message,
            from_email=email_from,
            recipient_list=recipient_list,
            fail_silently=False 
        )
        
        if send_result:
            logging.info(f"Email sent successfully to {student.email}")
        else:
            logging.error(f"Failed to send email to {student.email}")
        
        return send_result
        
    except Exception as e:
        logging.error(f"Email sending failed: {str(e)}")
        raise e