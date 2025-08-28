# import necessary libraries
import os # import os to access environment variables
import subprocess # import subprocess to run Python scripts
from google.genai import types  # import types

# schema for run_python_file file
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

# run a Python file
def run_python_file(working_directory, file_path, args=[]):
    # construct the absolute path to the target file
    target_file = os.path.join(working_directory, file_path)

    # check if absolute file path is outside the working directory
    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # check at every stage of the process
    try:
        # check if target file is a Python file
        if not target_file.endswith(".py"):
            return f'Error: File "{target_file}" is not a Python file'
        
        # check if target file exists
        if not os.path.exists(target_file):
            return f'Error: File "{file_path}" not found'

        # run the Python file
        output = subprocess.run(["python", file_path] + args, capture_output=True, text=True, timeout=30, cwd=working_directory)
        if output.returncode != 0: # check if the process exited with an error
            return f"Process exited with code {output.returncode}\nSTDOUT: {output.stdout}\nSTDERR: {output.stderr}" # return error code and both stdout and stderr
        if output.stdout.strip() == "" and output.stderr.strip() == "": # check if there was no output
            return "No output produced"
        return f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}" # return both stdout and stderr

    # catch timeout errors
    except subprocess.TimeoutExpired:
        return f"Error: Execution timed out after 30 seconds"

    # catch all for any other exceptions
    except Exception as e:
        return f"Error: executing python file: {e}" # catch all for any other exceptions