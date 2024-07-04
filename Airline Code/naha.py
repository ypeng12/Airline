import pandas as pd
import os

# Define the new raw data
new_raw_data = """MM 923 08:10 08:45
IT 231 10:10 10:40
BR 113 10:15 10:55
CI 121 11:50 12:25
MM 925 13:15 13:50 Departure 13:25 Arrival 14:00 on Tuesdays and Fridays
JX 871 15:35 16:05
MM 927 16:45 17:20
OD 883 16:50 17:30 Bound for Kuala Lumpur via Taipei / Operates on Mondays, Wednesdays, Fridays and Sundays
FD 231 16:55 17:30 Bound for Bangkok via Taipei Departure 17:35 Arrival 18:10 on Sundays
BR 185 19:55 20:30
CI 123 20:35 21:10 Operates on Tuesdays, Thursdays, Saturdays, Sundays"""

# Split the new data into lines
lines = new_raw_data.split('\n')
data = []

# Extract data from each line
for line in lines:
    parts = line.split()
    flight_no = parts[0] + " " + parts[1]
    departure_time = parts[2]
    arrival_time = parts[3]
    remarks = ' '.join(parts[4:]) if len(parts) > 4 else ''
    
    # Append extracted data to the list
    data.append([flight_no, departure_time, arrival_time, remarks])

# Define column names
columns = ['Flight No', 'Departure Time', 'Arrival Time', 'Remarks']

# Create a DataFrame
df_new = pd.DataFrame(data, columns=columns)

# Define the path to the Downloads directory
downloads_directory = os.path.expanduser('~/Okinawa')
os.makedirs(downloads_directory, exist_ok=True)

# Define the full path to the CSV file
csv_file_new = os.path.join(downloads_directory, 'Naha_intern_0704_2024.csv')
excel_file_new = os.path.join(downloads_directory, 'Naha_intern_0704_2024.xlsx')

# Save the new DataFrame to a CSV file
df_new.to_csv(csv_file_new, index=False)
print(f"Filtered flight data with remarks has been written to {csv_file_new}")

# Save the new DataFrame to an Excel file
df_new.to_excel(excel_file_new, index=False)
print(f"Filtered flight data with remarks has been written to {excel_file_new}")
