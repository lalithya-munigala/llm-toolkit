import argparse
from client import ask, cost_cents


def run_one(prompt: str, provider: str):
    print(f"\n--- {provider.upper()} ---")
    try:
        response = ask(prompt, provider=provider)
        print(response.text)
        print(f"[cost: {cost_cents(response):.4f} cents]")
    except Exception as e:
        print(f"(skipped — {e})")


def main():
    parser = argparse.ArgumentParser(description="Ask an LLM a question.")
    parser.add_argument("prompt", help="The question to ask")
    parser.add_argument("--provider", default="gemini", help="claude or gemini")
    parser.add_argument("--all", action="store_true", help="Ask all providers")
    args = parser.parse_args()

    if args.all:
        for provider in ["claude", "gemini"]:
            run_one(args.prompt, provider)
    else:
        run_one(args.prompt, args.provider)


if __name__ == "__main__":
    main()