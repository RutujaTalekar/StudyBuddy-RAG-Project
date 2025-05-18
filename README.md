# 🤖 StudyBuddy: System Design Chatbot

StudyBuddy is an AI-powered study assistant that leverages Retrieval-Augmented Generation (RAG) to provide accurate answers to system design questions based on the "System Design Handbook" by Alex Xu. It utilizes LangChain, SentenceTransformers, ChromaDB, and Together AI to deliver contextual responses grounded in the book's content.



## 🚀 Features

- 📚 Parses & embeds your own PDF (`System Design Handbook by Alex Xu`)
- 🔍 **Retrieval-Augmented Generation (RAG)** Answers are strictly derived from the "System Design Handbook"
- 🧠 Employs SentenceTransformer embeddings for effective semantic retrieval.
- 🧑‍💻 **free & open-source**, uses **Mistral-7B** or other Together AI models for smart Q&A
- 🧾 Shows source pages so you can dive deeper in the book
- 🐳 Easy to run locally or in Docker


## ⚙️ AI Model Used
> LLM Provider: Together AI

> Model: mistralai/Mistral-7B-Instruct-v0.1

- You get $1 free credit from Together AI, which is enough for 500–1000 questions.
- To change models, update the model name in rag_query.py or pass it as a parameter.

## 🔍 Limitations & Future Work

- Currently, the chatbot retrieves answers based only on **text extracted from the PDF**.
- Images, diagrams, and other non-text visual content are **not yet parsed or processed**.
- Future updates aim to add **OCR support** to extract text from images and diagrams for enhanced context and coverage.



## 🗂️ Project Structure
```
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
```

## 🧑‍💻 Setup Instructions - Run with Docker
<ol>

<li> Clone the repo and launch the chatbot in seconds using Docker:

```bash
git clone https://github.com/RutujaTalekar/StudyBuddy-RAG-Project.git
cd StudyBuddy-RAG-Project
```

</li>

<li> Add the PDF Book
Place your legal copy of the book at the following path:

```bash
data/Alex-Xu-SysDesignHandbook.pdf
```

⚠️ This project does not include or distribute the book. You must provide your own legally obtained copy.
</li>

<li> Configure Environment Variables
Copy the example .env file and add your Together AI API key:

```bash
cp .env.example .env
```

in .env add API key

```bash
TOGETHER_API_KEY=your_together_api_key_here
```
</li>

<li> Build and Run with Docker

Build the docker image with first command and then run in interactive mode with second command. 

```bash
docker-compose build
docker-compose run --rm studybuddy
```

You'll see -
```bash
============================================================
🎓 Welcome to StudyBuddy — System Design Chatbot 📘
============================================================

❓ Your question (or 'exit'): Explain load balancing in 2 lines
```
</li>

</ol>

## 🧠 What Happens Under the Hood

When you run the chatbot **for the first time**, the following steps occur — **only if the Chroma vectorstore (`alexxu_db/`) does not already exist**:

### 🔧 One-Time Preprocessing

1. **PDF Extraction**  
   Your legally provided PDF book is parsed and converted into a structured JSON format (`book_pages.json`), with one entry per page.

2. **Text Chunking & Embedding**  
   The parsed text is split into overlapping chunks (~500 tokens), then embedded using `sentence-transformers` (`all-MiniLM-L6-v2`).

3. **Vectorstore Creation**  
   All chunks and their embeddings are stored in a local Chroma vector database (`alexxu_db/`) for fast semantic retrieval.



### 🤖 Runtime Flow (For Each Question)

4. **Semantic Retrieval**  
   When a user asks a question, relevant chunks are retrieved from the vectorstore using semantic similarity.

5. **Custom Prompt Injection**  
   The retrieved context is inserted into a carefully designed **custom prompt template**, guiding the LLM to respond based on the book.

6. **Answer Generation (LLM)**  
   A Together AI language model (e.g., `mistralai/Mistral-7B-Instruct-v0.1`) generates a grounded, natural language answer.

7. **Relevance Filtering**  
   If the retrieved passages don’t match the question well (based on keyword overlap or length), a fallback message asks the user to rephrase.


## 👩‍💻 Developer Setup (Local without Docker)
If you're contributing or prefer to run the app locally without Docker:


<ol>

<li> Install Python and Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

</li>

<li> Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ If you face version conflicts, you may want to create a fresh `.venv` and reinstall or allow pip to auto-resolve by temporarily removing specific version pins.

</li>

<li> Add the PDF

Place the Alex Xu book at:

```bash
data/Alex-Xu-SysDesignHandbook.pdf
```

</li>

<li> Set Environment Variables

Create a `.env` file using the template:

```bash
cp .env.example .env
```

Edit `.env` and paste your Together AI key:

```
TOGETHER_API_KEY=your_together_api_key_here
```

</li>

<li> Build the Vector Store

Run the following once to prepare your local vectorstore:

```bash
python3 src/extract_text.py
python3 src/build_vectorstore.py
```

</li>

<li> Start the Chatbot

Launch the terminal chatbot:

```bash
python3 src/rag_query.py
```

And that's it! you can ask your questions in the terminal!

</li>







