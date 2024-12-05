from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('Owner', 'Owner'), ('Employee', 'Employee')])

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    designation = models.CharField(max_length=50)
    joining_date = models.DateField()

    def __str__(self):
        return self.name

