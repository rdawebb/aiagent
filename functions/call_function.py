# import necessary libraries
import os # import os to access environment variables
from google.genai import types  # import types

# import functions
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

# define available functions for Gemini
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
    ]
)

# call the appropriate function based on the function call part
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name # get the function name
    args = function_call_part.args.copy() # create a copy of the arguments

    # if verbose flag is set, print function name and arguments, else just name
    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f"- Calling function: {function_name}")

    # create a mapping of function names to function objects
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    args["working_directory"] = "./calculator" # add working_directory to the arguments

    # check if function_name is not valid
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # if function_name is valid, call the function and return the result
    function_result = function_map[function_name](**args) # call the function with arguments
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
