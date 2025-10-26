import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

verbose = False
user_prompt = ""

if "--verbose" in sys.argv:
    verbose = True
    sys.argv = list(filter(lambda arg: arg != "--verbose", sys.argv))

user_prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    # GenerateContentResponse
    print(f"GenAI Response: {response.text}")
    # print(response.usage_metadata)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
except IndexError:
    print("prompt not provied")
    exit(1)
