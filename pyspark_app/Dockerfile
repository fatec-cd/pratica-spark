# Imagem base leve com Python; Spark será fornecido via pacote PySpark em requirements.txt
FROM python:3.11-slim

# Metadata
LABEL maintainer="estudante@cienciadados.edu"
LABEL description="PySpark Application for Big Data Analytics"

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala Java 17 necessário pelo PySpark
# Debian Bookworm usa temurin ou default-jdk para Java 17
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jdk-headless \
        procps \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Configura JAVA_HOME (detecta automaticamente a versão instalada)
RUN JAVA_HOME_PATH=$(dirname $(dirname $(readlink -f $(which java)))) && \
    echo "export JAVA_HOME=$JAVA_HOME_PATH" >> /etc/profile && \
    echo "JAVA_HOME detectado: $JAVA_HOME_PATH"

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="$JAVA_HOME/bin:$PATH"

# Define diretório de trabalho
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Instala dependências Python (inclui pyspark)
RUN pip install --no-cache-dir -r requirements.txt

# Cria diretórios necessários com permissões adequadas
RUN useradd -ms /bin/bash spark && \
    mkdir -p /app/data /app/data/output && \
    chown -R spark:spark /app && \
    chmod -R 777 /app/data

# Copia scripts Python
COPY *.py ./

# Torna scripts executáveis e ajusta proprietário
RUN chmod +x *.py && chown -R spark:spark /app

# Executa como usuário não-root por segurança
USER spark

# Define comando padrão
CMD ["python3", "spark_sales_analysis.py"]
