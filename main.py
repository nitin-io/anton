import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[sys.argv[1]]
    )
except IndexError:
    print("prompt not provied")
    exit(1)

# GenerateContentResponse
print(response.text)
# print(response.usage_metadata)

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
