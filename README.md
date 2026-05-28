# Atividade Prática: PySpark com Python e Docker

## Informações Gerais

**Público-alvo:** Alunos de graduação em Ciência de Dados  
**Temática:** Infraestrutura para projetos de Big Data com Apache Spark  
**Nível:** Intermediário

---

## Objetivos de Aprendizagem

Ao final desta atividade, você será capaz de:

1. Compreender a arquitetura e conceitos fundamentais do Apache Spark
2. Implementar transformações e ações em PySpark
3. Processar dados estruturados e não estruturados usando DataFrames e RDDs
4. Containerizar aplicações Spark usando Docker
5. Aplicar operações de análise de dados em larga escala
6. Comparar o paradigma Spark com MapReduce tradicional

---

## Pré-requisitos

- Conhecimento básico de Python
- Familiaridade com linha de comando (terminal/bash)
- Conceitos básicos de SQL (desejável)
- Conta no GitHub com acesso ao GitHub Codespaces
- Navegador web moderno

---

## Recursos Necessários

Esta atividade foi revisada para ser executada integralmente no **GitHub Codespaces**, sem instalação local de Python, Java, Spark ou Docker.

- **GitHub Codespaces**: ambiente de desenvolvimento na nuvem
- **Docker dentro do Codespaces**: usado para construir e executar a aplicação containerizada
- **Scripts do repositório**: usados para preparar dependências, dados e diretórios
- **Dataset**: Dados de vendas de e-commerce para análise

### Como usar este roteiro

Siga as partes na ordem. Cada checkpoint indica o que deve estar funcionando antes de avançar. Se um comando falhar, consulte primeiro o **Apêndice A: Troubleshooting**, pois ele reúne os problemas mais comuns em Codespaces.

Ao longo da atividade, procure diferenciar três camadas:

1. **Conceito**: o que Spark faz e por que faz dessa forma
2. **Implementação**: como o conceito aparece nos scripts PySpark
3. **Infraestrutura**: como Docker e Codespaces tornam a execução reprodutível

---

## Parte 1: Fundamentos do Apache Spark

### 1.1 O que é Apache Spark?

Apache Spark é um framework de processamento de dados distribuído de código aberto, projetado para ser **rápido**, **escalável** e **fácil de usar**. Foi desenvolvido na UC Berkeley em 2009 e se tornou um projeto Apache em 2013.

#### Principais Características:

- **Velocidade**: Até 100x mais rápido que MapReduce (processamento em memória)
- **Facilidade de uso**: APIs em Python, Scala, Java, R e SQL
- **Generalidade**: Suporta batch, streaming, ML, grafos
- **Execução**: Local, cluster (Standalone, YARN, Mesos, Kubernetes)

### 1.2 Arquitetura do Spark

```
┌─────────────────────────────────────────────────────────────┐
│                      SPARK APPLICATION                      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              DRIVER PROGRAM                          │   │
│  │  • SparkContext/SparkSession                         │   │
│  │  • Converte programa em tarefas                      │   │
│  │  • Agenda tarefas nos executors                      │   │
│  │  • Monitora execução                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              CLUSTER MANAGER                           │ │
│  │  • Standalone / YARN / Mesos / Kubernetes              │ │
│  │  • Gerencia recursos do cluster                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         ▼                 ▼                 ▼               │
│  ┌───────────┐     ┌───────────┐     ┌───────────┐          │
│  │ EXECUTOR  │     │ EXECUTOR  │     │ EXECUTOR  │          │
│  │ ┌───────┐ │     │ ┌───────┐ │     │ ┌───────┐ │          │
│  │ │ Task  │ │     │ │ Task  │ │     │ │ Task  │ │          │
│  │ ├───────┤ │     │ ├───────┤ │     │ ├───────┤ │          │
│  │ │ Task  │ │     │ │ Task  │ │     │ │ Task  │ │          │
│  │ └───────┘ │     │ └───────┘ │     │ └───────┘ │          │
│  │  Cache    │     │  Cache    │     │  Cache    │          │
│  └───────────┘     └───────────┘     └───────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Componentes da Arquitetura:

1. **Driver Program**:
   - Executa a função `main()` da aplicação
   - Cria o SparkContext/SparkSession
   - Converte o código em um DAG (Directed Acyclic Graph)
   - Divide o DAG em stages e tasks
   - Agenda tasks para execução

2. **Cluster Manager**:
   - Gerencia recursos do cluster
   - Aloca recursos para a aplicação
   - Tipos: Standalone, YARN, Mesos, Kubernetes

3. **Executors**:
   - Processos que executam as tasks
   - Armazenam dados em cache/memória
   - Enviam resultados ao driver

4. **Tasks**:
   - Menor unidade de trabalho
   - Enviadas aos executors
   - Processam partições de dados

### 1.3 Conceitos Fundamentais

#### RDD (Resilient Distributed Dataset)

RDD é a abstração fundamental do Spark - uma coleção distribuída e imutável de objetos.

**Características:**
- **Resiliente**: Recupera-se de falhas automaticamente
- **Distribuído**: Dados particionados através do cluster
- **Dataset**: Coleção de dados

**Criação de RDD:**
```python
# A partir de uma coleção
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])

# A partir de arquivo
rdd = spark.sparkContext.textFile("data/input.txt")
```

#### DataFrames

DataFrames são coleções distribuídas de dados organizados em colunas nomeadas (similar a tabelas SQL ou DataFrames do pandas).

**Vantagens:**
- Otimização automática (Catalyst Optimizer)
- Suporte a SQL
- Schema definido
- Melhor performance que RDDs

**Criação de DataFrame:**
```python
# A partir de arquivo CSV
df = spark.read.csv("data/sales.csv", header=True, inferSchema=True)

# A partir de dados em memória
data = [(1, "João", 1000), (2, "Maria", 1500)]
df = spark.createDataFrame(data, ["id", "nome", "salario"])
```

#### Transformações vs Ações

**Transformações** (Lazy - não executam imediatamente):
- `map()`, `filter()`, `groupBy()`, `join()`, `select()`, `where()`
- Criam um novo RDD/DataFrame
- Exemplo: `df.filter(df.age > 18)`

**Ações** (Eager - disparam execução):
- `count()`, `collect()`, `first()`, `show()`, `save()`
- Retornam valores ao driver
- Exemplo: `df.count()`

### 1.4 Execução Lazy (Lazy Evaluation)

Spark utiliza **avaliação preguiçosa**: transformações não são executadas imediatamente.

**Fluxo de Execução:**
```
Código → DAG → Logical Plan → Physical Plan → Execução
```

1. **DAG Creation**: Spark constrói um grafo de dependências
2. **Logical Plan**: Otimizações lógicas (Catalyst)
3. **Physical Plan**: Escolha do melhor plano físico
4. **Execution**: Tasks são executadas nos executors

**Exemplo:**
```python
# Nada é executado aqui
df_filtered = df.filter(df.age > 18)
df_selected = df_filtered.select("name", "age")

# Somente aqui a execução acontece
result = df_selected.count()  # Ação dispara o processamento
```

### 1.5 Spark vs MapReduce

| Característica | MapReduce | Spark |
|---------------|-----------|-------|
| **Velocidade** | Mais lento (disco) | Até 100x mais rápido (memória) |
| **Facilidade** | Complexo (Java) | Simples (Python, Scala, SQL) |
| **Processamento** | Batch apenas | Batch, Streaming, ML, Grafos |
| **Iterações** | Lento (I/O disco) | Rápido (cache em memória) |
| **APIs** | Baixo nível | Alto nível (DataFrames, SQL) |
| **Uso** | Hadoop específico | Multi-plataforma |

### ✅ Checkpoint 1.1

Antes de prosseguir, responda:

- [ ] Você compreende a diferença entre Driver e Executor?
- [ ] Você entende o que são RDDs e DataFrames?
- [ ] Você sabe a diferença entre Transformações e Ações?
- [ ] Você compreende o conceito de Lazy Evaluation?
- [ ] Você consegue comparar Spark com MapReduce?

---

## Importante: ambiente padronizado da atividade

O ambiente oficial desta atividade é o **GitHub Codespaces**. Isso reduz diferenças entre Windows, macOS e Linux e evita que a execução dependa de instalações locais.

Antes de iniciar a parte prática, confirme estes pontos no terminal do Codespaces:

```bash
python3 --version
java -version
docker --version
docker compose version
```

Se `docker compose version` não funcionar, teste:

```bash
docker-compose --version
```

Use o comando disponível no seu Codespace. No roteiro, o padrão será `docker compose`, que é o comando atual do Docker Compose.

### Situações que podem prejudicar a execução

| Situação | Como prevenir ou corrigir |
|---|---|
| Dependências Python ausentes | Execute `./init-repo.sh` antes da Parte 4 |
| Erro de permissão no Docker | Execute `bash setup-docker-permissions.sh` ou reinicie o Codespace |
| Dataset não encontrado | Execute `python3 data_generator.py` dentro de `pyspark_app` |
| Comando `docker-compose` indisponível | Use `docker compose` |
| Build Docker lento na primeira execução | Aguarde o download das camadas; isso é esperado |
| Codespace parado ou expirado | Reabra o Codespace pelo GitHub; faça commits para preservar alterações |

**Para detalhes sobre volumes e permissões**, consulte [pyspark_app/PERMISSIONS_GUIDE.md](pyspark_app/PERMISSIONS_GUIDE.md).

---

## Parte 2: Caso de Uso - Análise de Vendas de E-commerce

### 2.1 Contexto do Problema

**Cenário**: Uma empresa de e-commerce precisa analisar suas vendas para tomar decisões estratégicas.

**Objetivos da Análise**:
1. Calcular receita total por categoria de produto
2. Identificar os produtos mais vendidos
3. Analisar padrões de vendas por região
4. Calcular ticket médio por cliente
5. Identificar tendências temporais de vendas

**Dataset**: `sales_data.csv`

**Estrutura dos dados:**
```csv
transaction_id,date,customer_id,product_id,product_name,category,quantity,price,region
TX001,2024-01-15,C101,P501,Notebook,Eletrônicos,1,2500.00,Sudeste
TX002,2024-01-15,C102,P502,Mouse,Eletrônicos,2,45.00,Sul
TX003,2024-01-16,C103,P503,Livro,Livros,3,35.00,Nordeste
...
```

**Campos:**
- `transaction_id`: ID único da transação
- `date`: Data da venda
- `customer_id`: ID do cliente
- `product_id`: ID do produto
- `product_name`: Nome do produto
- `category`: Categoria do produto
- `quantity`: Quantidade vendida
- `price`: Preço unitário
- `region`: Região da venda

### 2.2 Análises a Realizar

#### Análise 1: Receita Total por Categoria
Calcular a receita total (quantidade × preço) agrupada por categoria.

#### Análise 2: Top 10 Produtos Mais Vendidos
Identificar os 10 produtos com maior volume de vendas.

#### Análise 3: Vendas por Região
Analisar a distribuição de vendas entre as regiões do Brasil.

#### Análise 4: Ticket Médio por Cliente
Calcular o valor médio gasto por cada cliente.

#### Análise 5: Análise Temporal
Identificar tendências de vendas ao longo do tempo (diária/mensal).

### ✅ Checkpoint 2.1

Verifique:

- [ ] Você compreende o contexto do problema de negócio?
- [ ] Você entende a estrutura dos dados?
- [ ] Você sabe quais análises precisam ser realizadas?
- [ ] Você consegue pensar em como o Spark pode ajudar?

---

## Parte 3: Configuração do Ambiente

### 3.1 Fazendo Fork e Clonando o Repositório no GitHub Codespaces

**Passo 1:** Acesse https://github.com e faça login

**Passo 2:** Faça um fork do repositório do laboratório

1. Acesse o repositório original fornecido pelo professor
2. Clique no botão "Fork" no canto superior direito
3. Selecione sua conta como destino do fork
4. Aguarde a criação do fork (alguns segundos)

**Passo 3:** Clone seu fork usando GitHub Codespaces

1. No seu fork, clique no botão verde "Code"
2. Selecione a aba "Codespaces"
3. Clique em "Create codespace on main"
4. Aguarde o ambiente carregar (pode levar 2-3 minutos - Spark requer mais recursos)

**Passo 4:** Prepare o ambiente do laboratório

No terminal do Codespaces, execute o script de preparação. Ele verifica Python, Docker e Java, instala as dependências Python e gera os dados iniciais.

```bash
chmod +x init-repo.sh setup-docker-permissions.sh
./init-repo.sh
```

Critério de sucesso: ao final, o terminal deve mostrar que o setup foi concluído e que os dados de exemplo foram gerados.

**Passo 5:** Verifique o ambiente antes de avançar

```bash
python3 --version
java -version
docker --version
docker ps
docker compose version
```

Se `docker ps` retornar erro de permissão, execute:

```bash
bash setup-docker-permissions.sh
```

Se ainda houver problema, reinicie o Codespace: clique nos três pontos `...`, selecione **Restart Codespace**, aguarde reiniciar e teste novamente com `docker ps`.

**Passo 6:** Explore a estrutura do projeto

```bash
ls -la pyspark_app/
```

Você verá:
- `spark_sales_analysis.py` - Script principal de análise
- `spark_word_count.py` - Exemplo simples (Word Count)
- `data_generator.py` - Gerador de dados de vendas
- `Dockerfile` - Configuração do container
- `requirements.txt` - Dependências Python
- `data/` - Diretório com datasets de exemplo

**Pergunta de reflexão:** por que é importante validar o ambiente antes de analisar os scripts? Pense em quais erros seriam causados por falta de dependências, por ausência do dataset ou por problemas de permissão no Docker.

### ✅ Checkpoint 3.1

Verifique:

- [ ] Fork do repositório foi criado com sucesso
- [ ] Repositório foi clonado no Codespaces
- [ ] Python 3.x está instalado
- [ ] Java está instalado
- [ ] Dependências Python foram instaladas pelo `init-repo.sh`
- [ ] Dados de exemplo foram gerados
- [ ] Docker está disponível
- [ ] `docker ps` executa sem erro de permissão
- [ ] Todos os arquivos da aplicação estão presentes
- [ ] Você consegue visualizar os scripts Python

---

## Parte 4: Implementação com PySpark

### 4.1 Explorando a Estrutura do Projeto

O repositório já contém todos os scripts necessários. Nesta parte, você vai executar primeiro um exemplo pequeno e depois uma análise de negócio completa. A intenção é observar como os conceitos da Parte 1 aparecem em código real.

```bash
cd pyspark_app
ls -la
```

Estrutura esperada:

```
pyspark_app/
├── spark_sales_analysis.py    # Análise completa de vendas
├── spark_word_count.py         # Exemplo básico
├── data_generator.py           # Gera dados de teste
├── spark_stream_example.py     # Exemplo de streaming
├── Dockerfile                  # Imagem Docker com Spark
├── requirements.txt            # Dependências
├── docker-compose.yml          # Orquestração
└── data/                       # Datasets
    ├── sales_data.csv          # Dados de vendas
    ├── products.csv            # Catálogo de produtos
    └── input.txt               # Texto para word count
```

### 4.2 Entendendo o Dataset

Se você já executou `./init-repo.sh`, os dados de exemplo já foram criados. Caso queira recriar os arquivos, execute:

```bash
python3 data_generator.py
```

Visualize o conteúdo:

```bash
head -20 data/sales_data.csv
```

Observe:
- Quais colunas representam dimensões de análise, como categoria e região?
- Quais colunas permitem calcular métricas, como quantidade, preço e receita?
- Cada linha representa qual evento de negócio?

### 4.3 Exemplo Simples: Word Count com PySpark

Antes da análise completa, vamos executar um exemplo simples para entender os conceitos:

```bash
cat spark_word_count.py
```

Execute o exemplo:

```bash
python3 spark_word_count.py
```

**O que este script faz:**
1. Cria uma SparkSession
2. Lê um arquivo de texto
3. Aplica transformações (split, flatMap, map, reduceByKey)
4. Executa uma ação (collect/show)

**Critério de sucesso:** o terminal deve exibir rankings de palavras e o plano de execução do Spark. Use essa saída para identificar onde aparecem transformações, ações e lazy evaluation.

### 4.4 Análise de Vendas - Parte 1: Carregamento e Exploração

Abra o arquivo `spark_sales_analysis.py` e analise o código:

```bash
cat spark_sales_analysis.py
```

**Seção 1: Inicialização**
- Cria SparkSession
- Configura memória e cores

**Seção 2: Carregamento de Dados**
- Lê CSV com schema inference
- Valida dados carregados

**Seção 3: Exploração Inicial**
- Exibe schema
- Mostra primeiras linhas
- Calcula estatísticas

### 4.5 Análise de Vendas - Parte 2: Transformações e Agregações

**Análise Implementada:**

1. **Receita por Categoria**
```python
df.withColumn("revenue", col("quantity") * col("price"))
  .groupBy("category")
  .agg(sum("revenue").alias("total_revenue"))
  .orderBy(desc("total_revenue"))
```

2. **Top Produtos**
```python
df.groupBy("product_name")
  .agg(sum("quantity").alias("total_sold"))
  .orderBy(desc("total_sold"))
  .limit(10)
```

3. **Vendas por Região**
```python
df.groupBy("region")
  .agg(
    count("*").alias("num_transactions"),
    sum(col("quantity") * col("price")).alias("total_revenue")
  )
```

### 4.6 Executando a Análise Completa

Execute o script de análise:

```bash
python3 spark_sales_analysis.py
```

Observe a saída:
- Schema do DataFrame
- Estatísticas descritivas
- Resultados de cada análise
- Métricas de performance
- Diretórios criados em `data/output/`

**Pergunta de reflexão:** quais análises exigem apenas agregação? Quais poderiam exigir join, janela temporal ou cache se o volume de dados fosse maior?

### ✅ Checkpoint 4.1

Verifique:

- [ ] Você conseguiu gerar os dados de vendas?
- [ ] O exemplo de Word Count executou com sucesso?
- [ ] A análise de vendas foi executada completamente?
- [ ] Você compreende as transformações utilizadas?
- [ ] Os resultados fazem sentido do ponto de vista de negócio?

---

## Parte 5: Containerização com Docker

### 5.1 Entendendo o Dockerfile

Examine o Dockerfile:

```bash
cat Dockerfile
```

**Componentes:**
- Imagem base com Spark e Python
- Instalação de dependências
- Configuração do ambiente Spark
- Cópia dos scripts

### 5.2 Construindo a Imagem Docker

Antes do build, confirme que o Docker está acessível:

```bash
docker ps
```

Se houver erro de permissão, volte ao Apêndice A ou execute `bash setup-docker-permissions.sh` no diretório raiz do repositório.

Construa a imagem:

```bash
# Navegar para o diretório correto
cd pyspark_app

# Construir a imagem
docker build -t pyspark-app:v1.0 .
```

Aguarde o build. Na primeira execução, ele pode levar alguns minutos porque o Codespaces precisa baixar camadas da imagem e dependências.

**Verificar a imagem criada:**
```bash
docker images | grep pyspark-app
```

### 5.3 Executando o Container

**Opção 1: Executar análise de vendas**
```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  pyspark-app:v1.0 \
  python3 spark_sales_analysis.py
```

Critério de sucesso: a saída deve mostrar as mesmas análises da execução local e atualizar os resultados em `data/output/`.


**Opção 2: Executar word count**
```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  pyspark-app:v1.0 \
  python3 spark_word_count.py
```


### 5.4 Docker Compose

Para orquestração mais simples, use Docker Compose:

```bash
# Análise de vendas
docker compose up sales-analysis

# Word count
docker compose up word-count

# PySpark Shell interativo
docker compose up pyspark-shell
```

Se o comando `docker compose` não estiver disponível no seu Codespace, use `docker-compose` nos três comandos acima.

Para encerrar um serviço interativo que não voltou ao prompt, pressione `Ctrl+C`.

### ✅ Checkpoint 5.1

Verifique:

- [ ] A imagem Docker foi construída com sucesso?
- [ ] Os containers executam sem erros?
- [ ] Os volumes estão montados corretamente?
- [ ] Você consegue acessar os resultados?
- [ ] O Docker Compose está funcionando?

---

## Parte 6: Entregáveis da Atividade

### 6.1 O que deve ser entregue

Para comprovar a conclusão desta atividade prática, você deverá entregar **screenshots** das execuções na tarefa do Microsoft Teams atribuída ao aluno.

### 6.2 Lista de Screenshots Obrigatórios

Capture e envie os seguintes screenshots na tarefa do Teams:

**1. Fork do Repositório**
- Screenshot mostrando seu fork do repositório no GitHub

**2. Codespaces em Execução**
- Screenshot do GitHub Codespaces aberto com os arquivos do projeto

**3. Estrutura do Projeto**
- Screenshot do terminal mostrando a estrutura de arquivos com `ls -la pyspark_app/`

**4. Geração de Dados**
- Screenshot da execução do `data_generator.py` mostrando a criação dos arquivos CSV

**5. Execução do Word Count**
- Screenshot da execução completa do `spark_word_count.py` mostrando os resultados

**6. Análise de Vendas - Schema**
- Screenshot mostrando o schema do DataFrame de vendas

**7. Análise de Vendas - Receita por Categoria**
- Screenshot mostrando os resultados da análise de receita por categoria

**8. Análise de Vendas - Top 10 Produtos**
- Screenshot mostrando os 10 produtos mais vendidos

**9. Análise de Vendas - Vendas por Região**
- Screenshot mostrando a distribuição de vendas por região

**10. Docker Build**
- Screenshot mostrando o build da imagem Docker com sucesso

**11. Docker Images**
- Screenshot do comando `docker images` mostrando a imagem `pyspark-app:v1.0` criada

**12. Execução no Container**
- Screenshot mostrando a análise de vendas executando dentro do container Docker

**13. Docker Compose**
- Screenshot mostrando a execução com `docker compose up sales-analysis`

### 6.3 Orientações para os Screenshots

**Requisitos para os screenshots:**

1. **Qualidade**: Screenshots devem estar legíveis e em resolução adequada
2. **Conteúdo completo**: Capture toda a saída relevante do comando/execução
3. **Formato**: PNG ou JPG

**Como capturar screenshots:**
- Windows: `Windows + Shift + S`
- Mac: `Cmd + Shift + 4`
- Linux: `Print Screen` ou `Gnome Screenshot`

### 6.4 Como Entregar

1. Capture todos os 13 screenshots obrigatórios
2. Nomeie os arquivos de forma descritiva (ex: `01_fork_repositorio.png`, `02_codespaces.png`, etc.)
3. Envie todos os screenshots na **tarefa do Microsoft Teams** atribuída
4. Certifique-se de que todos os screenshots estão legíveis antes de enviar

### 6.5 Checklist Pré-Entrega

Antes de submeter, verifique:

- [ ] Todos os 13 screenshots obrigatórios foram capturados
- [ ] Screenshots estão legíveis e mostram informações completas
- [ ] Arquivos estão nomeados de forma clara
- [ ] Todos os scripts executaram corretamente
- [ ] A imagem Docker foi construída com sucesso
- [ ] As análises produziram resultados coerentes

### 6.6 Dúvidas Frequentes

**P: Preciso publicar a imagem Docker em algum registry?**  
R: Não. Para esta entrega, basta ter evidências de que a imagem foi construída e executada no Codespaces.

**P: O que fazer se meu Codespaces expirar?**  
R: Você pode recriar o Codespace do seu fork. Os arquivos estarão lá se você fez commit.

**P: Posso trabalhar localmente ao invés de usar Codespaces?**  
R: Para esta atividade, use Codespaces como ambiente padrão. A execução local só deve ser usada se o professor autorizar, pois diferenças de sistema operacional, Docker, Java e permissões podem alterar os resultados.

---

## Parte 7: Recursos Adicionais e Próximos Passos

### 7.1 Conceitos Avançados para Estudo

1. **Spark SQL**: Queries SQL em DataFrames
2. **Spark Streaming**: Processamento de dados em tempo real
3. **Spark MLlib**: Machine Learning distribuído
4. **GraphX**: Processamento de grafos
5. **Delta Lake**: ACID transactions em Data Lakes

### 7.2 Recursos de Aprendizagem

**Documentação Oficial**:
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)

**Cursos Online**:
- [Databricks Academy](https://www.databricks.com/learn/training)
- [Coursera - Big Data Specialization](https://www.coursera.org/specializations/big-data)

**Livros**:
- "Learning Spark" (O'Reilly)
- "Spark: The Definitive Guide" (O'Reilly)

**Comunidade**:
- [Stack Overflow - Apache Spark](https://stackoverflow.com/questions/tagged/apache-spark)
- [Spark User Mailing List](https://spark.apache.org/community.html)

### 7.3 Próximos Passos

1. **Deploy em Cluster**: Configure Spark em modo cluster (Standalone/YARN)
2. **Integração com Cloud**: Use AWS EMR, Azure Databricks ou GCP Dataproc
3. **Streaming**: Implemente processamento em tempo real com Kafka
4. **Machine Learning**: Crie modelos preditivos com MLlib
5. **Otimização**: Aprenda técnicas de tuning e particionamento

### 7.4 Certificações

- **Databricks Certified Associate Developer for Apache Spark**
- **Cloudera Certified Spark and Hadoop Developer**

---

## Apêndice A: Troubleshooting

### Problema: "Permission denied" ao acessar Docker daemon no Codespaces

Este é o problema **mais comum** ao executar o item 5.2 do roteiro no GitHub Codespaces.

**Erro completo**:
```
ERROR: permission denied while trying to connect to the Docker daemon socket at 
unix:///var/run/docker.sock: Head "http://%2Fvar%2Frun%2Fdocker.sock/_ping": 
dial unix /var/run/docker.sock: connect: permission denied
```

**Causa**: O usuário não tem permissões para acessar o Docker daemon.

**Solução rápida** (execute no terminal do Codespaces):
```bash
sudo usermod -aG docker $USER && newgrp docker
```

**Teste se funcionou**:
```bash
docker ps
```

**Se ainda não funcionar**:
1. Clique nos três pontos `...` no canto superior do Codespaces
2. Selecione **"Restart Codespace"**
3. Aguarde reiniciar e teste novamente: `docker ps`

**Solução alternativa**: use o script automático no diretório raiz do repositório:
```bash
chmod +x setup-docker-permissions.sh
bash setup-docker-permissions.sh
```

Se o erro persistir, reinicie o Codespace e teste novamente com `docker ps`.

---

### Problema: "Java not found"

**Solução**:
```bash
# No Codespaces
sudo apt-get update
sudo apt-get install -y default-jdk
java -version
```

Se você executou `./init-repo.sh`, essa verificação já foi feita pelo script.

### Problema: "ModuleNotFoundError: No module named 'pyspark'"

**Causa**: as dependências Python ainda não foram instaladas no Codespace.

**Solução**:
```bash
./init-repo.sh
```

Ou, dentro de `pyspark_app`:

```bash
python3 -m pip install -r requirements.txt
```

### Problema: `data/sales_data.csv` não encontrado

**Causa**: os dados sintéticos ainda não foram gerados ou foram apagados.

**Solução**:
```bash
cd pyspark_app
python3 data_generator.py
```

### Problema: `docker compose` não encontrado

**Solução**: verifique se o comando legado está disponível:

```bash
docker-compose --version
```

Se estiver, substitua `docker compose` por `docker-compose` nos comandos da Parte 5.

### Problema: "Out of Memory"

**Solução**:
```python
spark = SparkSession.builder \
    .appName("SalesAnalysis") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()
```

### Problema: "Permission Denied"

**Solução**:
```bash
chmod +x *.py
```

### Problema: Docker Build Falha

**Solução**:
```bash
# Limpe recursos não utilizados do Docker
docker system prune

# Rebuild sem cache
docker build --no-cache -t pyspark-app:v1.0 .
```

Use `docker system prune -a` apenas se o professor orientar, pois ele remove mais camadas e imagens do cache, deixando builds futuros mais lentos.

---

## Apêndice B: Comandos Úteis

### PySpark Shell Interativo

```bash
# Inicie o PySpark shell
pyspark

# Com configurações personalizadas
pyspark --master local[4] --driver-memory 2g
```

### Spark Submit

```bash
# Submeta uma aplicação
spark-submit \
  --master local[*] \
  --driver-memory 2g \
  --executor-memory 2g \
  spark_sales_analysis.py
```

### Monitoramento

```bash
# Spark UI (quando executando localmente)
# Acesse: http://localhost:4040
```

---

## Conclusão

Parabéns! Você completou o laboratório de PySpark. 

**O que você aprendeu**:
- ✅ Arquitetura e conceitos do Apache Spark
- ✅ Diferença entre RDDs e DataFrames
- ✅ Transformações e Ações
- ✅ Lazy Evaluation
- ✅ Análise de dados com PySpark
- ✅ Containerização de aplicações Spark
- ✅ Comparação com MapReduce

**Próximos passos**:
- Continue praticando com datasets reais
- Explore Spark Streaming e MLlib
- Considere certificações
- Contribua com projetos open source

---

