import faiss
import numpy as np

class VectorStore:

    def __init__(self, embeddings):
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query_embedding, k=3):
        D, I = self.index.search(query_embedding, k)
        return I