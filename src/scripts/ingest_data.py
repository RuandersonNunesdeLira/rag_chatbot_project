import os
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from src.core.config import GOOGLE_API_KEY, CHROMA_DB_PATH

if not GOOGLE_API_KEY:
    raise ValueError("A chave da API do Google não foi encontrada. Verifique seu arquivo .env.")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

def load_documents(directory='data'):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    
    return documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


def store_embeddings(chunks, persist_directory=CHROMA_DB_PATH):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = chromadb.PersistentClient(path=persist_directory)

    from langchain_community.vectorstores.chroma import Chroma

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return db


def main():
    if not os.path.exists(CHROMA_DB_PATH):
        os.makedirs(CHROMA_DB_PATH)

    documents = load_documents()
    if documents:
        chunks = split_documents(documents)
        store_embeddings(chunks)
    else:
        print("Nenhum documento encontrado para processar.")


if __name__ == "__main__":
    main()
