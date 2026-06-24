import pandas as pd

products = pd.read_csv("products.csv")

shirts = products[
    products["category"].isin([
        "formal-shirts",
        "casual-shirts",
        "linen-shirts"
    ])
]

bottoms = products[
    products["category"].isin([
        "trousers",
        "jeans",
        "chinos"
    ])
]

shoes = products[
    products["category"].isin([
        "formal-shoes",
        "loafers",
        "sandals",
        "sneakers"
    ])
]

watches = products[
    products["category"] == "watches"
]

print("SHIRTS")
print(shirts["name"])

print("\nBOTTOMS")
print(bottoms["name"])

print("\nSHOES")
print(shoes["name"])

print("\nWATCHES")
print(watches["name"])
