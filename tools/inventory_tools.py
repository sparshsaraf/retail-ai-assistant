from data_loader import INVENTORY

def search_products(tags=None, size=None, max_price=None, is_sale=None, is_clearance=None) -> list[dict]:
    df = INVENTORY.copy().reset_index(drop=True)

    if tags:
        def match_score(product_tags):
            return sum(1 for tag in tags if tag.lower() in [x.lower() for x in product_tags])
        scores = df["tags"].apply(match_score)
        df = df[scores >= 1].reset_index(drop=True)
        if df.empty:
            return[]
        df["match_score"] = df["tags"].apply(match_score)
        df = df.sort_values(["match_score", "bestseller_score"], ascending=[False, False]).reset_index(drop=True)
    else:
        df = df.sort_values("bestseller_score", ascending=False).reset_index(drop=True)

    if size:
        if df.empty:
            return []
        s = str(size)
        df = df[df["sizes_available"].apply(lambda x: s in x)].reset_index(drop=True)
        df = df[df["stock_per_size"].apply(lambda x: x.get(s, 0) > 0)].reset_index(drop=True)

    if max_price is not None:
        df = df[df["price"] <= max_price].reset_index(drop=True)

    if is_sale is not None:
        df = df[df["is_sale"] == is_sale].reset_index(drop=True)

    if is_clearance is not None:
        df = df[df["is_clearance"] == is_clearance].reset_index(drop=True)

    if "match_score" in df.columns:
        df = df.drop(columns=["match_score"])

    return df.head(3).to_dict(orient="records")


def get_product(product_id: str) -> dict | None:
    df = INVENTORY[INVENTORY["product_id"] == product_id]
    if df.empty:
        return None
    return df.iloc[0].to_dict()