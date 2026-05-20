import streamlit as st
from src.loader import load_pdf, chunk_text
from src.embedding import create_embeddings
from src.retrieval import VectorStore
from sentence_transformers import SentenceTransformer
import numpy as np

st.set_page_config(page_title="AI Semantic Search Chatbot", page_icon="🔍")
st.title("🔍 AI Semantic Search Chatbot")
st.caption("Ask any question about the document — powered by vector embeddings")

pdf_path = "data/notes.pdf"

def setup():
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    store = VectorStore(embeddings, chunks)
    return model, store, chunks

model, store, chunks = setup()

query = st.text_input("💬 Ask something about the document", placeholder="e.g. What projects has Aryan built?")

if query:
    k = min(3, len(chunks))
    query_embedding = model.encode([query])
    results = store.search(np.array(query_embedding), k=k)
    valid_results = [r for r in results if r["score"] > 0]

    st.subheader("Top Relevant Results")
    if valid_results:
        for i, result in enumerate(valid_results):
            with st.expander(f"Result {i+1} — relevance score: {result['score']:.2f}"):
                st.write(result["chunk"])
    else:
        st.info("No relevant results found. Try rephrasing your question.")
