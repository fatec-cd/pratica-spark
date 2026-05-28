# Guia de Permissões - Docker no GitHub Codespaces

Este guia complementa o roteiro principal. O ambiente oficial da atividade é o **GitHub Codespaces**, portanto as orientações abaixo priorizam problemas comuns nesse ambiente.

## O que já foi preparado no projeto

### Dockerfile

- Cria o diretório `/app/data` usado pelos scripts PySpark.
- Ajusta permissões para leitura e escrita dos dados.
- Instala Java e dependências Python necessárias para executar PySpark dentro do container.
- Define um usuário não-root como padrão na imagem.

### docker-compose.yml

- Monta `./data:/app/data` para persistir datasets e resultados.
- Usa `user: root` nos serviços do Compose para evitar falhas de escrita em volumes montados no ambiente de laboratório.
- Define serviços separados para geração de dados, word count, análise de vendas, shell interativo e Jupyter.

## Verificação inicial no Codespaces

Execute no terminal do Codespaces, a partir da raiz do repositório:

```bash
python3 --version
java -version
docker --version
docker ps
docker compose version
```

Se `docker compose version` não funcionar, teste:

```bash
docker-compose --version
```

Use o comando disponível no seu ambiente.

## Problema: permission denied ao acessar o Docker daemon

Erro comum:

```text
ERROR: permission denied while trying to connect to the Docker daemon socket
```

Causa provável: o usuário do Codespaces ainda não está com permissão para acessar o daemon do Docker.

Solução rápida:

```bash
sudo usermod -aG docker $USER && newgrp docker
docker ps
```

Solução usando o script do projeto:

```bash
bash setup-docker-permissions.sh
docker ps
```

Se o erro persistir, reinicie o Codespace pelo menu `...` e execute `docker ps` novamente.

## Problema: arquivos de dados não aparecem no container

Causa provável: o comando foi executado fora do diretório `pyspark_app` ou os dados ainda não foram gerados.

Solução:

```bash
cd pyspark_app
python3 data_generator.py
docker run --rm -v "$(pwd)/data:/app/data" pyspark-app:v1.0 python3 spark_sales_analysis.py
```

## Problema: falha ao escrever em data/output

Causa provável: diretório de saída ausente ou permissões antigas em arquivos gerados por containers anteriores.

Solução:

```bash
cd pyspark_app
mkdir -p data/output
docker compose down -v
docker compose build --no-cache
docker compose up sales-analysis
```

## Comandos recomendados no Codespaces

```bash
cd pyspark_app

# Build da imagem
docker build -t pyspark-app:v1.0 .

# Gerar dados via Compose
docker compose --profile setup up data-generator

# Executar análise de vendas
docker compose up sales-analysis

# Executar word count
docker compose --profile examples up word-count
```

## Observação sobre execução local

A atividade foi desenhada para Codespaces. A execução local pode funcionar, mas fica sujeita a diferenças de sistema operacional, Docker Desktop, WSL2, Java e permissões de volume. Use execução local apenas se o professor autorizar.

## Checklist rápido

- [ ] O Codespace está aberto no fork correto.
- [ ] `./init-repo.sh` foi executado na raiz do repositório.
- [ ] `docker ps` funciona sem erro de permissão.
- [ ] Os comandos estão sendo executados dentro de `pyspark_app` quando envolvem Docker.
- [ ] O diretório `pyspark_app/data` contém os arquivos gerados.
- [ ] O diretório `pyspark_app/data/output` existe ou será criado pela análise.
