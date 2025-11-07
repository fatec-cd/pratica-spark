# PySpark Big Data Application

Aplicação de análise de dados usando Apache Spark e PySpark, containerizada com Docker para análises de Big Data em e-commerce.

## 🚀 Quick Start

### Pré-requisitos
- Python 3.8+
- Apache Spark 3.5+ (para execução local)
- Docker 20.10+ (opcional, para containerização)
- Docker Compose 2.0+ (opcional, para orquestração)
- Java 11+ (necessário para Spark)

### Executar Localmente

```bash
# Navegue até o diretório da aplicação
cd pyspark_app

# Gere os dados de exemplo
python3 data_generator.py

# Execute a análise de vendas
python3 spark_sales_analysis.py

# Ou execute o exemplo de word count
python3 spark_word_count.py
```

### Executar com Docker

```bash
# Construa a imagem
docker build -t pyspark-app:v1.0 .

# Gere os dados
docker run --rm -v "$(pwd)/data:/app/data" pyspark-app:v1.0 python3 data_generator.py

# Execute análise de vendas
docker run --rm -v "$(pwd)/data:/app/data" pyspark-app:v1.0 python3 spark_sales_analysis.py
```

### Executar com Docker Compose

```bash
# Gerar dados
docker-compose --profile setup up data-generator

# Análise de vendas (perfil padrão)
docker-compose up sales-analysis

# Word count
docker-compose --profile examples up word-count

# PySpark Shell interativo
docker-compose --profile interactive up pyspark-shell
```

## 📊 Estrutura do Projeto

```
pyspark_app/
├── spark_sales_analysis.py    # Análise completa de vendas de e-commerce
├── spark_word_count.py         # Exemplo básico de word count
├── data_generator.py           # Gerador de dados sintéticos
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Configuração da imagem Docker
├── docker-compose.yml          # Orquestração de containers
├── .dockerignore               # Arquivos ignorados pelo Docker
└── data/                       # Datasets
    ├── sales_data.csv          # Dados de vendas (gerado)
    ├── products.csv            # Catálogo de produtos (gerado)
    ├── input.txt               # Texto para word count (gerado)
    └── output/                 # Resultados das análises
```

## 🎯 Caso de Uso: Análise de Vendas de E-commerce

### Contexto
Sistema de Business Intelligence para análise de vendas de uma empresa de e-commerce, processando transações para gerar insights de negócio.

### Análises Implementadas

1. **Receita por Categoria**: Identificação das categorias mais lucrativas
2. **Top Produtos**: Ranking dos produtos mais vendidos
3. **Vendas por Região**: Distribuição geográfica das vendas
4. **Métricas de Clientes**: Ticket médio e segmentação de clientes
5. **Tendências Temporais**: Padrões de vendas ao longo do tempo
6. **Performance de Produtos**: Análise detalhada por produto

### Dados Utilizados

**Dataset**: `sales_data.csv`

**Schema**:
- `transaction_id`: ID único da transação
- `date`: Data da venda
- `customer_id`: ID do cliente
- `product_id`: ID do produto
- `product_name`: Nome do produto
- `category`: Categoria (Electronics, Books, Stationery, Accessories)
- `quantity`: Quantidade vendida
- `price`: Preço unitário
- `region`: Região (Southeast, South, Northeast, North, Midwest)

## 🧪 Exemplos de Uso

### Word Count Básico

Demonstra conceitos fundamentais do Spark:
- RDDs (Resilient Distributed Datasets)
- DataFrames
- Spark SQL
- Transformações e Ações
- Lazy Evaluation

```bash
python3 spark_word_count.py
```

### Análise de Vendas Completa

Demonstra análises complexas de dados:
- Agregações múltiplas
- Joins e filtros
- Window functions
- SQL queries
- Cache e otimização

```bash
python3 spark_sales_analysis.py
```

## 📚 Conceitos PySpark Demonstrados

### Arquitetura Spark
- **Driver Program**: Coordena a execução
- **Cluster Manager**: Gerencia recursos
- **Executors**: Processam tarefas
- **Tasks**: Menor unidade de trabalho

### RDDs vs DataFrames
- **RDD**: Abstração de baixo nível, API funcional
- **DataFrame**: Alto nível, otimizações automáticas (Catalyst)

### Transformações (Lazy)
```python
df.filter(col("price") > 100)
df.groupBy("category").agg(sum("revenue"))
df.select("customer_id", "total_spent")
```

### Ações (Eager)
```python
df.count()
df.show()
df.collect()
df.write.csv("output.csv")
```

### Otimizações
- **Catalyst Optimizer**: Otimização de queries
- **Tungsten Engine**: Gerenciamento de memória
- **Adaptive Query Execution**: Ajustes dinâmicos

## 🔧 Configuração

### Configurações do Spark

```python
spark = SparkSession.builder \
    .appName("MyApp") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()
```

### Variáveis de Ambiente

```bash
export SPARK_HOME=/opt/spark
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYSPARK_PYTHON=python3
```

## 📈 Resultados

Os resultados das análises são salvos em:
- `data/output/revenue_by_category/`: Receita por categoria
- `data/output/top_products/`: Top produtos
- `data/output/sales_by_region/`: Vendas por região
- `data/output/customer_metrics/`: Métricas de clientes
- `data/output/monthly_trends/`: Tendências mensais
- `data/output/product_performance/`: Performance de produtos

## 🎓 Exercícios Práticos

### Exercício 1: Análise de Sazonalidade
Identifique padrões de vendas por dia da semana.

**Dica**: Use `dayofweek()` e `dayofmonth()`.

### Exercício 2: Clientes VIP
Liste os top 20 clientes que mais gastaram.

**Dica**: Use `groupBy()` + `agg()` + `orderBy()`.

### Exercício 3: Produtos Frequentemente Comprados Juntos
Análise de cesta de compras.

**Dica**: Use `self-join` em transactions do mesmo cliente.

### Exercício 4: Análise de Crescimento
Compare vendas mês a mês.

**Dica**: Use Window functions com `lag()`.

### Exercício 5: Otimização de Performance
Compare tempos de execução com diferentes configurações.

```bash
# Teste diferentes números de partições
spark-submit --conf spark.sql.shuffle.partitions=4 spark_sales_analysis.py
spark-submit --conf spark.sql.shuffle.partitions=8 spark_sales_analysis.py
spark-submit --conf spark.sql.shuffle.partitions=16 spark_sales_analysis.py
```

## 🆚 Comparação: MapReduce vs Spark

| Aspecto | MapReduce | Spark |
|---------|-----------|-------|
| **Velocidade** | Baseline | 10-100x mais rápido |
| **API** | Complexa (Java) | Simples (Python, SQL) |
| **Processamento** | Disco | Memória |
| **Iterações** | Lento | Rápido (cache) |
| **Casos de Uso** | Batch simples | Batch, Streaming, ML |
| **Curva de Aprendizado** | Íngreme | Suave |

## 🐛 Troubleshooting

### Java not found
```bash
# Instale OpenJDK 11
sudo apt-get install openjdk-11-jdk

# Configure JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Out of Memory
```python
# Aumente memória
spark = SparkSession.builder \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()
```

### Permission Denied
```bash
chmod +x *.py
```

### Data not found
```bash
# Gere os dados primeiro
python3 data_generator.py
```

## 📖 Recursos de Aprendizagem

### Documentação Oficial
- [Apache Spark](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

### Livros Recomendados
- "Learning Spark" (O'Reilly)
- "Spark: The Definitive Guide" (O'Reilly)
- "High Performance Spark" (O'Reilly)

### Cursos Online
- [Databricks Academy](https://www.databricks.com/learn)
- [Coursera - Big Data with Spark](https://www.coursera.org/)
- [edX - Spark Fundamentals](https://www.edx.org/)

## 🚀 Próximos Passos

1. **Spark Streaming**: Processamento em tempo real
2. **MLlib**: Machine Learning distribuído
3. **GraphX**: Análise de grafos
4. **Delta Lake**: ACID transactions
5. **Cloud Deployment**: AWS EMR, Azure Databricks, GCP Dataproc


