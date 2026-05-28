# Laboratorio de PySpark para Ciencia de Dados

## Sobre o Projeto

Este repositorio contem um roteiro pratico para aprendizado de **Apache Spark** e **PySpark**, desenvolvido para estudantes de Ciencia de Dados. O foco da atividade e compreender conceitos de processamento distribuido e aplica-los em analises de dados com Python.

O ambiente recomendado e o **GitHub Codespaces**, para que a turma use uma configuracao padronizada sem depender de instalacoes locais.

## Objetivos Principais

- Compreender a arquitetura do Apache Spark
- Diferenciar RDDs, DataFrames, transformacoes e acoes
- Executar exemplos PySpark em modo local no Codespaces
- Implementar analises de dados em um caso de e-commerce
- Interpretar resultados de negocio produzidos pelos scripts
- Comparar Spark com MapReduce

## Estrutura do Repositorio

```text
pratica-spark/
|-- README.md                    # Roteiro principal da atividade
|-- PROJETO_OVERVIEW.md          # Visao geral do projeto
|-- init-repo.sh                 # Setup para Codespaces/Linux
|-- init-repo.ps1                # Setup PowerShell
`-- pyspark_app/                 # Aplicacao PySpark
    |-- README.md                # Documentacao da aplicacao
    |-- requirements.txt         # Dependencias Python
    |-- data_generator.py        # Gerador de dados sinteticos
    |-- spark_word_count.py      # Exemplo basico com texto
    |-- spark_sales_analysis.py  # Analise completa de vendas
    |-- spark_stream_example.py  # Exemplo complementar de streaming
    `-- data/                    # Datasets e resultados
```

## Quick Start

### 1. Abra no GitHub Codespaces

Faca fork do repositorio, abra a aba **Code**, selecione **Codespaces** e crie um novo Codespace.

### 2. Execute o setup

```bash
chmod +x init-repo.sh
./init-repo.sh
```

### 3. Execute os exemplos

```bash
cd pyspark_app
python3 spark_word_count.py
python3 spark_sales_analysis.py
```

## Conteudo do Roteiro

### Parte 1: Fundamentos do Apache Spark

- Arquitetura: driver, executors, cluster manager e tasks
- RDDs e DataFrames
- Transformacoes e acoes
- Lazy evaluation
- Comparacao com MapReduce

### Parte 2: Caso de Uso - E-commerce

- Contexto de negocio
- Dataset de vendas
- Perguntas analiticas
- Relacao entre colunas, metricas e resultados

### Parte 3: Configuracao do Ambiente

- GitHub Codespaces
- Instalacao de dependencias Python
- Verificacao de Java e PySpark
- Geracao dos dados sinteticos

### Parte 4: Implementacao com PySpark

- Word Count com RDDs, DataFrames e SQL
- Analise de vendas com agregacoes e filtros
- Interpretacao dos resultados gerados
- Escrita de resultados em `data/output/`

### Parte 5: Entregaveis

- Screenshots obrigatorios
- Evidencias da execucao dos scripts
- Checklist pre-entrega

### Parte 6: Recursos Adicionais

- Documentacao oficial
- Proximos conceitos para estudo
- Ideias de extensao da analise

## Caso de Uso: Analise de Vendas

Dataset principal: `pyspark_app/data/sales_data.csv`

Campos principais:

- `transaction_id`: identificador da transacao
- `date`: data da venda
- `customer_id`: identificador do cliente
- `product_id`: identificador do produto
- `product_name`: nome do produto
- `category`: categoria
- `quantity`: quantidade vendida
- `price`: preco unitario
- `region`: regiao

Analises implementadas:

- Receita total por categoria
- Produtos mais vendidos
- Distribuicao de vendas por regiao
- Metricas e segmentacao de clientes
- Tendencias temporais
- Performance de produtos

## Resultados

Apos executar a analise de vendas, os resultados sao gravados em:

```text
pyspark_app/data/output/
|-- revenue_by_category/
|-- top_products/
|-- sales_by_region/
|-- customer_metrics/
|-- monthly_trends/
`-- product_performance/
```

## Exercicios Extras

Ideias de extensao para os alunos:

1. Criar uma analise por dia da semana
2. Identificar clientes com maior ticket medio
3. Comparar receita por categoria e regiao
4. Criar uma consulta SQL sobre o DataFrame de vendas
5. Testar diferentes valores de `spark.sql.shuffle.partitions`

## Recursos de Aprendizagem

- [Apache Spark Docs](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Databricks Academy](https://www.databricks.com/learn)

## Licenca

MIT License. Veja [LICENSE](LICENSE) para detalhes.
