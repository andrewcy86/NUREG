import os
import csv
import re
from bs4 import BeautifulSoup

def extract_table_from_html(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all tables in the HTML content
    tables = soup.find_all('table')
    
    table_count = len(tables)
    # Extract data from each table
    rows = []

    if table_count == 1:
        for table in tables:
            # Extract data from each row in the table
            for row in table.find_all('tr'):
                cells = [cell.get_text(strip=True).encode('ascii', 'ignore').decode("utf-8") for cell in row.find_all(['th', 'td'])]
                rows.append(cells)
    else:
        rows = ''
    #print(rows)
    return rows

def process_files(directory):
    # Initialize list to hold rows from all tables
    all_rows = []
    
    # Loop through files in the directory
    for filename in os.listdir(directory):
        if "footnote" in filename.lower() and filename.endswith(".htm"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                html_content = file.read()
                table_data = extract_table_from_html(html_content)
                filename_list = []
                match = re.search(r'_(\d+)\.', filename)
                if match:
                    ref_num = match.group(1)
                else:
                    ref_num = ''
                error_message = '---Fill in Information---'
                filename_cell = [ref_num,error_message]
                filename_list.append(filename_cell)
                if extract_table_from_html(html_content) == '':
                    all_rows.extend(filename_list)
                    #print(table_data)
                else:
                    all_rows.extend(table_data)

    
    # Write the extracted data to a CSV file
    output_csv_path = "footnote_output.csv"
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(all_rows)
    
    print(f"CSV file '{output_csv_path}' has been created with extracted table data.")

def remove_files_with_footnote(directory):
    for filename in os.listdir(directory):
        if "footnote" in filename.lower():
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {str(e)}")

# Example usage:
directory = "C:/Users/admin/Documents/Python Scripts/NUREG/testing/"
process_files(directory)
remove_files_with_footnote(directory)