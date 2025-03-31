#!/usr/bin/env python3
import csv
from datetime import datetime

# Define date format conversion functions
def parse_date_multi_format(date_str):
    formats = [
        '%m/%d/%y',     # 01/15/23
        '%m/%d/%Y',     # 01/15/2023
        '%Y-%m-%d',     # 2023-01-15
        '%d/%m/%y',     # 15/01/23
        '%d/%m/%Y'      # 15/01/2023
    ]
    
    for date_format in formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue
            
    raise ValueError(f'Unable to parse date: {date_str}')

# Read the existing data
data = []
with open('transactions.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames
    for row in reader:
        data.append(row)

# Update the dates
target_format = '%d/%m/%y'
updated_data = []
for row in data:
    try:
        date_str = row['Transaction Date']
        # Convert the date string to a datetime object
        date_obj = parse_date_multi_format(date_str)
        # Format it in our target format
        row['Transaction Date'] = date_obj.strftime(target_format)
    except ValueError as e:
        print(f'Error parsing date: {date_str} - {e}')
    
    updated_data.append(row)

# Write the data back to file
with open('transactions.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_data)

print('Date format standardization complete: All dates in transactions.csv converted to dd/mm/yy format') 