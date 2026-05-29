import json
import os
from groq import Groq
from tools.inventory_tools import search_products, get_product
from tools.order_tools import get_order
from tools.return_tools import evaluate_return
from agent.tool_definitions import tools

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a retail AI assistant for a clothing store with two roles:

1. Personal Shopper - Help users find products that match their style, size, budget and occasion.
2. Customer Support - Help users with order returns, exchanges and refunds based on store policy.

STRICT RULES:
- Never recommend a product you have not retrieved from search_products first.
- Never decide return eligibility yourself, always call evaluate_return.
- Never make up order details, always call get_order first.
- If an order ID or product ID does not exist, clearly tell the user it was not found.
- Always explain your reasoning,  why a product fits, why a return is eligible or not.
- Be conversational, helpful and concise.
"""

TOOL_MAP = {
    "search_products": search_products,
    "get_product": get_product,
    "get_order": get_order,
    "evaluate_return": evaluate_return,
}

def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1000,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            tools=tools,
            tool_choice="auto",
            temperature=0  # add this line
        )

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        # LLM wants to call a tool
        if stop_reason == "tool_calls" and message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # Process each tool call
            for tc in message.tool_calls:
                tool_name = tc.function.name
                tool_input = json.loads(tc.function.arguments)

                print(f"\n[Agent calling tool: {tool_name} with {tool_input}]")

                tool_fn = TOOL_MAP.get(tool_name)
                if tool_fn:
                    result = tool_fn(**tool_input)
                else:
                    result = {"error": f"Tool {tool_name} not found"}

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, default=str)
                })

        # LLM is done
        elif stop_reason == "stop":
            return message.content or "No response generated."

        # unexpected
        else:
            return "Something went wrong. Please try again."