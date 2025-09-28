import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python script.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    target_file = os.path.join(working_directory, file_path)

    # security check: prevent directory traversal attacks
    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    try:
        if not target_file.endswith(".py"):
            return f'Error: File "{target_file}" is not a Python file'
        
        if not os.path.exists(target_file):
            return f'Error: File "{file_path}" not found'

        # execute with 30-second timeout to prevent hanging
        output = subprocess.run(["python", file_path] + args, capture_output=True, text=True, timeout=30, cwd=working_directory)
        if output.returncode != 0:
            return f"Process exited with code {output.returncode}\nSTDOUT: {output.stdout}\nSTDERR: {output.stderr}"
        if output.stdout.strip() == "" and output.stderr.strip() == "":
            return "No output produced"
        return f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"

    except subprocess.TimeoutExpired:
        return f"Error: Execution timed out after 30 seconds"

    except Exception as e:
        return f"Error: executing python file: {e}"