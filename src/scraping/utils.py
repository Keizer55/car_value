import pandas as pd

def excel_to_df(filename, sheetname):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(filename, sheetname=sheetname)
    # Return the DataFrame
    return df


import os

def check_and_create_folder(path):
  # check if the path exists and is a directory
  if os.path.exists(path) and os.path.isdir(path):
    print(f"Folder {path} already exists")
  # if not, create the folder and any missing parent directories
  else:
    os.makedirs(path, exist_ok=True)
    print(f"Folder {path} created")
    
    





# =============================================================================
#     # Get the absolute path of the current file
#     current_file = os.path.abspath(__file__)
#     # Get the directory name of the current file
#     current_dir = os.path.dirname(current_file)
#     # Go one folder up from the current directory
#     parent_dir = os.path.join(current_dir, "..")
#     # Set the working path to the parent directory
#     os.chdir(parent_dir)
# =============================================================================
