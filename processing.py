import os
from bs4 import BeautifulSoup
import csv
csv_filename_mapping = "filename_mapping.csv"
folder_path = "C:/Users/admin/Documents/Python Scripts/NUREG/testing/"

def determine_filename(title):
    if title.startswith('Section'): 
        new_filename_part = title.split('.')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif title.startswith('Task'):
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif title.startswith('Item'):
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif title.startswith('Issue'):
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_")  + ".htm"
    elif title.startswith('TABLE'):
        new_filename_part = title.split(':')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif title.startswith('Appendix'):
        new_filename_part = title.split('.')[0]
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"
    elif title.startswith('Footnote'):
        new_filename_part = title.split(":")[1].strip().encode('ascii', 'ignore').decode("utf-8")
        return new_filename_part.replace(" ", "_").replace(".", "_") + ".htm"                                      
    else: 
        return title + ".htm"

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
                        title = h4_tag.text.strip()  
                    else:
                        title = h3_tag.text.strip()  
   
                    new_filename = determine_filename(title)
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
