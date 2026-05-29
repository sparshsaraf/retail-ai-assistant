from datetime import datetime
from data_loader import ORDERS, INVENTORY, POLICY
from tools.order_tools import get_order
from tools.inventory_tools import get_product

def evaluate_return(order_id: str) -> dict:
    #Get the order
    order = get_order(order_id)
    if order is None:
        return {
            "eligible": False,
            "reason": "Order not found. Please check your order ID."
        }

    #Get the product
    product = get_product(order["product_id"])
    if product is None:
        return {
            "eligible": False,
            "reason": "Product associated with this order no longer exists in our system."
        }

    #Calculate days since purchase
    order_date = order["order_date"]
    if isinstance(order_date, str): #in data loader it already converts to date but just to be sure 
        order_date = datetime.strptime(order_date, "%Y-%m-%d")
    days_since = (datetime.now() - order_date).days

    vendor = product["vendor"]
    is_clearance = product["is_clearance"]
    is_sale = product["is_sale"]

    #Apply policy rules in order of priority

    #Clearance is always final sale
    if is_clearance:
        return {
            "eligible": False,
            "reason": "This is a clearance item. All clearance purchases are final sale — no returns or exchanges."
        }

    #Vendor: Aurelia Couture, exchanges only
    if vendor == "Aurelia Couture":
        return {
            "eligible": "exchange_only",
            "reason": "Aurelia Couture items are eligible for exchanges only, no refunds. Please contact support to initiate a size exchange if stock is available."
        }

    #Vendor: Nocturne, extended 21 day window
    if vendor == "Nocturne":
        if days_since <= 21:
            return {
                "eligible": True,
                "reason": f"Nocturne items have an extended 21-day return window. Your order was {days_since} days ago. Return accepted for full refund."
            }
        else:
            return {
                "eligible": False,
                "reason": f"Nocturne's extended return window is 21 days. Your order was {days_since} days ago. Return window has closed."
            }

    #Sale items, 7 day window, store credit only
    if is_sale:
        if days_since <= 7:
            return {
                "eligible": True,
                "reason": f"This is a sale item. Returns accepted within 7 days for store credit only. Your order was {days_since} days ago. Return accepted."
            }
        else:
            return {
                "eligible": False,
                "reason": f"Sale items must be returned within 7 days. Your order was {days_since} days ago. Return window has closed."
            }

    #Normal items, 14 day window, full refund
    if days_since <= 14:
        return {
            "eligible": True,
            "reason": f"Standard return policy applies. Returns accepted within 14 days. Your order was {days_since} days ago. Return accepted for full refund."
        }
    else:
        return {
            "eligible": False,
            "reason": f"Standard return window is 14 days. Your order was {days_since} days ago. Return window has closed."
        }