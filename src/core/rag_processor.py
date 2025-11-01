from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.core import config

class RagProcessor():
    def __init__(self):
    
        self.embedding = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)

        self.chroma_db = Chroma(
            persist_directory=config.CHROMA_DB_PATH,
            embedding_function=self.embedding
            )
        
        self.llm = ChatOpenAI(api_key=config.OPENAI_API_KEY)

        self.retriever = self.chroma_db.as_retriever()

        self.prompt_base = """
            Você é um assistente de atendimento ao cliente. Use APENAS as informações do contexto abaixo para responder à pergunta no final. Se a resposta não estiver no contexto, diga 'Desculpe, não encontrei informações sobre isso.'. Não tente inventar uma resposta.

            Contexto:
            {context}

            Pergunta:
            {question}
    """

        self.dictonary = {
            "context": self.retriver,
            "question": RunnablePassthrough()
        } 

        self.prompt_template = PromptTemplate.from_template(self.prompt_base)
        
        self.chain = self.dictonary | self.prompt_template | self.llm | StrOutputParser()

    def ask(self, question: str) -> str:
        return self.chain.invoke(question)

if __name__ == "__main__":
    processor = RagProcessor()
    print(processor.ask("Vocês atendem pela Unimed ?"))