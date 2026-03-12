import streamlit as st
from src.loader import load_pdf
from src.embedding import create_embeddings
from sentence_transformers import SentenceTransformer
import numpy as np

st.title("AI Resume Chatbot (Semantic Search)")

pdf_path = "data/notes.pdf"

text = load_pdf(pdf_path)

chunks = [chunk for chunk in text.split("\n") if chunk.strip() != ""]

embeddings = create_embeddings(chunks)

model = SentenceTransformer("all-MiniLM-L6-v2")

query = st.text_input("Ask something about the document")

if query:

    query_embedding = model.encode([query])

    similarities = np.dot(embeddings, query_embedding.T).flatten()

    top_k = 3
    top_indices = similarities.argsort()[-top_k:][::-1]

    st.subheader("Top Relevant Results")

    for i in top_indices:
        st.write(chunks[i])