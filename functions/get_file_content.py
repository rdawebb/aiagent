import os
from functions.config import MAX_CHARS
from google.genai import types

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

def get_file_content(working_directory, file_path):
    target_file = os.path.join(working_directory, file_path)

    # security check: prevent directory traversal attacks
    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    try:
        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: '{file_path}'"

        with open(target_file, "r") as file:
            content = file.read()
            if len(content) > MAX_CHARS:
                return content[:MAX_CHARS] + f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
            return content

    except Exception as e:
        return f"Error: {str(e)}"