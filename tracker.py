import os
import json
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from google import genai
from groq import Groq
from openai import OpenAI

load_dotenv()

# API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY= os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL= os.getenv("OPENROUTER_MODEL")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# Model validation
if not GEMINI_MODEL:
    print("Warning: GEMINI_MODEL is missing.")

if not GROQ_MODEL:
    print("Warning: GROQ_MODEL is missing.")

if not OPENROUTER_MODEL:
    print("Warning: OPENROUTER_MODEL is missing.")

# Initialize clients
gemini_client = (
    genai.Client(
        api_key=GEMINI_API_KEY,
        http_options={
            "timeout": 30000
        }
    )
    if GEMINI_API_KEY else None
)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


openrouter_client = (
    OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    if OPENROUTER_API_KEY else None
)
    
def calculate_cost(input_tokens, output_tokens, input_price, output_price):
    """Calculate API cost in USD (prices per 1 million tokens)."""

    if input_price is None or output_price is None:
        return None

    return (
        (input_tokens / 1_000_000) * input_price
        + (output_tokens / 1_000_000) * output_price
    )


def get_price(variable):
    """Get token pricing from environment variables."""

    value = os.getenv(variable)

    return float(value) if value else None


def gemini_provider(prompt):
    """Generate a response using Gemini with retry."""

    if not gemini_client:
        raise ValueError("GEMINI_API_KEY is missing.")

    if not GEMINI_MODEL:
        raise ValueError("GEMINI_MODEL is missing.")

    max_retries = 3

    for attempt in range(max_retries):

        try:
            print("Connecting to Gemini API...", flush=True)

            start_time = time.perf_counter()

            response = gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            response_time = time.perf_counter() - start_time

            usage = response.usage_metadata

            input_tokens = usage.prompt_token_count or 0 if usage else 0
            output_tokens = usage.candidates_token_count or 0 if usage else 0

            cost = calculate_cost(
                input_tokens,
                output_tokens,
                get_price("GEMINI_INPUT_PRICE"),
                get_price("GEMINI_OUTPUT_PRICE")
            )

            return {
                "provider": "Gemini",
                "model": GEMINI_MODEL,
                "reply": response.text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "response_time": round(response_time, 3),
                "cost_usd": cost
            }

        except Exception as error:

            if "503" in str(error) or "UNAVAILABLE" in str(error):

                if attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Gemini overloaded. Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise

            else:
                raise


def groq_provider(prompt):
    """Generate a response using Groq."""

    if not groq_client:
        raise ValueError("GROQ_API_KEY is missing.")
    start_time = time.perf_counter()
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    end_time = time.perf_counter()

    response_time = end_time - start_time
    usage = response.usage

    input_tokens = usage.prompt_tokens if usage else 0
    output_tokens = usage.completion_tokens if usage else 0

    cost = calculate_cost(
        input_tokens,
        output_tokens,
        get_price("GROQ_INPUT_PRICE"),
        get_price("GROQ_OUTPUT_PRICE")
    )

    return {
        "provider": "Groq",
        "model": GROQ_MODEL,
        "reply": response.choices[0].message.content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "response_time": round(response_time, 3),
        "cost_usd": cost
    }

def openrouter_provider(prompt):
    """Generate a response using OpenRouter."""

    if not openrouter_client:
        raise ValueError("OPENROUTER_API_KEY is missing.")

    if not OPENROUTER_MODEL:
        raise ValueError("OPENROUTER_MODEL is missing.")

    start_time = time.perf_counter()

    response = openrouter_client.chat.completions.create(
    model=OPENROUTER_MODEL,
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=2000
)
    

    response_time = time.perf_counter() - start_time

    usage = response.usage

    input_tokens = usage.prompt_tokens if usage else 0
    output_tokens = usage.completion_tokens if usage else 0

    cost = None

    if usage and getattr(usage, "cost", None) is not None:
        cost = usage.cost
    else:
        cost = calculate_cost(
            input_tokens,
            output_tokens,
            get_price("OPENROUTER_INPUT_PRICE"),
            get_price("OPENROUTER_OUTPUT_PRICE")
        )

    return {
        "provider": "OpenRouter",
        "model": OPENROUTER_MODEL,
        "reply": response.choices[0].message.content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "response_time": round(response_time, 3),
        "cost_usd": cost
    }


def display_results(results):

    print("\n" + "=" * 115)
    print("                         API PROVIDER COMPARISON")
    print("=" * 115)

    print(
        f"{'Provider':<15}"
        f"{'Model':<25}"
        f"{'Input Tokens':>14}"
        f"{'Output Tokens':>15}"
        f"{'Response Time':>18}"
        f"{'Cost (USD)':>16}"
    )

    print("-" * 115)

    for result in results:

        cost = (
            f"${result['cost_usd']:.8f}"
            if result["cost_usd"] is not None
            else "N/A"
        )

        print(
            f"{result['provider']:<15}"
            f"{result['model']:<25}"
            f"{result['input_tokens']:>14}"
            f"{result['output_tokens']:>15}"
            f"{result['response_time']:>15.3f} sec"
            f"{cost:>16}"
        )

    print("=" * 115)


def save_results(results):
    """Save results to results.json."""

    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": results
    }

    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print("\nResults saved to results.json")


def main():
    prompt = input("\nEnter your prompt: ").strip()

    if not prompt:
        print("Prompt cannot be empty.")
        return

    providers = [
    gemini_provider,
    groq_provider,
    openrouter_provider
    ]
    

    results = []

    for provider in providers:
        print(f"\nRunning {provider.__name__}...")

        try:
            result = provider(prompt)
            results.append(result)

            print(f"\n{result['provider']} Response:")
            print("-" * 50)
            print(result["reply"])

        except Exception as error:
            print(f"Error in {provider.__name__}: {error}")

    if results:
        display_results(results)
        save_results(results)
    else:
        print("\nNo successful API responses.")


if __name__ == "__main__":
    main()