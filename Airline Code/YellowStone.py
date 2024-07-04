import pandas as pd
import os

# Define the raw data
raw_data = """Delta	4314	SLC	1:15 PM	2:32 PM	May 06
Delta	4314	SLC	1:15 PM	2:32 PM	May 07
Delta	4314	SLC	1:15 PM	2:32 PM	May 08
Delta	4314	SLC	1:15 PM	2:32 PM	May 09
Delta	4314	SLC	1:15 PM	2:32 PM	May 10
Delta	4314	SLC	1:15 PM	2:32 PM	May 11
Delta	4314	SLC	1:15 PM	2:32 PM	May 12
Delta	4314	SLC	1:15 PM	2:32 PM	May 13
Delta	4314	SLC	1:15 PM	2:32 PM	May 14
Delta	4314	SLC	1:15 PM	2:32 PM	May 15
Delta	4314	SLC	1:15 PM	2:32 PM	May 16
Delta	4314	SLC	1:15 PM	2:32 PM	May 17
Delta	4314	SLC	1:15 PM	2:32 PM	May 18
Delta	4314	SLC	1:15 PM	2:32 PM	May 19
Delta	4314	SLC	11:45 AM	1:00 PM	May 20
Delta	4313	SLC	3:30 PM	4:40 PM	May 20
Delta	4314	SLC	11:45 AM	1:00 PM	May 21
Delta	4314	SLC	11:45 AM	1:00 PM	May 22
Delta	4314	SLC	11:45 AM	1:00 PM	May 23
Delta	4313	SLC	3:30 PM	4:40 PM	May 23
Delta	4314	SLC	11:45 AM	1:00 PM	May 24
Delta	4313	SLC	3:30 PM	4:40 PM	May 24
Delta	4314	SLC	11:45 AM	1:00 PM	May 25
Delta	4313	SLC	3:30 PM	4:40 PM	May 25
Delta	4314	SLC	11:45 AM	1:00 PM	May 26
Delta	4313	SLC	3:30 PM	4:40 PM	May 26
Delta	4314	SLC	11:45 AM	1:00 PM	May 27
Delta	4313	SLC	3:30 PM	4:40 PM	May 27
Delta	4314	SLC	11:45 AM	1:00 PM	May 28
Delta	4314	SLC	11:45 AM	1:00 PM	May 29
Delta	4314	SLC	11:45 AM	1:00 PM	May 30
Delta	4313	SLC	3:30 PM	4:40 PM	May 30
Delta	4314	SLC	11:45 AM	1:00 PM	May 31
Delta	4313	SLC	3:30 PM	4:40 PM	May 31"""

# Process the raw data
lines = raw_data.split('\n')
data = []
for line in lines:
    parts = line.split()
    airline = parts[0]
    flight_number = parts[1]
    destination = parts[2]
    departure_time = ' '.join(parts[3:5])
    arrival_time = ' '.join(parts[5:7])
    date = ' '.join(parts[7:])
    data.append([airline, flight_number, destination, departure_time, arrival_time, date])

# Define column names
columns = ['Airline', 'Flight Number', 'Destination', 'Departure Time', 'Arrival Time', 'Date']

# Create a DataFrame
df = pd.DataFrame(data, columns=columns)

# Define the path to the Downloads directory
downloads_directory = os.path.expanduser('~/YellowStone/Departure')

# Create the Downloads directory if it doesn't exist
os.makedirs(downloads_directory, exist_ok=True)

# Define the full path to the CSV file
csv_file = os.path.join(downloads_directory, 'Yellow-May-24.csv')

# Save the DataFrame to a CSV file
df.to_csv(csv_file, index=False)

print(f"Data has been written to {csv_file}")
