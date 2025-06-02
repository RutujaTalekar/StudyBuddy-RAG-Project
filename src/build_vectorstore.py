print("🚀 build_vectorstore.py is running...")

import json
import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Chroma

# Paths
JSON_PATH = "data/book_pages.json"
CHROMA_PATH = "alexxu_db"

# 1. Load book content
def load_documents(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        pages = json.load(f)
    documents = [
        Document(page["content"], metadata={"page": page["page_number"]})
        for page in pages
    ]
    return documents

# 2. Split text into chunks
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,     
        chunk_overlap=50
    )
    return splitter.split_documents(documents)

# 3. Create vector store using SentenceTransformer
def build_vectorstore(chunks, persist_path):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=LangchainSentenceTransformer(model),     # error - LangchainSentenceTransformer returns NumPy arrays, but Chroma expects a regular list of floats.
        persist_directory=persist_path
    )
    vectorstore.persist()
    return vectorstore

# Wrapper for compatibility with Langchain
from langchain.embeddings.base import Embeddings

from langchain.embeddings.base import Embeddings

class LangchainSentenceTransformer(Embeddings):
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return [vec.tolist() for vec in self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)]

    def embed_query(self, text):
        return self.model.encode(text, convert_to_numpy=True).tolist()


# Run it
if __name__ == "__main__":
    print("📂 Checking for JSON at:", JSON_PATH)

    if not os.path.exists(JSON_PATH):
        print(f"❌ Missing JSON at {JSON_PATH}")
        exit()

    print("📚 Loading pages...")
    docs = load_documents(JSON_PATH)

    print("✂️ Chunking into smaller passages...")
    chunks = chunk_documents(docs)

    print(f"🔢 Building vectorstore with {len(chunks)} chunks...")
    build_vectorstore(chunks, CHROMA_PATH)

    print("✅ Vector store created and saved to:", CHROMA_PATH)
