# ---- 1. Imagem Base ----
# Começamos com uma imagem oficial e leve do Python 3.11.
FROM python:3.11-slim

# ---- 2. Variáveis de Ambiente ----
# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Evita que o Python escreva arquivos .pyc no disco.
ENV PYTHONDONTWRITEBYTECODE 1
# Garante que a saída do Python seja exibida imediatamente nos logs do contêiner.
ENV PYTHONUNBUFFERED 1

# ---- 3. Instalação de Dependências ----
# Copia apenas o arquivo de requisitos primeiro para aproveitar o cache do Docker.
COPY requirements.txt .

# Instala as dependências. --no-cache-dir reduz o tamanho da imagem final.
RUN pip install --no-cache-dir -r requirements.txt

# ---- 4. Copiar Código da Aplicação ----
# Copia o código-fonte da aplicação para o diretório de trabalho no contêiner.
COPY ./src ./src

# ---- 5. Ingestão de Dados (Construção do Banco Vetorial) ----
# Declara um argumento que pode ser passado durante o build.
# Isso é necessário para autenticar com a OpenAI e criar os embeddings.
ARG OPENAI_API_KEY

# Copia os dados que serão ingeridos.
COPY ./data ./data

# Executa o script de ingestão. O segredo é consumido aqui e não fica na imagem final.
# O script irá criar o diretório 'db/' dentro da imagem.
RUN --mount=type=secret,id=openai_api_key \
    OPENAI_API_KEY=$(cat /run/secrets/openai_api_key) python -m src.scripts.ingest_data

# ---- 6. Expor a Porta ----
# Informa ao Docker que a aplicação dentro do contêiner escutará na porta 8000.
EXPOSE 8000

# ---- 7. Comando de Execução ----
# O comando que será executado quando o contêiner iniciar.
# Inicia o servidor Uvicorn, escutando em todas as interfaces (0.0.0.0).
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]