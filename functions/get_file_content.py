# import necessary libraries
import os # import os to access environment variables
from functions.config import MAX_CHARS # import max characters variable
from google.genai import types  # import types

# schema for get_file_content function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specific file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve, relative to the working directory.",
            ),
        },
    ),
)

# get content of a file
def get_file_content(working_directory, file_path):
    # construct the absolute path to the target file
    target_file = os.path.join(working_directory, file_path)

    # check if absolute file path is outside the working directory
    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    # check at every stage of the process
    try:
        # check if absolute file path is a file
        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: '{file_path}'"

        # read the contents of file and truncate if necessary
        with open(target_file, "r") as file: # open file for reading
            content = file.read() # read file content
            if len(content) > MAX_CHARS: # check if content exceeds max characters
                return content[:MAX_CHARS] + f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
            return content

    # if any error occurs, return the error message
    except Exception as e:
        return f"Error: {str(e)}"