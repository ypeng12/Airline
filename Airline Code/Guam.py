import pandas as pd
import os
import re

# Define the new raw data
new_raw_data = """"""

# Split the new data into lines
lines = new_raw_data.split('\n')
data = []

def find_flight_number(parts):
    for i, part in enumerate(parts):
        if re.match(r'[A-Za-z]+\d+', part):
            return i
    return -1

# Function to find the first time format (XX:XX) from the back of the list
def find_times_from_back(parts):
    times = [part for part in parts if re.match(r'^\d{1,2}:\d{2}$', part)]
    if len(times) >= 2:
        return times[-2], times[-1]
    return None, None

# Extract data from each line
for line in lines:
    parts = line.split()
    
    # Extract the date
    date_parts = []
    for i, part in enumerate(parts):
        date_parts.append(part)
        if part == "2024":
            date = ' '.join(date_parts)
            break

    # Find the index of the flight number
    flight_no_index = find_flight_number(parts)
    if flight_no_index == -1:
        continue

    flight_no = parts[flight_no_index]
    
    # Find departure and estimated times
    departure_time, estimated_time = find_times_from_back(parts)
    
    if departure_time is None or estimated_time is None:
        continue
    
    # The TO part is between flight number and departure time
    to_end_index = parts.index(departure_time)
    destination = ' '.join(parts[flight_no_index + 1:to_end_index])
    
    # Append extracted data to the list
    data.append([date, flight_no, destination, departure_time, estimated_time])

# Define column names
columns = ['DATE', 'FLIGHT NO.', 'To', 'DEPARTURE TIME', 'ESTIMATED TIME']

# Create a DataFrame
df_new = pd.DataFrame(data, columns=columns)

# Define the path to the Downloads directory
downloads_directory = os.path.expanduser('~/Guam')
os.makedirs(downloads_directory, exist_ok=True)

# Define the full path to the CSV file
# Sorting at 13:30 pct
csv_file_new = os.path.join(downloads_directory, 'Guam_0704_2024.csv')
excel_file_new = os.path.join(downloads_directory, 'Guam_0704_2024.xlsx')

# Save the new DataFrame to a CSV file
df_new.to_csv(csv_file_new, index=False)
print(f"New flight data has been written to {csv_file_new}")

# Save the new DataFrame to an Excel file
df_new.to_excel(excel_file_new, index=False)
print(f"New flight data has been written to {excel_file_new}")
