# from django.db import models
# from django.contrib.auth.models import User
# import uuid

# # Create your models here.
# class Student(models.Model):
#     name = models.CharField(max_length = 120)
#     email = models.EmailField(max_length = 120, unique = True)
#     password = models.CharField(max_length = 128)
#     school_student = models.BooleanField(default = False)
#     email_token = models.UUIDField(default=uuid.uuid4)
#     is_verified = models.BooleanField(default = False)

#     def __str__(self):
#         return self.name

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Student(AbstractUser):
    school_student = models.BooleanField(default = False)
    email_token = models.UUIDField(default=uuid.uuid4)
    is_verified = models.BooleanField(default = False)
    def __str__(self):
        return self.username
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}- {self.message[:40]}"
    