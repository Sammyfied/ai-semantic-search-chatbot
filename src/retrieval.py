import faiss
import numpy as np

class VectorStore:
    def __init__(self, embeddings, chunks):
        self.chunks = chunks
        embeddings = np.array(embeddings).astype(np.float32)
        # Normalize for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        normalized = embeddings / norms
        dimension = normalized.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(normalized)

    def search(self, query_embedding, k=3):
        query_embedding = np.array(query_embedding).astype(np.float32)
        # Normalize query
        norm = np.linalg.norm(query_embedding)
        if norm > 0:
            query_embedding = query_embedding / norm
        D, I = self.index.search(query_embedding, k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < len(self.chunks):
                results.append({
                    "chunk": self.chunks[idx],
                    "score": float(score)
                })
        return results
