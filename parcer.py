import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# URL
url = ""

# request
response = requests.get(url)
response.raise_for_status()  # request status

# Create object BeautifulSoup for parcing HTML
soup = BeautifulSoup(response.text, 'html.parser')

# find classes course-brief-info__b
data_elements = soup.select('.course-brief-info__body .course-brief-info__b')

# raw data into array
rawdata = [element.get_text(strip=True).replace(' ', '') for element in data_elements if element.get_text(strip=True)]

data_sort = [
    [rawdata[0], rawdata[3], rawdata[4], rawdata[9], rawdata[12], rawdata[13]],
    [rawdata[1], rawdata[5], rawdata[6], rawdata[10], rawdata[14], rawdata[15]],
    [rawdata[2], rawdata[7], rawdata[8], rawdata[11], rawdata[16], rawdata[17]]
]

current_time_unix = int(datetime.now().timestamp())

# add date to each row
data_with_time = [[current_time_unix] + row for row in data_sort]

# arr row to str
data = [','.join(map(str, row)) for row in data_with_time]
result = '\n'.join(data)
print(f"{result}\n")

file_path = 'currency_data.csv'

# if file exist write line
write_mode = 'a' if os.path.exists(file_path) else 'w'

with open(file_path, write_mode, newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # write header if new
    if write_mode == 'w':
        writer.writerow(['Time_Unix,Currency,Sell,Buy,NBRB,Exchange,Exchange_Trading_Update_Time'])

    # write to CSV
    for value in data_with_time:
        writer.writerow(value)

print(f"Success, {file_path}")
