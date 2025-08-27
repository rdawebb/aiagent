# import necessary libraries
import os # import os to access environment variables
import sys # import sys to check prompt input
from dotenv import load_dotenv # import api key
from google import genai # import Gemini
from google.genai import types # import types

# main function
def main():
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

    # generate response from Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", # model name
        contents=messages # user prompt passed to Gemini
    )

    # if verbose flag is set, print prompt and token counts
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}") # user prompt output
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # prompt token count output
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # response token count output

    print(response.text) # Gemini response

# run main function
if __name__ == "__main__":
    main()
