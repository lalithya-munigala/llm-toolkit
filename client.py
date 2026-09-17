import os
from dataclasses import dataclass
from dotenv import load_dotenv
import anthropic
from google import genai

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Prices are dollars per million tokens: {"in": input_price, "out": output_price}
PRICES = {
    "claude-sonnet-4-6": {"in": 3.0, "out": 15.0},
    "gemini-3.6-flash": {"in": 0.075, "out": 0.30},
}


@dataclass
class Response:
    text: str
    input_tokens: int
    output_tokens: int
    model: str


def cost_cents(response: Response) -> float:
    prices = PRICES.get(response.model)
    if not prices:
        return 0.0
    dollars = (response.input_tokens / 1_000_000) * prices["in"] + \
              (response.output_tokens / 1_000_000) * prices["out"]
    return dollars * 100


def ask(prompt: str, provider: str = "gemini", model: str | None = None) -> Response:
    if provider == "claude":
        model = model or "claude-sonnet-4-6"
        result = anthropic_client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return Response(
            text=result.content[0].text,
            input_tokens=result.usage.input_tokens,
            output_tokens=result.usage.output_tokens,
            model=model
        )

    elif provider == "gemini":
        model = model or "gemini-3.6-flash"
        result = gemini_client.models.generate_content(model=model, contents=prompt)
        usage = result.usage_metadata
        return Response(
            text=result.text,
            input_tokens=usage.prompt_token_count,
            output_tokens=usage.candidates_token_count,
            model=model
        )

    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'claude' or 'gemini'.")


if __name__ == "__main__":
    response = ask("Explain what a token is in 2 sentences.", provider="gemini")
    print(f"Gemini says: {response.text}")
    print(f"Cost: {cost_cents(response):.4f} cents")