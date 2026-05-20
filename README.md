# AI Semantic Search Chatbot

An intelligent document Q&A tool that lets you ask natural language questions about any PDF — powered by vector embeddings and semantic similarity search.

🔗 **[Live Demo →]([https://your-streamlit-app-link-here](https://ai-semantic-search-chatbot-fggappz8g8gyqll8868au6q.streamlit.app/))**  

---

## 📌 What it does

Most search tools look for exact keyword matches. This app understands the *meaning* of your question and finds the most relevant sections of a document — even if the exact words don't match.

**Example:** Upload a resume and ask:
- *"What programming languages does this person know?"*
- *"What projects has the applicant built?"*
- *"Where is the applicant located?"*

---

## ✨ Features

- 📄 Upload any PDF document
- 🔍 Ask questions in plain English
- 🧠 Semantic search using vector embeddings (not just keyword matching)
- ⚡ Fast similarity retrieval with FAISS
- 🖥️ Clean interactive UI with Streamlit

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector Search | FAISS |
| PDF Parsing | PyPDF |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
ai-semantic-search-chatbot/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── README.md
├── src/
│   ├── loader.py           # PDF loading and text extraction
│   ├── embedding.py        # Sentence embedding generation
│   └── retrieval.py        # FAISS vector similarity search
└── data/
    └── notes.pdf           # Sample PDF for testing
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Sammyfied/ai-semantic-search-chatbot.git
cd ai-semantic-search-chatbot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Open in browser**
```
http://localhost:8501
```

---

## 🧠 How It Works

```
PDF Document
     ↓
Text Extraction (PyPDF)
     ↓
Split into chunks
     ↓
Generate vector embeddings (Sentence Transformers)
     ↓
Store in FAISS index
     ↓
User asks a question
     ↓
Question → embedding → similarity search
     ↓
Top-K most relevant chunks returned
```

---

## 📦 Dependencies

```
streamlit
sentence-transformers
faiss-cpu
pypdf
```

---

## 🔮 Planned Improvements

- [ ] Support for multiple PDF uploads
- [ ] Chat history / conversation memory
- [ ] Highlight matched sections in the original PDF
- [ ] Export answers as a summary report

---

## 👤 Author

**Samarthya** — [GitHub](https://github.com/Sammyfied) · [LinkedIn](https://linkedin.com/in/your-linkedin-here)

---

⭐ If you found this useful, consider starring the repo!

