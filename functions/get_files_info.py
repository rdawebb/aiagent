import os
from google.genai import types

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

def get_files_info(working_directory, directory="."):
    target_directory = os.path.join(working_directory, directory)

    # security check: prevent directory traversal attacks
    if not os.path.abspath(target_directory).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    try:
        if not os.path.isdir(target_directory):
            return f"Error: '{directory}' is not a directory"

        files_info = []
        for items in os.listdir(target_directory):
            item_path = os.path.join(target_directory, items)
            size = os.path.getsize(item_path)
            if os.path.isfile(item_path):
                files_info.append(f"- {items}: file_size={size} bytes, is_dir=False")
            elif os.path.isdir(item_path):
                files_info.append(f"- {items}: file_size={size} bytes, is_dir=True")
            else:
                continue
    
    except Exception as e:
        return f"Error: {str(e)}"

    return "\n".join(files_info)