import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from prompt_template import get_custom_prompt
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
CHROMA_PATH = "alexxu_db"
USE_FAKE_LLM = False


class LangchainSentenceTransformer(Embeddings):
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return [vec.tolist() for vec in self.model.encode(texts)]

    def embed_query(self, text):
        return self.model.encode(text).tolist()


def load_vectorstore():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = LangchainSentenceTransformer(model)
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
    return vectordb
            
def main():

    print("=" * 60)
    print("🎓 Welcome to StudyBuddy — System Design Chatbot 📘")
    print("=" * 60)

    vectordb = load_vectorstore()
    # Semantic retrieval
    retriever = vectordb.as_retriever(search_kwargs={"k": 6})
    # Prompt extraction
    custom_prompt = get_custom_prompt()

    if not USE_FAKE_LLM:
        llm = ChatOpenAI(
            openai_api_key=TOGETHER_API_KEY,
            openai_api_base="https://api.together.xyz/v1",
            model="mistralai/Mistral-7B-Instruct-v0.1",
            temperature=0.3,
        )
    else:
        llm = RunnableLambda(lambda input, **kwargs: "🤖 This is a fake answer.")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True,
    )

    while True:
        query = input("\n❓ Your question (or 'exit'): ").strip()
        if not query:
            print("⚠️  Please enter a more specific question.")
            continue
        if query.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break
        

        result = qa_chain.invoke(query.lower().strip())

        source_docs = result.get("source_documents", [])
        top_chunks = [doc.page_content for doc in source_docs if doc.page_content.strip()]
        query_keywords = set(query.lower().split())
        
        if not top_chunks or all(len(chunk) < 30 for chunk in top_chunks) or not any(
            any(word in doc.page_content.lower() for word in query_keywords) for doc in source_docs):
            print("\n💬 Answer:")
            print("⚠️ Sorry, I couldn't find anything relevant in the book. Please try rephrasing.")
            continue  # skip to next prompt
        
        else:
            print("\n💬 Answer:")
            print(result["result"])
            print("\n📄 Referenced Pages:")
            pages = {doc.metadata.get("page") for doc in source_docs if doc.metadata.get("page") is not None}
            print(sorted(pages))

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
