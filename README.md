# AI Semantic Search Chatbot

## Overview
This project demonstrates a semantic search system that allows users to ask questions about a PDF document (such as a resume).

The system converts text into vector embeddings and retrieves the most relevant sections using similarity search.

## Features
- Semantic search on PDF documents
- Vector embeddings using Sentence Transformers
- Top-K relevant result retrieval
- Interactive UI using Streamlit

## Technologies Used
- Python
- Streamlit
- Sentence Transformers
- FAISS (vector similarity search)
- PyPDF

## Project Structure

endee-project
│
├── app.py
├── requirements.txt
├── README.md
├── src
│   ├── loader.py
│   ├── embedding.py
│   └── retrieval.py
└── data
    └── notes.pdf

## How to Run

1. Install dependencies

pip install -r requirements.txt

2. Run the application

streamlit run app.py

3. Open browser

http://localhost:8501

## Example Questions

- Who is the applicant?
- What skills does the applicant have?
- What is the applicant's location?