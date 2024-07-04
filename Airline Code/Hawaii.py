import pandas as pd
import os
import re

# Define the raw data
raw_data = """

"""

# Split the data into lines
lines = raw_data.split('\n')
data = []

# Initialize variables for processing
airline = airline_code = flight = to = sched = updated = None
status_keywords = {"In", "Arrived", "Scheduled", "Delayed", "Landed", "No", "Departed","Cancelled"}

def is_flight_number(s, airline_code):
    return s.startswith(airline_code) and any(char.isdigit() for char in s)

def extract_to_and_status(parts):
    combined = ' '.join(parts)
    for keyword in status_keywords:
        if keyword in combined:
            to_part, status_part = combined.split(keyword, 1)
            return to_part.strip(), keyword, status_part.strip()
    return combined, "", ""

def extract_times(remaining):
    time_pattern = r'\d{1,2}:\d{2} [AP]M'
    times = re.findall(time_pattern, remaining)
    return times

for i, line in enumerate(lines):
    parts = line.split()

    if not parts:
        continue  # Skip empty lines

    # Determine if the current line could be an airline line
    if i + 1 < len(lines) and parts and lines[i + 1].split() and is_flight_number(lines[i + 1].split()[0], parts[0]):
        # Airline name and code from the first part of the current line
        airline = line
        airline_code = parts[0]

    elif airline_code and parts and is_flight_number(parts[0], airline_code):
        # Flight number
        flight = parts[0]
    else:
        # Extract To and Status
        to, status, remaining = extract_to_and_status(parts)

        # Ensure 'To' contains a comma
        if ',' not in to:
            continue

        # Identify schedule and updated times
        times = extract_times(remaining)

        if len(times) >= 2:
            sched = times[0]
            updated = times[1]
        elif len(times) == 1:
            sched = times[0]
            updated = ""

        # Add row to data
        data.append([airline_code, flight, to, sched, updated])
        # Reset variables for next entry
        flight = to = sched = updated = None

# Define column names
columns = ['Airline', 'Flight', 'To', 'Sched.', 'Updated']

# Create a DataFrame
df = pd.DataFrame(data, columns=columns)

# Define the path to the Downloads directory
downloads_directory = os.path.expanduser('~/Hawaii')
os.makedirs(downloads_directory, exist_ok=True)

# Define the full path to the CSV file and Excel file
csv_file = os.path.join(downloads_directory, 'Daniel_0702_2024.csv')
excel_file = os.path.join(downloads_directory, 'Daniel_0702_2024.xlsx')

# Save the DataFrame to a CSV file
df.to_csv(csv_file, index=False)
print(f"Data has been written to {csv_file}")

# Save the DataFrame to an Excel file
df.to_excel(excel_file, index=False)
print(f"Data has been written to {excel_file}")