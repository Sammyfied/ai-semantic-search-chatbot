import streamlit as st
from src.loader import load_pdf, chunk_text
from src.embedding import create_embeddings
from src.retrieval import VectorStore
from sentence_transformers import SentenceTransformer
import numpy as np
import google.generativeai as genai

st.set_page_config(page_title="AI Document Q&A", page_icon="🤖")
st.title("🤖 AI Document Q&A — RAG System")
st.caption("Ask any question about the document — powered by FAISS + Gemini")

# --- API Key input ---
api_key = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")
st.sidebar.caption("Get your free key at aistudio.google.com")

pdf_path = "data/notes.pdf"

def setup():
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    store = VectorStore(embeddings, chunks)
    return model, store, chunks

model, store, chunks = setup()

query = st.text_input("💬 Ask anything about the document", placeholder="e.g. What projects has Aryan built?")

if query:
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar to get answers.")
    else:
        with st.spinner("Searching document and generating answer..."):
            # Step 1 — retrieve relevant chunks
            k = min(5, len(chunks))
            query_embedding = model.encode([query])
            results = store.search(np.array(query_embedding), k=k)
            valid_results = [r for r in results if r["score"] > 0]
            context = "\n\n".join([r["chunk"] for r in valid_results])

            # Step 2 — send to Gemini
            genai.configure(api_key=api_key)
            gemini = genai.GenerativeModel("gemini-2.0-flash")

            prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the document context provided below.
If the answer is not in the context, say "I couldn't find that information in the document."
Be concise, clear, and accurate.

Document Context:
{context}

User Question: {query}

Answer:"""

            response = gemini.generate_content(prompt)
            answer = response.text

        # Display answer
        st.subheader("💡 Answer")
        st.write(answer)

        # Show retrieved chunks in expander
        with st.expander("📄 View source chunks used"):
            for i, result in enumerate(valid_results):
                st.markdown(f"**Chunk {i+1} — score: {result['score']:.2f}**")
                st.write(result["chunk"])
                st.divider()
