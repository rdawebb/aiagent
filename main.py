# import necessary libraries
import os # import os to access environment variables
import sys # import sys to check prompt input
from dotenv import load_dotenv # import api key
from google import genai # import Gemini
from google.genai import types # import types
from functions.get_files_info import schema_get_files_info  # import schema for get_files_info function
from functions.get_file_content import schema_get_file_content  # import schema for get_file_content function
from functions.write_file import schema_write_file  # import schema for write_file function
from functions.run_python_file import schema_run_python_file  # import schema for run_python function

# main function
def main():
    # define available functions for Gemini
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file
        ]
    )
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY") # Get API key from environment file
    client = genai.Client(api_key=api_key) # Create Gemini client

    if len(sys.argv) < 2: # check if prompt is provided
        print("Usage: python main.py '<your prompt here>'") # error message
        sys.exit(1) # exit with error code
    args = sys.argv[1:] # user prompt
    prompt = " ".join(args) # concatenate user prompt into single string

    # create message object to store conversation history
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # system prompt to instruct Gemini on its capabilities
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    # generate response from Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", # model name
        contents=messages, # user prompt passed to Gemini
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ) # config for Gemini API
    )

    # if verbose flag is set, print prompt and token counts
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}") # user prompt output
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # prompt token count output
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # response token count output

    # check if there are function calls
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})") # print function call name and arguments
            return 
    print(response.text) # Gemini response

# run main function
if __name__ == "__main__":
    main()