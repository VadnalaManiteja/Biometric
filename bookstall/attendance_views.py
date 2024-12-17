
import xlrd
import re
from django.shortcuts import render

# Function to extract the value after the keyword
def extract_value(details_string, keyword):
    match = re.search(rf"{keyword}[: ]*([\d:.]+)", details_string)
    if match:
        return match.group(1)
    return None
from .models import Employee

# Function to process the rows for Employee details and attendance data
def process_row(row_num, sheet):
    if row_num < sheet.nrows:
        row_data = sheet.row_values(row_num)
        employee_data = row_data[3]  # Extract employee ID and name from column 4 (index 3)
        per_day_wage = 1.0
        per_hour_wage = 1.0
        per_min_wage = 1.0

        # Extract employee ID and name
        if ":" in employee_data:
            employee_id, employee_name = employee_data.split(":")
            employee_id = employee_id.strip()
            employee_name = employee_name.strip()
            filtered_employees = Employee.objects.filter(name=employee_name)
            if filtered_employees.exists():
                salary = filtered_employees.first().salary
                per_day_wage = filtered_employees.first().per_day_wage
                per_hour_wage = filtered_employees.first().per_hour_wage
                per_min_wage = filtered_employees.first().per_min_wage
                print(f"{employee_name}'s salary is: {salary} {per_day_wage} {per_hour_wage} {per_min_wage}")
            
            # Extract other details from the details string (index 8 in the row)
            details_string = row_data[8]
            total_work_duration = extract_value(details_string, "Total Work Duration")
            total_ot = extract_value(details_string, "Total OT")
            present_count = extract_value(details_string, "Present")
            absent_count = extract_value(details_string, "Absent")
            week_off_count = extract_value(details_string, "WeeklyOff")
            holidays = extract_value(details_string, "Holidays")  # New field
            leaves_taken = extract_value(details_string, "Leaves Taken")  # New field
            late_by_hours = extract_value(details_string, "Late By Hrs")
            late_by_days = extract_value(details_string, "Late By Days")
            early_by_hours = extract_value(details_string, "Early By Hrs")
            early_going_by_days = extract_value(details_string, "Early going By Days")
            total_duration_ot = extract_value(details_string, "Total Duration\\(\\+OT\\)")
            avg_working_hours = extract_value(details_string, "Average Working Hrs")

            # Parse total OT (hours and minutes)
            hours, minutes = total_ot.split(":")
            hours = int(hours)
            minutes = int(minutes)

            # Calculate total salary
            total_salary = float(present_count) * float(per_day_wage)
            total_salary += (float(hours) * float(per_hour_wage)) + (float(minutes) * float(per_min_wage))
            
            # Deduct salary for late and early going days
            late_deductions = int(float(late_by_days) // 4)  # 1 day salary deducted for every 4 late days
            early_deductions = int(float(early_going_by_days) // 2)  # 1 day salary deducted for every 2 early going days
            
            total_deductions = (late_deductions + early_deductions) * float(per_day_wage)
            total_salary = total_salary - total_deductions  # Apply deductions
            
            # Print additional details if the employee is "Kumar"
            if employee_name == "Kumar":
                print(type(total_salary))
                print(type(total_deductions))
                print(f"Hours: {hours}, Minutes: {minutes}")
                print(f"Deduction Late: {late_deductions} day(s)")
                print(f"Deduction Early: {early_deductions} day(s)")
                print(f"Before Deduction Total Salary: {total_salary + total_deductions}")
                print(f"Late Deductions: {late_deductions} day(s), Early Deductions: {early_deductions} day(s)")
                print(f"Total Deductions: {total_deductions}")
                print(f"Total Salary: {total_salary}")
            
            return {
                'employee_id': employee_id,
                'employee_name': employee_name,
                'total_work_duration': total_work_duration,
                'total_ot': total_ot,
                'present_count': present_count,
                'absent_count': absent_count,
                'week_off_count': week_off_count,
                'holidays': holidays,  # New field
                'leaves_taken': leaves_taken,  # New field
                'late_by_hours': late_by_hours,
                'late_by_days': late_by_days,
                'early_by_hours': early_by_hours,
                'early_going_by_days': early_going_by_days,
                'total_duration_ot': total_duration_ot,
                'avg_working_hours': avg_working_hours,
                'total_salary': int(round(total_salary))
            }
        else:
            print(f"Invalid employee data in row {row_num + 1}.")
            return None
    return None

# Django view function to handle file upload and process the Excel data
def attendance_upload(request):
    results = []  # List to store the results

    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]

        try:
            # Load the workbook
            workbook = xlrd.open_workbook(file_contents=excel_file.read())

            # Select the first sheet (or specify by index or name)
            sheet = workbook.sheet_by_index(0)

            # Loop through the rows starting from row 10 (index 10) and step by 10 (11, 21, 31, etc.)
            for row_num in range(10, sheet.nrows, 10):  # Process row 11, 21, 31, etc.
                employee_data = process_row(row_num, sheet)

                # If data is extracted, append it to results
                if employee_data:
                    results.append(employee_data)

            # Pass results to the template
            return render(request, 'attendance/attendance_upload.html', {'results': results})

        except Exception as e:
            # If there is any issue with the file, show an error
            return render(request, 'attendance/attendance_upload.html', {'error': f"Error processing the file: {e}"})

    return render(request, 'attendance/attendance_upload.html')
