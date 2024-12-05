from .models import Employee
from django.shortcuts import render, redirect

def employee_form(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('employee_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        designation = request.POST.get('designation')
        joining_date = request.POST.get('joining_date')

        # Save data to the database
        Employee.objects.create(
            name=name,
            email=email,
            contact=contact,
            designation=designation,
            joining_date=joining_date,
        )
        return redirect('employee_list')  # Redirect to the list page

    return render(request, 'employee/employee_form.html')

def employee_list_view(request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee_list.html', {'employees': employees})

from django.shortcuts import render, get_object_or_404, redirect

def update_employee_view(request, pk):
    # Retrieve the employee object
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        # Update employee details from the form
        employee.name = request.POST.get('employee_name')
        employee.email = request.POST.get('email')
        employee.contact = request.POST.get('contact')
        employee.designation = request.POST.get('designation')
        employee.joining_date = request.POST.get('joining_date')
        employee.save()  # Save changes to the database
        return redirect('employee_list')  # Redirect to the employee list
    
    # Render the update form with the current employee details
    return render(request, 'employee/update_employee.html', {'employee': employee})


def delete_employee_view(request, pk):
    # Retrieve and delete the employee object
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')  # Redirect to the employee list