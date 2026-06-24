import pandas as pd

products = pd.read_csv("products.csv")

gender = "men"
occasion = "office"

# OFFICE / INTERVIEW

if occasion == "office":

    shirts = products[
        (products["gender"] == gender)
        &
        (products["category"] == "formal-shirts")
    ]

    bottoms = products[
        (products["gender"] == gender)
        &
        (products["category"] == "trousers")
    ]

    shoes = products[
        (products["gender"] == gender)
        &
        (products["category"] == "formal-shoes")
    ]

# CASUAL

else:

    shirts = products[
        (products["gender"] == gender)
        &
        (
            products["category"].isin([
                "casual-shirts",
                "linen-shirts"
            ])
        )
    ]

    bottoms = products[
        (products["gender"] == gender)
        &
        (
            products["category"].isin([
                "jeans",
                "chinos"
            ])
        )
    ]

    shoes = products[
        (products["gender"] == gender)
        &
        (
            products["category"].isin([
                "loafers",
                "sandals",
                "sneakers"
            ])
        )
    ]

watches = products[
    (products["gender"] == gender)
    &
    (products["category"] == "watches")
]

shirt = shirts.sample(1).iloc[0]
bottom = bottoms.sample(1).iloc[0]
shoe = shoes.sample(1).iloc[0]
watch = watches.sample(1).iloc[0]

print("SMART OUTFIT")
print("------------------")

print("TOPWEAR:")
print(shirt["name"])

print("\nBOTTOMWEAR:")
print(bottom["name"])

print("\nFOOTWEAR:")
print(shoe["name"])

print("\nACCESSORY:")
print(watch["name"])