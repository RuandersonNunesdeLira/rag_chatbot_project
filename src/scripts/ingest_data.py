import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.core import config

DATA_PATH = "data/"
DB_PATH = config.CHROMA_DB_PATH


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    if not documents:
        print("Nenhum documento PDF encontrado no diretório 'data/'.")
        return None
    print(f"{len(documents)} documento(s) carregado(s).")
    return documents


def split_documents(documents):
    print("Dividindo documentos em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    print(f"Total de {len(texts)} chunks criados.")
    return texts


def main():
    documents = load_documents()
    if not documents:
        return

    texts = split_documents(documents)

    print("Criando embeddings e armazenando no ChromaDB...")
    if not config.OPENAI_API_KEY:
        raise ValueError(
            "A chave da API da OpenAI não foi encontrada. Verifique seu arquivo .env."
        )

    embeddings_model = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

    db = Chroma.from_documents(
        documents=texts, embedding=embeddings_model, persist_directory=DB_PATH
    )

    db.persist()
    print("Banco de dados vetorial criado e salvo com sucesso em:", DB_PATH)
    print("Processo de ingestão concluído.")


if __name__ == "__main__":
    main()
