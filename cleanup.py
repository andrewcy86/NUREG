import os
import csv
from bs4 import BeautifulSoup

def replace_links_in_html(html_file, csv_file):
    # Open and parse the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')

    # Read the CSV file to get the links
    links_to_replace = {}
    with open(csv_file, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) >= 2:
                old_link = row[0].strip()
                new_link = row[1].strip()
                links_to_replace[old_link] = new_link

    # Replace links in the HTML file
    for link in soup.find_all('a'):
        href = link.get('href')
        #print(href)
        #print(links_to_replace)
        if href in links_to_replace:
            link['href'] = links_to_replace[href]

    # Write the modified HTML back to the file
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

# Iterate through HTML files in a folder
def process_html_files(folder_path, csv_file):
    for filename in os.listdir(folder_path):
        if filename.endswith('.htm'):
            html_file = os.path.join(folder_path, filename)
            replace_links_in_html(html_file, csv_file)
            print(filename)

# Change Directory Path
directory = "C:/Users/admin/Documents/Python Scripts/NUREG/testing/"
csv_file = "C:/Users/admin/Documents/Python Scripts/NUREG/filename_mapping.csv"

process_html_files(directory, csv_file)
