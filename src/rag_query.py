import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.runnables import RunnableLambda
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# === Load environment variables ===
load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


# === CONFIG ===
CHROMA_PATH = "alexxu_db"
USE_FAKE_LLM = False  # Set True to use dummy LLM

# === WRAPPER FOR EMBEDDINGS ===
class LangchainSentenceTransformer(Embeddings):
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return [vec.tolist() for vec in self.model.encode(texts)]

    def embed_query(self, text):
        return self.model.encode(text).tolist()

# === CHROMA LOADING ===
def load_vectorstore():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = LangchainSentenceTransformer(model)
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
    return vectordb

# === MAIN ===
def main():
    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    # ✅ Real LLM via OpenRouter
    if not USE_FAKE_LLM:
        llm = ChatOpenAI(
            openai_api_key=TOGETHER_API_KEY,
            openai_api_base="https://api.together.xyz/v1",
            model="mistralai/Mistral-7B-Instruct-v0.1",  # Example model
            temperature=0.3
        )
    else:
        llm = RunnableLambda(lambda input, **kwargs: "🤖 This is a fake answer.")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    print("🧠 StudyBuddy is ready! Ask a question about system design.")
    while True:
        query = input("\n❓ Your question (or 'exit'): ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        result = qa_chain.invoke(query)
        print("\n💬 Answer:")
        print(result["result"])

        print("\n📄 Referenced Pages:")
        pages = {doc.metadata["page"] for doc in result["source_documents"]}
        print(sorted(pages))

        print("\n" + "="*80 + "\n")


# === Run ===
if __name__ == "__main__":
    main()
