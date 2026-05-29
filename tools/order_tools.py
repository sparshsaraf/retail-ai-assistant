from data_loader import ORDERS

def get_order(order_id: str) -> dict | None:
    df = ORDERS[ORDERS["order_id"] == order_id]
    if df.empty:
        return None
    return df.iloc[0].to_dict()