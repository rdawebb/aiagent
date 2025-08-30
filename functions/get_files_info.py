# import necessary libraries
import os # import os to access environment variables
from google.genai import types # import types

# define the schema for the get_files_info function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# get information about files in a directory
def get_files_info(working_directory, directory="."):
    # construct the absolute path to the target directory
    target_directory = os.path.join(working_directory, directory)

    # check if absolute directory is outside the working directory
    if not os.path.abspath(target_directory).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    # check at every stage of the process
    try:
        # check if directory argument is a directory
        if not os.path.isdir(target_directory):
            return f"Error: '{directory}' is not a directory"

        # list files and directories in the target directory
        files_info = [] # list to store file information
        for items in os.listdir(target_directory):
            item_path = os.path.join(target_directory, items) # construct the absolute path
            size = os.path.getsize(item_path) # get the size of the file or directory
            if os.path.isfile(item_path): # check if it's a file
                files_info.append(f"- {items}: file_size={size} bytes, is_dir=False") # add file info
            elif os.path.isdir(item_path): # check if it's a directory
                files_info.append(f"- {items}: file_size={size} bytes, is_dir=True") # add directory info
            else:
                continue # skip if not a file or directory
    
    # if any error occurs, return the error message
    except Exception as e:
        return f"Error: {str(e)}" # catch-all for any other exceptions

    # return the collected file information
    return "\n".join(files_info)