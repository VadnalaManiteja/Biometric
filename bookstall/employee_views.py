from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee

# View to create a new employee
def employee_form(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('employee_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        designation = request.POST.get('designation')
        joining_date = request.POST.get('joining_date')
        salary = request.POST.get('salary')

        # Input validation
        if not all([name, email, contact, designation, joining_date, salary]):
            messages.error(request, "All fields are required.")
            return render(request, 'employee/employee_form.html')

        # Save data to the database
        try:
            Employee.objects.create(
                name=name,
                email=email,
                contact=contact,
                designation=designation,
                joining_date=joining_date,
                salary=int(salary),
            )
            messages.success(request, "Employee added successfully.")
            return redirect('employee_list')  # Redirect to the list page
        except Exception as e:
            messages.error(request, f"Error adding employee: {e}")
    
    return render(request, 'employee/employee_form.html')


# View to list all employees
def employee_list_view(request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee_list.html', {'employees': employees})


# View to update an existing employee
def update_employee_view(request, pk):
    # Retrieve the employee object
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        # Update employee details from the form
        name = request.POST.get('employee_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        designation = request.POST.get('designation')
        joining_date = request.POST.get('joining_date')
        salary = request.POST.get('salary')

        # Input validation
        if not all([name, email, contact, designation, joining_date, salary]):
            messages.error(request, "All fields are required.")
            return render(request, 'employee/update_employee.html', {'employee': employee})

        try:
            employee.name = name
            employee.email = email
            employee.contact = contact
            employee.designation = designation
            employee.joining_date = joining_date
            employee.salary = int(salary)
            employee.save()  # Triggers per-day and per-hour wage calculation
            messages.success(request, "Employee updated successfully.")
            return redirect('employee_list')  # Redirect to the employee list
        except Exception as e:
            messages.error(request, f"Error updating employee: {e}")

    # Render the update form with the current employee details
    return render(request, 'employee/update_employee.html', {'employee': employee})


# View to delete an employee
def delete_employee_view(request, pk):
    # Retrieve and delete the employee object
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')  # Redirect to the employee list
