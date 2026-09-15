import os
from dotenv import load_dotenv
import anthropic
from google import genai

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def ask(prompt: str, provider: str = "gemini", model: str | None = None) -> str:
    if provider == "claude":
        model = model or "claude-sonnet-4-6"
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    elif provider == "gemini":
        model = model or "gemini-3.6-flash"
        response = gemini_client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text

    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'claude' or 'gemini'.")


if __name__ == "__main__":
    answer = ask("Explain what a token is in 2 sentences.", provider="gemini")
    print("Gemini says:")
    print(answer)

    # Uncomment this once you've added Claude credits:
    # answer = ask("Explain what a token is in 2 sentences.", provider="claude")
    # print("\nClaude says:")
    # print(answer)