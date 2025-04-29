from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee

# View to create a new employee
def employee_form(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('employee_name')
        employee_id = request.POST.get('employee_id')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        designation = request.POST.get('designation')
        joining_date = request.POST.get('joining_date')
        salary_per_day = request.POST.get('salary_per_day')
        salary_per_hour = request.POST.get('salary_per_hour')
        early_logouts_late_logins = request.POST.get('early_logouts_late_logins')
        days_to_deduct = request.POST.get('days_to_deduct')

        # Input validation
        if not all([name, employee_id, email, contact, designation, joining_date, salary_per_day, salary_per_hour, early_logouts_late_logins, days_to_deduct]):
            messages.error(request, "All fields are required.")
            return render(request, 'employee/employee_form.html')

        # Save data to the database
        try:
            Employee.objects.create(
                name=name,
                employee_id=employee_id,
                email=email,
                contact=contact,
                designation=designation,
                joining_date=joining_date,
                salary_per_day=float(salary_per_day),
                salary_per_hour=float(salary_per_hour),
                early_logouts_late_logins=int(early_logouts_late_logins),
                days_to_deduct=int(days_to_deduct)
            )
            messages.success(request, "Employee added successfully.")
            return redirect('employee_list')  # Redirect to the employee list page
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
        employee_name = request.POST.get('employee_name')
        employee_id = request.POST.get('employee_id')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        designation = request.POST.get('designation')
        joining_date = request.POST.get('joining_date')
        salary_per_day = request.POST.get('salary_per_day')
        salary_per_hour = request.POST.get('salary_per_hour')
        early_logouts_late_logins = request.POST.get('early_logouts_late_logins')
        days_to_deduct = request.POST.get('days_to_deduct')

        # Input validation
        if not all([employee_name, employee_id, email, contact, designation, joining_date, salary_per_day, salary_per_hour, early_logouts_late_logins, days_to_deduct]):
            messages.error(request, "All fields are required.")
            return render(request, 'employee/update_employee.html', {'employee': employee})

        try:
            # Update employee details
            employee.name = employee_name
            employee.employee_id = employee_id
            employee.email = email
            employee.contact = contact
            employee.designation = designation
            employee.joining_date = joining_date
            employee.salary_per_day = float(salary_per_day)
            employee.salary_per_hour = float(salary_per_hour)
            employee.early_logouts_late_logins = int(early_logouts_late_logins)
            employee.days_to_deduct = int(days_to_deduct)

            employee.save()  # Save updated data
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
