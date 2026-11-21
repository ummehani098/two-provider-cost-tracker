🤖 AI Multi-Provider Cost Tracker

A Python-based application that compares three AI providers: Google Gemini, Groq, and OpenRouter using the same user prompt.

Project Features
Integrates Gemini, Groq, and OpenRouter APIs.
Compares AI-generated responses.
Tracks input and output tokens.
Measures API response time.
Calculates estimated API costs.
Saves results automatically in results.json.
Handles individual provider errors.
Technologies
Python
Google Gen AI SDK
Groq SDK
OpenAI SDK
JSON
python-dotenv

Project Structure text
two-provider-cost-tracker/
│
├── tracker.py
├── .env
├── results.json
├── .gitignore
└── README.md

Installation

Clone the repository:

bash 
git clone https://github.com/ummehani098/two-provider-cost-tracker.git
cd two-provider-cost-tracker

Install dependencies:

bash
pip install google-genai groq openai python-dotenv

Environment Variables

Create a .env file:

env
GEMINI_API_KEY=your_key
GEMINI_MODEL=your_model

GROQ_API_KEY=your_key
GROQ_MODEL=your_model

OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=your_model


Also configure the input and output token prices for each provider.

Run the Project
bash
uv run tracker.py


Enter a prompt and the application will generate responses from all three providers.

Testing Prompts
Enter your prompt: What are new branches of Artificial Intelligence?

===================================================================================================================
                         API PROVIDER COMPARISON
===================================================================================================================
Provider       Model                      Input Tokens  Output Tokens     Response Time      Cost (USD)
-------------------------------------------------------------------------------------------------------------------
Gemini         gemini-3.5-flash-lite                 9           1017          4.808 sec     $0.00254520
Groq           openai/gpt-oss-120b                  79           3072          7.008 sec     $0.00185505
OpenRouter     google/gemini-3.8-flash               8           1996         18.985 sec     $0.00749100
===================================================================================================================

Enter your prompt: Suggest some Artificial Engineering Projects for beginners?

===================================================================================================================
                         API PROVIDER COMPARISON
===================================================================================================================
Provider       Model                      Input Tokens  Output Tokens     Response Time      Cost (USD)
-------------------------------------------------------------------------------------------------------------------
Gemini         gemini-3.5-flash-lite                 9            949          3.887 sec     $0.00237520
Groq           openai/gpt-oss-120b                  79           3072          7.142 sec     $0.00185505
OpenRouter     google/gemini-3.8-flash               8           1996         17.183 sec     $0.00749100
===================================================================================================================

Enter your prompt: What is best example of artificial intelligence daily use?

===================================================================================================================
                         API PROVIDER COMPARISON
===================================================================================================================
Provider       Model                      Input Tokens  Output Tokens     Response Time      Cost (USD)
-------------------------------------------------------------------------------------------------------------------
Gemini         gemini-3.5-flash-lite                11            454          2.570 sec     $0.00113830
Groq           openai/gpt-oss-120b                  81            796          2.640 sec     $0.00048975
OpenRouter     google/gemini-3.8-flash              10           1307         12.868 sec     $0.00490875
===================================================================================================================

Through this project, I explored:

Working with multiple AI provider APIs.
Integrating different LLM models into one application.
Understanding token consumption and API pricing.
Measuring API performance and response latency.
Managing API keys securely with environment variables.
Handling API errors and exceptions.
Working with JSON data and Python functions.
Comparing different AI models based on performance and cost.
👩‍💻 Author

Umme Hani

GitHub: @ummehani098
