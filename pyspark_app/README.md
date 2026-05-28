# PySpark Big Data Application

Aplicacao de analise de dados usando Apache Spark e PySpark em um caso de vendas de e-commerce. O foco deste diretorio e demonstrar conceitos de Spark por meio de scripts Python executados diretamente no ambiente do GitHub Codespaces.

## Quick Start

### Pre-requisitos

- Python 3.8 a 3.11, preferencialmente Python 3.11 no Codespaces
- Java 11 ou 17, preferencialmente Java 17
- Dependencias instaladas a partir de `requirements.txt`

Na raiz do repositorio, o comando recomendado e:

```bash
./init-repo.sh
```

### Executar os exemplos

```bash
cd pyspark_app

# Gera os dados de exemplo
python3 data_generator.py

# Exemplo basico: Word Count
python3 spark_word_count.py

# Analise completa: Vendas
python3 spark_sales_analysis.py
```

## Estrutura do Projeto

```text
pyspark_app/
|-- spark_sales_analysis.py    # Analise completa de vendas de e-commerce
|-- spark_word_count.py        # Exemplo basico de word count
|-- spark_stream_example.py    # Exemplo complementar de streaming
|-- data_generator.py          # Gerador de dados sinteticos
|-- requirements.txt           # Dependencias Python
`-- data/                      # Datasets e resultados
    |-- sales_data.csv         # Dados de vendas gerados
    |-- products.csv           # Catalogo de produtos gerado
    |-- input.txt              # Texto para word count gerado
    `-- output/                # Resultados das analises
```

## Caso de Uso: Analise de Vendas de E-commerce

O script `spark_sales_analysis.py` simula uma rotina de Business Intelligence para uma empresa de e-commerce. Ele processa transacoes de vendas e produz resultados analiticos.

Analises implementadas:

1. **Receita por categoria**: identifica categorias mais lucrativas
2. **Top produtos**: lista produtos mais vendidos
3. **Vendas por regiao**: compara distribuicao geografica
4. **Metricas de clientes**: calcula ticket medio e segmentacao
5. **Tendencias temporais**: observa padroes ao longo do tempo
6. **Performance de produtos**: analisa receita e volume por item

## Dados Utilizados

Dataset principal: `data/sales_data.csv`

Schema esperado:

- `transaction_id`: ID unico da transacao
- `date`: data da venda
- `customer_id`: ID do cliente
- `product_id`: ID do produto
- `product_name`: nome do produto
- `category`: categoria
- `quantity`: quantidade vendida
- `price`: preco unitario
- `region`: regiao

## Conceitos PySpark Demonstrados

### Word Count

O arquivo `spark_word_count.py` demonstra:

- SparkSession
- RDDs
- DataFrames
- Spark SQL
- Transformacoes e acoes
- Lazy evaluation
- Plano de execucao

Execute:

```bash
python3 spark_word_count.py
```

### Analise de Vendas

O arquivo `spark_sales_analysis.py` demonstra:

- Leitura de CSV com inferencia de schema
- Criacao de colunas derivadas
- Agregacoes com `groupBy()` e `agg()`
- Ordenacao com `orderBy()`
- Uso de funcoes SQL
- Escrita de resultados em CSV

Execute:

```bash
python3 spark_sales_analysis.py
```

## Configuracao do Spark

Os scripts usam modo local:

```python
spark = SparkSession.builder \
    .appName("MyApp") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()
```

Isso permite estudar os conceitos do Spark sem configurar um cluster real.

## Resultados

Os resultados das analises sao salvos em:

- `data/output/revenue_by_category/`
- `data/output/top_products/`
- `data/output/sales_by_region/`
- `data/output/customer_metrics/`
- `data/output/monthly_trends/`
- `data/output/product_performance/`

## Exercicios Praticos

1. Identifique padroes de vendas por dia da semana
2. Liste os top 20 clientes que mais gastaram
3. Compare vendas mes a mes
4. Crie uma consulta SQL para receita por regiao e categoria
5. Compare tempos de execucao com diferentes configuracoes de particao

Exemplo:

```bash
spark-submit --conf spark.sql.shuffle.partitions=4 spark_sales_analysis.py
spark-submit --conf spark.sql.shuffle.partitions=8 spark_sales_analysis.py
spark-submit --conf spark.sql.shuffle.partitions=16 spark_sales_analysis.py
```

## Troubleshooting

### Java not found ou erro ViewFileSystem do Hadoop

```bash
sudo apt-get update
sudo apt-get install -y openjdk-17-jdk
java -version
```

Se aparecer `Provider org.apache.hadoop.fs.viewfs.ViewFileSystem could not be instantiated`, verifique se o ambiente esta usando Java 21 ou superior. Para este laboratorio, use Java 17 e reinstale as dependencias com:

```bash
python3 -m pip install --force-reinstall -r requirements.txt
```

Tambem confirme que o Python esta na faixa 3.8 a 3.11. Python 3.12 pode iniciar o Spark, mas falhar quando os workers do PySpark executam as acoes.

### PySpark nao encontrado

```bash
python3 -m pip install -r requirements.txt
```

### Dados nao encontrados

```bash
python3 data_generator.py
```

### Permissao negada

```bash
chmod +x *.py
```

Tambem e possivel executar os scripts com `python3 nome_do_script.py`.

## Recursos de Aprendizagem

- [Apache Spark](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
