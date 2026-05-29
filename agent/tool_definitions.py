tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": """Search the product inventory based on filters provided by the user.
            Use this when the user is looking for product recommendations or wants to find products
            matching their preferences like occasion, style, size, or budget.
            Always use this before recommending any product — never recommend from memory.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Style or occasion tags e.g. ['modest', 'evening', 'lace']"
                    },
                    "size": {
                        "type": "string",
                        "description": "Dress size e.g. '8', '14', '2'"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price as a number, not a string. e.g. 300 not '300'"
                    },
                    "is_sale": {
                        "type": "boolean",
                        "description": "True if user wants sale items only"
                    },
                    "is_clearance": {
                        "type": "boolean",
                        "description": "True if user wants clearance items only"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": """Fetch full details of a single product by product_id.
            Only call this with a product_id from previous search_products results, never guess.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID e.g. 'P004'"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Fetch order details by order_id. Use when user mentions an order number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID e.g. '1043'"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_return",
            "description": """Evaluate return eligibility for an order based on store policy.
            Always call this for return/exchange/refund requests  never guess eligibility yourself.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID to evaluate e.g. '1043'"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]