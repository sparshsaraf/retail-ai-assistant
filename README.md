# Retail AI Assistant

A conversational AI agent that simulates two roles for a retail clothing store 
a Personal Shopper and a Customer Support Assistant. The agent uses tool calling 
to ground every response in real inventory and order data, avoiding hallucination.



## Tech Stack

- Python
- Groq API (llama-3.3-70b-versatile)
- Pandas
- python-dotenv

## Setup Instructions

1. Clone the repository
```cmd
git clone https://github.com/yourusername/retail-ai-assistant.git
cd retail-ai-assistant
```

2. Create and activate virtual environment
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```cmd
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Groq API key

GROQ_API_KEY=your_groq_api_key_here

5. Run the assistant
```cmd
python main.py
```

---

## Example Queries

**Shopping:**

I need a modest evening gown under $300 in size 8, I prefer something on sale

I am looking for a bestselling bridal dress for a wedding, size 12 under $400

**Support:**
I want to return order O0012

I want to return order O0003

**Edge case:**
I want to return order O9999

## how it works 
the agent uses a react style loop , it reads the user message, decides which tool to call , executes it against real data, uses the result to form a grounded response 

check out architecture.md for full details 

