# import necessary libraries
import os # import os to access environment variables
import sys # import sys to check prompt input
from dotenv import load_dotenv # import api key
from google import genai # import Gemini
from google.genai import types # import types

# import functions
from functions.call_function import call_function, available_functions  # import call_function function
from prompts import system_prompt  # import system prompt

# main function
def main():
    load_dotenv() # load environment variables from .env file

    api_key = os.environ.get("GEMINI_API_KEY") # Get API key from environment file
    client = genai.Client(api_key=api_key) # Create Gemini client

    verbose = "--verbose" in sys.argv # check if verbose flag is set
    if len(sys.argv) < 2: # check if prompt is provided
        print("AI Agent\nUsage: python main.py '<your prompt here>'") # error message
        sys.exit(1) # exit with error code
    args = sys.argv[1:] # user prompt
    prompt = " ".join(args) # concatenate user prompt into single string

    # print user prompt if verbose flag is set
    if verbose:
        print(f"User prompt: {prompt}\n") # user prompt output

    # create message object to store conversation history
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # main loop with error handling and 20 iteration limit
    i = 0 # loop counter 
    while i < 20:
        # check for errors during response generation
        try:
            final_response = generate_content(client, messages, verbose) # generate response from Gemini

            # check for response.text property, break loop if so
            if final_response:
                print(f'Final response:\n{final_response}') # print final response
                break

        # check if there are any errors
        except Exception as e:
            print(f"Error: {e}") # print error message

        i += 1 # increment loop counter

    # iteration limit message
    if i >= 20:
        print("Max iterations (20) reached")
        sys.exit(1) # exit with error code

def generate_content(client, messages, verbose):
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
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # prompt token count output
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # response token count output

    # check candidates property of the response
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content) # append Gemini response to messages

    # check if there are any function calls
    if not response.function_calls:
        return response.text
    
    all_responses = [] # list to store all function call responses
    for function_call_part in response.function_calls: # iterate over function calls
        function_call_result = call_function(function_call_part, verbose) # call the appropriate function
        function_call_response = function_call_result.parts[0] # get the function response part

        # check if function_call_result has a valid response
        if (not function_call_result.parts or
            not function_call_response):
            raise Exception("Exiting - empty function response") # error if function call did not return a response

        # check if verbose flag is set
        if verbose:
            print(f"-> {function_call_response.response}") # print function call response
        all_responses.append(function_call_response) # add function call response to all_responses list

    # check if all_responses have a valid response
    if not all_responses:
        raise Exception("Exiting - no function response") # error if function call did not return a response

    # append all responses to messages
    messages.append(types.Content(role="user", parts=all_responses))

# run main function
if __name__ == "__main__":
    main()