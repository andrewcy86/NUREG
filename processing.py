import os
from bs4 import BeautifulSoup
import csv
csv_filename_mapping = "filename_mapping.csv"
folder_path = "C:/Users/admin/Documents/Python Scripts/NUREG/testing/"

def extract_value_from_string(string, term):
    delimiter = ''
    if term.lower() == 'section' or term.lower() == 'appendix':
        delimiter = '.'
    elif term.lower() == 'task' or term.lower() == 'item' or term.lower() == 'issue' or term.lower() == 'table' or term.lower() == 'nureg-0933: footnote':
        delimiter = ':'
    else:
        return None

    index = string.lower().find(term.lower())
    if index != -1:
        if term.lower() == 'nureg-0933: footnote':
            value = string.split(":")[1].strip().encode('ascii', 'ignore').decode("utf-8")
        else:
            value = string.split(delimiter)[0].strip()
        return value.replace(" ", "_").replace(".", "_") + ".htm"
    else:
        return None
    
def find_matching_term(terms, string):
    for term in terms:
        if string.lower().startswith(term.lower()):
            return term
    return None
"""    
def determine_filename(title):
    if "Section" in title:
        new_filename_part = title.split('.')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif "Task" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif "Item" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif "Appendix" in title:
        new_filename_part = title.split('.')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif "Issue" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_")  + ".htm"
    elif "TABLE" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif "Footnote" in title:
        new_filename_part = title.split(":")[1].strip().encode('ascii', 'ignore').decode("utf-8")
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"                                      
    else: 
        return title + ".htm"
 """
def rename_files(folder_path):
    with open(csv_filename_mapping, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=',')
        for filename in os.listdir(folder_path):
            if filename.endswith(".htm"):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, "rb") as file:
                    contents = file.read()
                    soup = BeautifulSoup(contents, "html.parser")
                    h4_tag = soup.find("h4")
                    h3_tag = soup.find("h3")

                    if h4_tag:
                        title = h4_tag.text.strip().encode('ascii', 'ignore').decode("utf-8")
                    else:
                        title = h3_tag.text.strip().encode('ascii', 'ignore').decode("utf-8")
   
                    terms = ['Section', 'Task', 'Item', 'Issue', 'TABLE', 'Appendix', 'NUREG-0933: Footnote']

                    matching_term = find_matching_term(terms, title)

                    if matching_term:
                        new_filename = extract_value_from_string(title, matching_term)
                    else:
                        new_filename = title.replace(" ( )", "").replace(" ", "_").replace(".", "_") + ".htm"

                    new_filepath = os.path.join(folder_path, new_filename)
                    file.close()
                    os.rename(filepath, new_filepath)
                    print(f"Renamed {filename} to {new_filename}")
                    writer.writerow([filename, new_filename])
                   
def remove_hr_image(folder_path):
    with open('removed_images.txt', 'w') as rmfile:
        for filename in os.listdir(folder_path):
            if filename.endswith(".htm"):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, "rb") as file:
                    contents = file.read()
                    soup = BeautifulSoup(contents, "html.parser")
                    h4_tag = soup.find('h4')
                    h3_tag = soup.find('h3')

                    if h4_tag:
                        # Find the first p tag directly under the h4 tag
                        p_tag = h4_tag.find_next_sibling('p')
                        if p_tag:
                            img_tag = p_tag.find('span').find('img') if p_tag.find('span') else None
                            if img_tag:
                                # If image tag exists, extract filename and remove it
                                filename = img_tag['src'].split('/')[-1]
                                p_tag.decompose()  # Remove the surrounding tag
                                # Replace with a hr tag
                                h4_tag.insert_after(soup.new_tag('hr'))
                                print(f"Filename: {filename}")
                                rmfile.write(filename +'\n')
                                # Alter HTML file to see the changes done
                                with open(filepath, "wb") as f_output:
                                    f_output.write(soup.prettify("utf-8"))
                                    file.close()
                            else:
                                print("No image tag found under p tag.")
                        else:
                            print("No p tag found under h4 tag.")
                    else:
                        print("No h4 tag found.")

                    if h3_tag:
                        # Find the first p tag directly under the h4 tag
                        p_tag = h3_tag.find_next_sibling('p')
                        if p_tag:
                            img_tag = p_tag.find('span').find('img') if p_tag.find('span') else None
                            if img_tag:
                                # If image tag exists, extract filename and remove it
                                filename = img_tag['src'].split('/')[-1]
                                p_tag.decompose()  # Remove the surrounding tag
                                # Replace with a hr tag
                                h3_tag.insert_after(soup.new_tag('hr'))
                                print(f"Filename: {filename}")
                                rmfile.write(filename +'\n')
                                # Alter HTML file to see the changes done
                                with open(filepath, "wb") as f_output:
                                    f_output.write(soup.prettify("utf-8"))
                                    file.close()
                            else:
                                print("No image tag found under p tag.")
                        else:
                            print("No p tag found under h3 tag.")
                    else:
                        print("No h3 tag found.")

def delete_files_from_list(file_list_path):

    flist = open(file_list_path)

    for f in flist:
        fname = f.rstrip()
        if os.path.isfile(folder_path+fname):
            os.remove(folder_path+fname)
            print("File Delete: " + fname)
    
    flist.close()
 
rename_files(folder_path)
remove_hr_image(folder_path)

file_list_path = "removed_images.txt"
delete_files_from_list(file_list_path)
