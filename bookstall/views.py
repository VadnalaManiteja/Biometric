from django.shortcuts import render

def base(request):
    return render(request, 'base.html')

from django.shortcuts import render
from .models import Employee  # Import your Employee model

def index(request):
    total_employees = Employee.objects.count()  # Count total employees
    return render(request, 'index.html', {'total_employees': total_employees})
