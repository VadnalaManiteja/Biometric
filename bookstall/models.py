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
    salary = models.PositiveIntegerField(default=0,null=True,blank=True)
    per_day_wage = models.DecimalField(max_digits=10,null=True, decimal_places=2, editable=False)
    per_hour_wage = models.DecimalField(max_digits=10, null=True,decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate per day and per hour wages
        self.per_day_wage = self.salary / 30  # Assuming 30 days in a month
        self.per_hour_wage = self.per_day_wage / 8  # Assuming 8 working hours per day
        super().save(*args, **kwargs)

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
