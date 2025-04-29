from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('Owner', 'Owner'), ('Employee', 'Employee')])

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50,unique=True,default='unknown')
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    designation = models.CharField(max_length=50)
    joining_date = models.DateField()
    salary_per_day = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    salary_per_hour = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    early_logouts_late_logins = models.PositiveIntegerField(default=0)
    days_to_deduct = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



class AttendanceRecord(models.Model):
    """
    Model to store attendance data for employees.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    late_by_days = models.PositiveIntegerField(default=0, verbose_name="Late By Days")
    early_going_by_days = models.PositiveIntegerField(default=0, verbose_name="Early Going By Days")
    absent_count = models.PositiveIntegerField(default=0, verbose_name="Absent Count")
    week_off_count = models.PositiveIntegerField(default=0, verbose_name="Week Off Count")
    present_count = models.FloatField(default=0.0, verbose_name="Present Count")  # Allows half-day precision
    record_date = models.DateField(auto_now_add=True, verbose_name="Record Date")

    def __str__(self):
        return f"Attendance for {self.employee.name} on {self.record_date}"
