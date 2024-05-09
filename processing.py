import os
from bs4 import BeautifulSoup
import csv
csv_filename_mapping = "filename_mapping.csv"

def determine_filename(title):
    if "Section" in title.split('.')[0]: 
        new_filename_part = ''
        return new_filename_part + ".htm"
    elif "Task" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part + ".htm"
    elif "Item" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part + ".htm"
    elif "Issue" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part  + ".htm"
    elif "TABLE" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part + ".htm"
    elif "Appendix" in title:
        new_filename_part = title.split('.')[0]
        return new_filename_part + ".htm"
    elif "Footnote" in title:
        new_filename_part = title.rsplit(': ', 1)
        return new_filename_part + ".htm"                                      
    else: 
        return title + "_" + ".htm"

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
                        new_filename = ''
                        title = h4_tag.text.strip().replace(" ", "_").replace(".", "_")

                        old_filename = os.path.splitext(filename)[0]
                        new_filename = determine_filename(title)
                        #new_filepath = os.path.join(folder_path, new_filename)
                        #os.rename(filepath, new_filepath)
                        print(f"Renamed {filename} to {new_filename}")
                        writer.writerow([filename, new_filename])
                    else:
                        print(f"No <h4> tag found in {filename}")
                        if h3_tag:
                            new_filename = determine_filename(title)
                            #new_filepath = os.path.join(folder_path, new_filename)
                            #os.rename(filepath, new_filepath)
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
                            else:
                                print("No image tag found under p tag.")
                        else:
                            print("No p tag found under h3 tag.")
                    else:
                        print("No h3 tag found.")

folder_path = "C:/Users/admin/Documents/Python Scripts/NUREG/testing/"
rename_files(folder_path)
remove_hr_image(folder_path)
