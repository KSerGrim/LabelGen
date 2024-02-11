import csv
import json
import requests
import unittest
# import pandas as pd

from datetime import datetime
from format_header import searchingHeaders, default_headers, formatted_headers
from credentials import creds, BASE_URL, API_TOKEN

""" Label Gen"""
def txt_to_csv(txt_file_path, csv_file_path, delimiter):
    with open(txt_file_path, 'r') as txt_file, open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = next(txt_file).strip().split(delimiter)  # Read the first line to get the header
        csv_writer.writerow(header)  # Write the header to the CSV
        
        quantity_to_ship_index = header.index("quantity-to-ship")  # Find the index of the 'quantity-to-ship' column
        
        for line in txt_file:
            # Split each line by the delimiter to get individual fields
            fields = line.strip().split(delimiter)
            quantity_to_ship = int(fields[quantity_to_ship_index])  # Convert the quantity to an integer
            
            if quantity_to_ship > 1:
                # Split the order into multiple rows based on the 'quantity-to-ship'
                for _ in range(quantity_to_ship):
                    # Adjust the quantity to 1 for each split order
                    fields_copy = fields.copy()
                    fields_copy[quantity_to_ship_index] = '1'
                    csv_writer.writerow(fields_copy)
            else:
                # If 'quantity-to-ship' is not more than 1, write the row as is
                csv_writer.writerow(fields)
    print(f"Excel file '{csv_file_path}' created successfully.")

def copy_rows_based_on_header(source_csv_path, csv_file_path):
    with open(source_csv_path, mode='r', newline='') as source_file:
        reader = csv.DictReader(source_file)
        headers = reader.fieldnames
    
        with open(csv_file_path, mode='w', newline='') as target_file:
            csv_writer = csv.writer(target_file)
            # Read headers from the source worksheet
            csv_writer.writerow(formatted_headers.keys())
            
            # Iterate over each row in the source CSV file
            for row in reader:
                # Initialize a list to hold the row data according to formatted_headers
                row_data = []
                for header in formatted_headers.keys():
                    # If the header is found in the source CSV, use that value
                    if header in row:
                        row_data.append(row[header])
                    # Otherwise, use the default value if specified in formatted_headers, else from default_headers
                    else:
                        row_data.append(formatted_headers.get(header, default_headers.get(header, "")))
                
                # Write the constructed row to the target CSV file
                csv_writer.writerow(row_data)
                    
        print(f"Data copied to '{csv_file_path}' successfully.")

def correct_csv_headers(source_csv_path, corrected_csv_path):
    """
    Correct specific headers in a CSV file.

    :param source_csv_path: Path to the source CSV file.
    :param corrected_csv_path: Path to save the corrected CSV file.
    :param header_corrections: A dictionary mapping old headers to new headers.
    """
    with open(source_csv_path, mode='r', newline='') as source_file:
        reader = csv.reader(source_file)
        headers = next(reader)  # Read the original headers
        
        # Correct the headers
        corrected_headers = [searchingHeaders.get(header, header) for header in headers]
        
        with open(corrected_csv_path, mode='w', newline='') as corrected_file:
            writer = csv.writer(corrected_file)
            writer.writerow(corrected_headers)  # Write the corrected headers
            
            # Write the remaining rows unchanged
            for row in reader:
                writer.writerow(row)

    print(f"Headers corrected and data saved to '{corrected_csv_path}'.")

def csv_to_json(csv_file_path, json_file_path):
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', newline='') as csv_file:
        # Create a CSV reader
        reader = csv.DictReader(csv_file)
        amazon_order_list = []
        # Convert each row into the specified JSON structure
        # Assuming each row in the CSV corresponds to one JSON object like the example
        for row in reader:
            formatted_data = {
                "provider_code": row.get("provider", ""),
                "class": row.get("class", ""),
                "weight": int(row.get("weight", 0)),
                "notes": row.get("notes", ""),
                "length": int(row.get("length", 0)),
                "width": int(row.get("width", 0)),
                "height": int(row.get("height", 0)),
                "from_name": row.get("from_name", ""),
                "from_phone": row.get("from_phone", ""),
                "from_address1": row.get("from_address1", ""),
                "from_address2": row.get("from_address2", ""),
                "from_city": row.get("from_city", ""),
                "from_state": row.get("from_state", ""),
                "from_postcode": row.get("from_postcode", ""),
                "from_country": row.get("from_country", ""),
                "to_name": row.get("to_name", ""),
                "to_phone": row.get("to_phone", ""),
                "to_address1": row.get("to_address1", ""),
                "to_address2": row.get("to_address2", ""),
                "to_address3": row.get("to_address3", ""),
                "to_city": row.get("to_city", ""),
                "to_state": row.get("to_state", ""),
                "to_postcode": row.get("to_postcode", ""),
                "to_country": row.get("to_country", "")
            }
            amazon_order_list.append(formatted_data)
            # Open the JSON file for writing
        with open(json_file_path, mode='w', newline='') as json_file:
                # Write the formatted data to the JSON file
            json.dump(amazon_order_list, json_file, indent=4)
                
            # print(f"Data from '{csv_file_path}' was successfully written to '{json_file_path}'.")
            
# def create_final_data_row(formatted_headers, default_headers, acquired_data):
#     final_data_row = {}

#     # Iterate through each header in formatted_headers to maintain order
#     for header in formatted_headers.keys():
#         # If acquired_data contains the header, use that value
#         if header in acquired_data:
#             final_data_row[header] = acquired_data[header]
#         # Otherwise, if default_headers contains the header, use the default value
#         elif header in default_headers:
#             final_data_row[header] = default_headers[header]
#         # If the header isn't in acquired_data or default_headers, use the value from formatted_headers
#         else:
#             final_data_row[header] = formatted_headers[header]

#     return final_data_row
# def write_data_to_csv(data, csv_file_path):
#     wb = openpyxl.Workbook()
#     ws = wb.active
        
#     # Write the headers to the first row
#     ws.append(headers)
    
#     # Open the CSV file for writing
#     with open(csv_file_path, 'w', newline='') as csv_file:
#         writer = csv.writer(csv_file)
        
#         writer.writerow(list(formatted_headers))  # Write headers
#         # for row in data:
#             # row_data = [row.get(header, default_headers.get(header, "")) for header in formatted_headers]
#             # writer.writerow(row_data)
    
#     # Save the workbook
#     wb.save(excel_file_path)
#     print(f"Formatted Excel file '{excel_file_path}' created successfully.")
# def view_excel_sheet(excel_file_path, sheet_name=None):
#     # Load the Excel file into a pandas DataFrame
#     # If sheet_name is None, pandas will load the first sheet by default
#     df = pd.read_excel(excel_file_path, sheet_name=sheet_name, engine='openpyxl')
    
    
#     # Print the DataFrame to view its contents
#     print(df)

""" Global Variables """
today_str = datetime.now().strftime('%Y-%m-%d')
txt_file_path = 'C:/Users/Patrick/Downloads/83698219468019761.txt'
csv_file_path = f'{today_str}-input_data.csv'
new_csv_file_path = f'{today_str}-output_data.csv'
final_csv_file_path = f'{today_str}-shipd_data.csv'
json_file_path = 'data.json'

endpoint = "providers" #bulk-orders

class ShipdAPITest(unittest.TestCase):
    def test_api_call(self):
        """Test an API call to Shipd.io"""
        url = f"{creds[BASE_URL]}/{endpoint}"
        headers = {'Auth': f'{creds[API_TOKEN]}'}
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Request was successful!")
            print("Response:", response.json())  # Assuming the response is in JSON format
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            
        
        

if __name__ == '__main__':
    unittest.main()

""" Calling Functions """
txt_to_csv(txt_file_path, csv_file_path, '\t')
copy_rows_based_on_header(csv_file_path, new_csv_file_path)
correct_csv_headers(new_csv_file_path, final_csv_file_path)
csv_to_json(final_csv_file_path, json_file_path)
# view_excel_sheet(csv_file_path)

