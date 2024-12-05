from .models import Employee
from django.shortcuts import render
import xlrd



def attendance_upload(request):
    results = []  # List to store the results

    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]

        try:
            # Load the workbook
            workbook = xlrd.open_workbook(file_contents=excel_file.read())

            # Select the first sheet (or specify by index or name)
            sheet = workbook.sheet_by_index(0)

            # Function to process rows for Employee ID, Name, and Attendance
            def process_rows(start_row, sheet):
                try:
                    employee_row = start_row  # Row containing employee ID and name
                    attendance_row = start_row + 1  # Row containing attendance data

                    # Check if the rows exist
                    if sheet.nrows > employee_row and sheet.nrows > attendance_row:
                        # Extract employee ID and name
                        employee_data = sheet.row_values(employee_row)[3]  # Assuming data is in the 4th column
                        if ":" in employee_data:
                            parts = employee_data.split(":")
                            employee_id = parts[0].strip()
                            employee_name = parts[1].strip()
                        else:
                            print(f"No valid employee data found in row {employee_row + 1}")
                            return
                        
                        details_string = sheet.row_values(employee_row)[8]  # Assuming data is in 9th column
                        
                        # Function to extract specific information from the details string
                        def extract_value(details, keyword):
                            keyword = keyword.lower()  # Ensure case insensitivity
                            parts = details.lower().split(keyword)  # Split on the keyword
                            if len(parts) > 1:
                                # Extract the part after the keyword and take the first number
                                value_part = parts[1].split()  # Split the remaining part by spaces
                                return value_part[0]  # Return the first part (the value)
                            return None  # Return None if the keyword isn't found
                        
                        # Extract "Late By Days" and "Early Going By Days"
                        late_by_days = extract_value(details_string, "Late By Days:")
                        early_going_by_days = extract_value(details_string, "Early going By Days:")
                        
                        # Extract attendance data
                        attendance_data = sheet.row_values(attendance_row)
                        valid_statuses = [item for item in attendance_data if item in {"A", "WO", "P", "½P"}]

                        # Count occurrences
                        absent_count = valid_statuses.count("A")
                        week_off_count = valid_statuses.count("WO")
                        present_count = valid_statuses.count("P") + (valid_statuses.count("½P") * 0.5)

                        # Append results to the results list
                        results.append({
                            'employee_id': employee_id,
                            'employee_name': employee_name,
                            'late_by_days': late_by_days,
                            'early_going_by_days': early_going_by_days,
                            'absent_count': absent_count,
                            'week_off_count': week_off_count,
                            'present_count': present_count
                        })

                except Exception as e:
                    print(f"Error processing rows {start_row} and {start_row + 1}: {e}")

            # Loop through the rows in steps of 10 (21-22, 31-32, etc.)
            for start_row in range(10, sheet.nrows, 10):
                process_rows(start_row, sheet)

            # Pass results to the template
            return render(request, 'attendance/attendance_upload.html', {'results': results})

        except Exception as e:
            # If there is any issue with the file, show an error
            return render(request, 'attendance/attendance_upload.html', {'error': f"Error processing the file: {e}"})

    return render(request, 'attendance/attendance_upload.html')
