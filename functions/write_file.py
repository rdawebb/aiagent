import os
from google.genai import types

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

def write_file(working_directory, file_path, content):
    target_file = os.path.join(working_directory, file_path)

    # security check: prevent directory traversal attacks
    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"

    try:
        if not os.path.exists(target_file):
            # create parent directories if they don't exist
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as file:
            file.write(content)
            return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"

    except Exception as e:
        return f"Error: {str(e)}"