import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.schemas import schema_get_files_info
from functions.schemas import schema_write_file
from functions.schemas import schema_run_python_file
from functions.schemas import schema_get_file_content
from libs.function_call import call_function

verbose = False
user_prompt = ""

if "--verbose" in sys.argv:
    verbose = True
    sys.argv = list(filter(lambda arg: arg != "--verbose", sys.argv))

user_prompt = sys.argv[1]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    model='gemini-2.0-flash-001'
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    # GenerateContentRespons
    # print(response)
    print(response.function_calls)
    result = call_function(response.function_calls[0])
    print(result)
    print(response.text)

    # print(response.usage_metadata)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
except IndexError:
    print("prompt not provied")
    exit(1)
