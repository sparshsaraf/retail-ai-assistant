import pandas as pd
import ast
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def _parse_stock(val):
    """Convert stringified dict to actual dict."""
    try:
        return ast.literal_eval(val)
    except:
        return {}

def load_data():
    # Load inventory
    inventory_df = pd.read_csv(os.path.join(DATA_DIR, "product_inventory.csv"))
    inventory_df["stock_per_size"] = inventory_df["stock_per_size"].apply(_parse_stock)
    inventory_df["tags"] = inventory_df["tags"].apply(
        lambda x: [t.strip() for t in x.split(",")]
    )
    inventory_df["sizes_available"] = inventory_df["sizes_available"].apply(
        lambda x: [s.strip() for s in x.split("|")]
    )

    # Load orders
    orders_df = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

    # Load policy
    with open(os.path.join(DATA_DIR, "policy.txt"), "r") as f:
        policy_text = f.read()

    return inventory_df, orders_df, policy_text


# Load once at module import , all tools import from here
INVENTORY, ORDERS, POLICY = load_data()