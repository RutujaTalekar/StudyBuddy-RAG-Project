# 🤖 StudyBuddy: System Design Chatbot

A lightweight, open-source chatbot to help you study **_Introduction to System Design_** by **Alex Xu**.

Ask questions. Get summaries. Understand core concepts. All powered by local PDF embeddings + Together AI LLM.



## 🚀 Features

- 🔍 **Retrieval-Augmented Generation (RAG)** for accurate, book-based answers
- 📚 Parses & embeds your own PDF (`System Design Handbook by Alex Xu`)
- 🧠 Uses **Mistral-7B** or other Together AI models for smart Q&A
- 🧾 Shows source pages so you can dive deeper in the book
- 💸 **free & open-source**, no OpenAI key required
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
git clone https://github.com/your-username/system-design-chatbot.git
cd system-design-chatbot
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
docker-compose run --rm studybuddy-chatbot
```

You'll see -
```bash
🧠 StudyBuddy is ready! Ask a question about system design.
❓ Your question (or 'exit'):   Explain CAP theorem in 2 lines
```
</li>

</ol>

## 🧠 What Happens Under the Hood
The first time you run the chatbot, the following steps are handled automatically:

- The PDF is parsed and converted to a JSON structure

- Text chunks are embedded using sentence-transformers

- A local Chroma vectorstore is built (alexxu_db/)

- Your questions are matched against the book's content

- A Together AI model (like mistralai/Mistral-7B-Instruct-v0.1) generates an answer


Example prompts:
```bash
Explain CAP theorem in 2 lines?

What are the tradeoffs of sharding?

Give me a summary of caching layers
```


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







