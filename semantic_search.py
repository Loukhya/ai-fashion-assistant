import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer

products = pd.read_csv("products.csv")

index = faiss.read_index(
    "fashion.index"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

query = input("Query: ")

query_embedding = model.encode(
    [query]
)

distances, indices = index.search(
    query_embedding.astype("float32"),
    5
)

print("\nTOP RESULTS\n")

for idx in indices[0]:
    print(
        products.iloc[idx]["name"]
    )