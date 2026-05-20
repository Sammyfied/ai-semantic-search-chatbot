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

@st.cache_resource
def setup():
    text = load_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=300, overlap=50)
    embeddings = create_embeddings(chunks)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    store = VectorStore(embeddings, chunks)
    return model, store, chunks

model, store, chunks = setup()

query = st.text_input("💬 Ask something about the document", placeholder="e.g. What projects has the applicant built?")

if query:
    query_embedding = model.encode([query])
    results = store.search(np.array(query_embedding), k=3)

    st.subheader("Top Relevant Results")
    for i, result in enumerate(results):
        with st.expander(f"Result {i+1} — relevance score: {result['score']:.2f}"):
            st.write(result["chunk"])
