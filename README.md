# llm-toolkit

A shared foundation library that talks to multiple LLM providers (Claude, Gemini) through one simple interface, with built-in cost tracking.

## What it does

- One `ask(prompt, provider, model)` function that works across providers
- Automatically tracks token usage and calculates cost per call
- A command-line tool to compare answers from multiple providers side by side

## Setup

1. Clone this repo and install [uv](https://docs.astral.sh/uv/)
2. Run `uv sync` to install dependencies
3. Create a `.env` file with your API keys:

ANTHROPIC_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here

## Usage

Ask one provider:

uv run cli.py "What is a token?" --provider gemini

Ask all providers at once:

uv run cli.py "What is a token?" --all

## Example output

<img width="950" height="517" alt="demo" src="https://github.com/user-attachments/assets/b8d7d3cd-b006-40f5-a180-b75b3afbc1a3" />

## What I learned

Building this taught me how different LLM providers structure their APIs differently — Claude and Gemini return usage/token data in different shapes, so I had to normalize both into one `Response` dataclass. I also learned that cost tracking has to happen per-call using actual token counts, not estimates.

## Next steps

- Add OpenAI as a third provider
- Add streaming support
- Use this as the foundation for the Athena and Scout projects in later weeks