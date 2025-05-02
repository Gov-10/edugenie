from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length = 120)
    email = models.EmailField(max_length = 120, unique = True)
    password = models.CharField(max_length = 120)
    school_student = models.BooleanField(default = False)

    def __str__(self):
        return self.name
