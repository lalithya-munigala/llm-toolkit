import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def ask(prompt: str, model: str = "gemini-3.6-flash") -> str:
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    answer = ask("Explain what a token is in 2 sentences.")
    print(answer)