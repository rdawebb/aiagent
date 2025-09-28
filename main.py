import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function, available_functions
from prompts import system_prompt

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    if len(sys.argv) < 2:
        print("AI Agent\nUsage: python main.py '<your prompt here>'")
        sys.exit(1)
    args = sys.argv[1:]
    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # retry loop with 20 iteration limit to handle function calls
    i = 0
    while i < 20:
        try:
            final_response = generate_content(client, messages, verbose)

            if final_response:
                print(f'Final response:\n{final_response}')
                break

        except Exception as e:
            print(f"Error: {e}")

        i += 1

    if i >= 20:
        print("Max iterations (20) reached")
        sys.exit(1)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            )
        )
    
    if "--verbose" in sys.argv:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # if no function calls, return the text response
    if not response.function_calls:
        return response.text
    
    # process function calls
    all_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        function_call_response = function_call_result.parts[0]

        if (not function_call_result.parts or
            not function_call_response):
            raise Exception("Exiting - empty function response")

        if verbose:
            print(f"-> {function_call_response.response}")
        all_responses.append(function_call_response)

    if not all_responses:
        raise Exception("Exiting - no function response")

    messages.append(types.Content(role="user", parts=all_responses))

if __name__ == "__main__":
    main()