# 🤖 StudyBuddy: System Design Chatbot

A lightweight, open-source chatbot to help you study **_Introduction to System Design_** by **Alex Xu**.

Ask questions. Get summaries. Understand core concepts. All powered by local PDF embeddings + Together AI LLM.

---

## 🚀 Features

- 🔍 **Retrieval-Augmented Generation (RAG)** for accurate, book-based answers
- 📚 Parses & embeds your own PDF (`System Design Handbook` by Alex Xu)
- 🧠 Uses **Mistral-7B** or other Together AI models for smart Q&A
- 🧾 Shows source pages so you can dive deeper in the book
- 💸 100% **free & open-source**, no OpenAI key required
- 🐳 Easy to run locally or in Docker

---

## 🗂️ Project Structure

system-design-chatbot/
│
├── data/ # PDF and preprocessed JSON
│ └── Alex-Xu-SysDesignHandbook.pdf
│
├── src/ # Core logic
│ ├── extract_text.py # Convert PDF to JSON pages
│ ├── build_vectorstore.py # Chunk & embed content into ChromaDB
│ └── rag_query.py # Run the chatbot with local + cloud LLM
│
├── alexxu_db/ # ChromaDB vector store (auto-generated)
│
├── .env # (not committed) API keys
├── .env.example # ✅ Template for environment variables
├── requirements.txt # Python dependencies
└── README.md # You're reading it


---

## 🧑‍💻 Setup Instructions

### 1. Clone the repo

```bash
git clone git@github.com:your-username/system-design-chatbot.git
cd system-design-chatbot
```

### 2. Install dependencies (Python ≥ 3.10 recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Book PDF
Put your copy of the Alex Xu Book
```bash
data/Alex-Xu-SysDesignHandbook.pdf
```
⚠️ You must own a legal copy of the book. This repo does not distribute copyrighted content.

### 4. Environment Variables
Copy the example env file:
```bash
cp .env.example .env
```
Paste your Together AI key in .env:
```bash
TOGETHER_API_KEY=your_together_api_key_here
```

### 5. Build Knowledge Base
Step 1: Extract & preprocess
```bash
python3 src/extract_text.py
```
This will parse the book PDF and generate a JSON file data/book_pages.json.


Step 2: Build Chroma vectorstore
```bash
python3 src/build_vectorstore.py
```
This step:

- Splits the book into semantic chunks
- Converts them into vector embeddings
- Stores them in alexxu_db/ using ChromaDB

You only need to run this again if the source book changes.

### 5. Run the ChatBot

```bash
python3 src/rag_query.py

```
Example prompts:

"Explain CAP theorem in 2 lines"

"What are the tradeoffs of sharding?"

"Give me a summary of caching layers"

The chatbot uses your local vectorstore to fetch top-matching passages from the book, and Together AI to generate accurate responses.

## ⚙️ Model Used
LLM Provider: Together AI
Model: mistralai/Mistral-7B-Instruct-v0.1

🪙 You get $1 free credit from Together AI, which is enough for 500–1000 questions.
To change models, update the model name in rag_query.py or pass it as a parameter.










