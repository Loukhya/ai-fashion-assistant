import pandas as pd

products = pd.read_csv("products.csv")

print("DATASET SHAPE")
print(products.shape)

print("\nCOLUMNS")
print(products.columns.tolist())

print("\nGENDER DISTRIBUTION")
print(products["gender"].value_counts())

print("\nCATEGORY DISTRIBUTION")
print(products["category"].value_counts())