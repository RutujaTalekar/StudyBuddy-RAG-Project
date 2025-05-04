import os
from langchain_core.runnables import RunnableLambda
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# === CONFIG ===
CHROMA_PATH = "alexxu_db"
USE_FAKE_LLM = True  # Change to False later to plug in real LLM

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

    # ✅ Dummy LLM for retrieval testing only
    if USE_FAKE_LLM:
        llm = RunnableLambda(lambda input, **kwargs: "🤖 This is a fake answer. Replace with a real LLM.")
    else:
        raise NotImplementedError("Real LLM integration coming next.")

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

# === Run ===
if __name__ == "__main__":
    main()
