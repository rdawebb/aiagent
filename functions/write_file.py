# import necessary libraries
import os # import os to access environment variables
from google.genai import types  # import types

# schema for write_file function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specific file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

# write content to a file
def write_file(working_directory, file_path, content):
    # construct the absolute path to the target file
    target_file = os.path.join(working_directory, file_path)

    # check if absolute file path is outside the working directory
    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"

    # check at every stage of the process
    try:
        # check if file path exists
        if not os.path.exists(target_file):
            os.makedirs(os.path.dirname(target_file), exist_ok=True) # create directories if they don't exist

        # write the contents to the file
        with open(target_file, "w") as file: # open file for writing
            file.write(content) # write content to file
            return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"

    # if any error occurs, return the error message
    except Exception as e:
        return f"Error: {str(e)}"