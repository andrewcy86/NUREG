import os
from bs4 import BeautifulSoup
def determine_filename(title,old_filename):
    if "Section" in title.split('.')[0]: 
        new_filename_part = ''
        return new_filename_part + "_" + old_filename + ".htm"
    elif "Task" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part + "_" + old_filename + ".htm"
    elif "Item" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part + "_" + old_filename + ".htm"
    elif "Issue" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part + "_" + old_filename + ".htm"
    elif "TABLE" in title:
        new_filename_part = title.split(':')[0]
        return new_filename_part + "_" + old_filename + ".htm"
    elif "Appendix" in title:
        new_filename_part = title.split('.')[0]
        return new_filename_part + "_" + old_filename + ".htm"
    elif "Footnote" in title:
        new_filename_part = title.rsplit(': ', 1)
        return new_filename_part + "_" + old_filename + ".htm"                                      
    else: 
        return title + "_" + old_filename + ".htm"

def rename_files(folder_path):
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
                    new_filename = determine_filename(title,old_filename)

                    #new_filepath = os.path.join(folder_path, new_filename)
                    #os.rename(filepath, new_filepath)
                    print(f"Renamed {filename} to {new_filename}")
                else:
                    print(f"No <h4> tag found in {filename}")
                    if h3_tag:
                        new_filename = determine_filename(title,old_filename)
                        #new_filepath = os.path.join(folder_path, new_filename)
                        #os.rename(filepath, new_filepath)
                        print(f"Renamed {filename} to {new_filename}")

folder_path = "C:/Users/admin/Documents/Python Scripts/NUREG/testing/"
rename_files(folder_path)