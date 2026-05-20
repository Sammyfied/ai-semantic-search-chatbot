import faiss
import numpy as np

class VectorStore:
    def __init__(self, embeddings, chunks):
        self.chunks = chunks
        dimension = embeddings.shape[1]
        # Normalize embeddings for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized = embeddings / (norms + 1e-10)
        self.index = faiss.IndexFlatIP(normalized.shape[1])  # Inner product = cosine similarity
        self.index.add(normalized.astype(np.float32))

    def search(self, query_embedding, k=5):
        # Normalize query embedding
        norm = np.linalg.norm(query_embedding)
        normalized_query = query_embedding / (norm + 1e-10)
        D, I = self.index.search(normalized_query.astype(np.float32), k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < len(self.chunks):
                results.append({
                    "chunk": self.chunks[idx],
                    "score": float(score)
                })
        return results
