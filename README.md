# NUREG
1) Take the NUREG 0933 pdf and export it to HTML ensuring that the option to export to seperate pages based on bookmarks is selected.
2) Run processing.py to rename files and generate the filename_mapping.csv.
   processing.py also cleans up hr images and inserts the appropriate hr html tag.
3) Run footnote.py to generate footnote_output.csv and remove filenames
4) Run clenaup.py to map all the old url's to the new filenames.
   TODO: Cleanup footnote links to map to the footnote solution that will be developed.
   
![image](https://github.com/andrewcy86/NUREG/assets/5041903/6598719a-9a08-41e4-8e02-1875856c1638)
