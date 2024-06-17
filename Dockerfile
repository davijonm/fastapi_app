FROM python:3.12

RUN apt-get update && apt-get -y install \
    graphviz \
    libaio1 \
    libgraphviz-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /mnt/code

# Copia o código-fonte do FastAPI para o contêiner
COPY ./backend .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Executa o servidor na inicialização do container
CMD ["./start.sh"]
