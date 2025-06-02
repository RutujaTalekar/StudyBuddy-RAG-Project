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
    # creating a retriever object for Semantic retrieval, return 6 most relevant chunks
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    # prompt extraction
    custom_prompt = get_custom_prompt()


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
                                    chain_type="stuff",  # explore "refine" later for better tuning
                                    chain_type_kwargs={"prompt": custom_prompt},
                                    return_source_documents=True
                                    )
    


    while True:
        query = input("\n❓ Your question (or 'exit'): ").strip()
        if not query:
            print("⚠️  Please enter a more specific question.")
            continue
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
