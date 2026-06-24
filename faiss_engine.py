import pandas as pd
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

products = pd.read_csv("products.csv")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

texts = (
    products["name"].fillna("") + " " +
    products["category"].fillna("") + " " +
    products["occasion"].fillna("")
).tolist()

embeddings = model.encode(
    texts,
    convert_to_numpy=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    embeddings.astype("float32")
)

faiss.write_index(
    index,
    "fashion.index"
)

np.save(
    "fashion_embeddings.npy",
    embeddings
)

print("FAISS Index Created Successfully")