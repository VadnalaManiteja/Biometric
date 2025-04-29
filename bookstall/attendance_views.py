
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

        if ":" in employee_data:
            employee_id, employee_name = employee_data.split(":")
            employee_id = employee_id.strip()
            employee_name = employee_name.strip()

            # Fetch employee details from the database
            filtered_employees = Employee.objects.filter(name=employee_name)
            if filtered_employees.exists():
                employee = filtered_employees.first()

                # Extract dynamic values from the Employee model
                salary_per_day = float(employee.salary_per_day or 0)
                salary_per_hour = float(employee.salary_per_hour or 0)
                days_to_deduct = int(employee.days_to_deduct or 1)  # Default to 1 to avoid division by zero

                print(f"{employee_name}'s details: Salary per day: {salary_per_day}, Salary per hour: {salary_per_hour}, Days to deduct: {days_to_deduct}")
            
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
                late_by_days_and_early_going_by_days = int(late_by_days) + int(early_going_by_days)

                # Parse total OT (hours and minutes)
                hours, minutes = total_ot.split(":")
                hours = int(hours)
                minutes = int(minutes)
                total_late_and_early_out_days = int(late_by_days_and_early_going_by_days)
                deduction_days = total_late_and_early_out_days // days_to_deduct
                days_to_pay = float(present_count) - deduction_days
                amout_to_pay = days_to_pay * float(salary_per_day)
                total_ot_amount = float(hours) * float(salary_per_hour) + float(minutes) * float(salary_per_hour / 60)
                total_salary = amout_to_pay + total_ot_amount

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
                    'total_salary': int(round(total_salary)),
                    'late_by_days_and_early_going_by_days': late_by_days_and_early_going_by_days,
                    'days_to_pay': days_to_pay,
                    'salary_per_hour': salary_per_hour,
                    'salary_per_day': salary_per_day,
                    'amout_to_pay': amout_to_pay,
                    'total_ot_amount':(round(total_ot_amount)),
                }
            else:
                print(f"Employee {employee_name} not found in database.")
                return None
        else:
            print(f"Invalid employee data in row {row_num + 1}.")
            return None
    return None


# Django view function to handle file upload and process the Excel data
def attendance_upload(request):
    print("hit this view")
    results = []  # List to store the results

    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]

        try:
            # Load the workbook
            workbook = xlrd.open_workbook(file_contents=excel_file.read())

            # Select the first sheet (or specify by index or name)
            sheet = workbook.sheet_by_index(0)
            print("Sheet Name:", sheet)
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
