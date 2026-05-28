# PySparkContainer - Laboratório de Big Data

## 📚 Sobre o Projeto

Este repositório contém um roteiro prático completo para aprendizado de **Apache Spark** e **PySpark**, desenvolvido para estudantes de Ciência de Dados. É uma continuação natural do laboratório de MapReduce, oferecendo uma visão moderna de processamento de Big Data.

## 🎯 Objetivos Principais

- Compreender a arquitetura distribuída do Apache Spark
- Dominar conceitos de RDDs, DataFrames e Spark SQL
- Implementar análises de dados em larga escala
- Containerizar aplicações Spark com Docker
- Comparar paradigmas MapReduce vs Spark
- Aplicar conhecimentos em casos de uso reais

## 📁 Estrutura do Repositório

```
PySparkContainer/
├── README.md                          # Roteiro principal (teoria + prática)
├── ENTREGA_TEMPLATE.md               # Template para relatório do aluno
├── ORIENTACOES_PROFESSOR.md          # Guia de correção para o professor
├── COMPARACAO_MAPREDUCE_SPARK.md     # Análise comparativa detalhada
├── EXERCICIOS_EXTRAS.md              # 10 exercícios adicionais
├── PROJETO_OVERVIEW.md               # Este arquivo (visão geral)
├── LICENSE                           # Licença MIT
├── init-repo.sh                      # Script de setup (Linux/Mac)
├── init-repo.ps1                     # Script de setup (Windows)
├── .gitignore                        # Arquivos ignorados pelo Git
├── .devcontainer/                    # Configuração GitHub Codespaces
│   └── devcontainer.json
├── evidencias/                       # Pasta para screenshots dos alunos
│   └── README.md                     # Instruções sobre evidências
└── pyspark_app/                      # Aplicação PySpark
    ├── README.md                     # Documentação da aplicação
    ├── requirements.txt              # Dependências Python
    ├── Dockerfile                    # Imagem Docker
    ├── docker-compose.yml            # Orquestração
    ├── .dockerignore                 # Arquivos ignorados pelo Docker
    ├── data_generator.py             # Gerador de dados sintéticos
    ├── spark_word_count.py           # Exemplo básico (RDD + DataFrame)
    ├── spark_sales_analysis.py       # Análise completa de vendas
    ├── spark_stream_example.py       # Exemplo de streaming
    └── data/                         # Datasets
        ├── .gitkeep
        ├── sales_data.csv            # Dados de vendas (gerado)
        ├── products.csv              # Catálogo (gerado)
        ├── input.txt                 # Texto para word count (gerado)
        └── output/                   # Resultados das análises
```

## 🚀 Quick Start

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/PySparkContainer.git
cd PySparkContainer
```

### 2. Execute o Setup (GitHub Codespaces recomendado)

**Linux/Mac:**
```bash
chmod +x init-repo.sh
./init-repo.sh
```

**Windows (PowerShell):**
```powershell
.\init-repo.ps1
```

### 3. Execute os Exemplos

```bash
cd pyspark_app

# Gera dados (se ainda não executou o setup)
python3 data_generator.py

# Exemplo básico: Word Count
python3 spark_word_count.py

# Análise completa: Vendas
python3 spark_sales_analysis.py
```

### 4. Docker (Opcional)

```bash
# Build da imagem
docker build -t pyspark-app:v1.0 .

# Execução
docker compose up sales-analysis
```

## 📖 Conteúdo do Roteiro

### Parte 1: Fundamentos do Apache Spark
- Arquitetura (Driver, Executors, Cluster Manager)
- RDDs vs DataFrames
- Transformações e Ações
- Lazy Evaluation
- Comparação com MapReduce

### Parte 2: Caso de Uso - E-commerce
- Contexto: Análise de vendas online
- Dataset: Transações com múltiplas dimensões
- 6 análises implementadas:
  1. Receita por categoria
  2. Top 10 produtos
  3. Vendas por região
  4. Métricas de clientes
  5. Tendências temporais
  6. Performance de produtos

### Parte 3: Configuração do Ambiente
- GitHub Codespaces
- Instalação de dependências
- Configuração do Spark

### Parte 4: Implementação com PySpark
- Scripts Python comentados
- Geração de dados
- Análise de vendas completa
- Métricas e resultados

### Parte 5: Containerização com Docker
- Dockerfile otimizado
- Docker Compose
- Execução em container
- Volumes e persistência

### Parte 6: Entregáveis da Atividade
- Template de relatório (ENTREGA.md)
- 13 screenshots obrigatórios
- Critérios de avaliação
- Checklist de conclusão
- Orientações de entrega

### Parte 7: Recursos Adicionais
- Conceitos avançados para estudo
- Links para documentação
- Próximos passos
- Certificações

### Parte 8: Checklist Final
- Verificação de código
- Verificação de Docker
- Verificação de documentação
- Orientações para entrega

## 🎓 Caso de Uso: Análise de Vendas

### Dataset: `sales_data.csv`

**Campos:**
- `transaction_id`: ID único
- `date`: Data da venda
- `customer_id`: ID do cliente
- `product_id`: ID do produto
- `product_name`: Nome do produto
- `category`: Categoria (Electronics, Books, etc.)
- `quantity`: Quantidade
- `price`: Preço unitário
- `region`: Região brasileira

**Análises:**
- Receita total por categoria
- Produtos mais vendidos
- Distribuição geográfica
- Segmentação de clientes (VIP, Premium, Regular)
- Padrões temporais (mensal, semanal)

## 🆚 Comparação com MapReduce

| Aspecto | MapReduce | Spark |
|---------|-----------|-------|
| **Velocidade** | Baseline | 10-100x |
| **Código** | ~40 linhas | ~15 linhas |
| **APIs** | Baixo nível | Alto nível |
| **Use Cases** | Batch | Batch + Streaming + ML |
| **Curva de Aprendizado** | Íngreme | Moderada |

**Recomendação:** Use Spark para novos projetos!

## 💡 Conceitos PySpark Demonstrados

### Básicos
- ✅ SparkSession e SparkContext
- ✅ RDDs (Resilient Distributed Datasets)
- ✅ DataFrames e SQL
- ✅ Transformações (map, filter, groupBy)
- ✅ Ações (count, collect, show)

### Intermediários
- ✅ Agregações complexas (sum, avg, count)
- ✅ Window functions
- ✅ Joins e unions
- ✅ Cache e persist
- ✅ Particionamento

### Avançados
- ✅ Catalyst Optimizer
- ✅ Lazy Evaluation
- ✅ DAG (Directed Acyclic Graph)
- ✅ Physical Plans
- ✅ Adaptive Query Execution

## 🐳 Docker

### Imagens Disponíveis

- **Base**: `apache/spark-py:v3.5.0`
- **Custom**: Adiciona scripts e dependências

### Serviços Docker Compose

```yaml
services:
  data-generator    # Gera dados sintéticos
  word-count        # Exemplo básico
  sales-analysis    # Análise completa (padrão)
  pyspark-shell     # Shell interativo
  jupyter           # Jupyter Notebook (opcional)
```

### Comandos Úteis

```bash
# Build
docker compose build

# Executar análise
docker compose up sales-analysis

# Shell interativo
docker compose --profile interactive up pyspark-shell

# Jupyter Notebook
docker compose --profile jupyter up jupyter
```

## 📊 Resultados

Após executar as análises, encontre os resultados em:

```
pyspark_app/data/output/
├── revenue_by_category/
├── top_products/
├── sales_by_region/
├── customer_metrics/
├── monthly_trends/
└── product_performance/
```

## 🎯 Exercícios Extras

10 exercícios adicionais disponíveis em `EXERCICIOS_EXTRAS.md`:

1. **Cohort Analysis** - Análise de retenção
2. **Anomaly Detection** - Detecção de outliers
3. **RFM Analysis** - Segmentação de clientes
4. **Market Basket** - Análise de associação
5. **Time Series** - Séries temporais
6. **Geospatial** - Análise geográfica
7. **CLV** - Customer Lifetime Value
8. **Performance** - Otimização de queries
9. **Join Optimization** - Tipos de join
10. **Data Quality** - Validação de dados

## 📚 Recursos de Aprendizado

### Documentação Oficial
- [Apache Spark Docs](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

### Livros Recomendados
- "Learning Spark" (O'Reilly)
- "Spark: The Definitive Guide" (O'Reilly)
- "High Performance Spark" (O'Reilly)

### Cursos Online
- [Databricks Academy](https://www.databricks.com/learn)
- [Coursera - Big Data Specialization](https://www.coursera.org/)
- [edX - Spark Fundamentals](https://www.edx.org/)

### Certificações
- Databricks Certified Associate Developer
- Cloudera Spark and Hadoop Developer

## 🚀 Próximos Passos

Após completar este laboratório:

1. **Spark Streaming** - Processamento em tempo real
2. **MLlib** - Machine Learning distribuído
3. **GraphX** - Análise de grafos
4. **Delta Lake** - ACID transactions
5. **Cloud Deployment** - AWS EMR, Azure Databricks, GCP Dataproc

## 🤝 Contribuindo

Este é um projeto educacional. Contribuições são bem-vindas:

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-analise`
3. Commit: `git commit -m 'Adiciona nova análise'`
4. Push: `git push origin feature/nova-analise`
5. Abra um Pull Request

## 📝 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

Livre para uso educacional e comercial.

## 👨‍🏫 Créditos

**Desenvolvido para:**
- FATEC - Faculdade de Tecnologia
- Curso: Ciência de Dados
- Disciplina: Infraestrutura para Ciência de Dados

**Versão:** 1.0  
**Data:** Novembro 2025  
**Autor:** Professor/Instrutor

## 🐛 Troubleshooting

### Java não encontrado
```bash
sudo apt-get install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Out of Memory
```python
spark = SparkSession.builder \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()
```

### Arquivos não encontrados
```bash
python3 data_generator.py
```

### Permission Denied
```bash
chmod +x *.py *.sh
```

## 📧 Suporte

- **Issues**: Use o GitHub Issues
- **Discussões**: GitHub Discussions
- **Email**: professor@fatec.edu

## ⭐ Reconhecimentos

Agradecimentos especiais a:
- Apache Spark Community
- Databricks por recursos educacionais
- Alunos que contribuíram com feedback

---

## 📈 Estatísticas do Projeto

- **Linhas de código:** ~2.000+
- **Scripts Python:** 4 principais
- **Exercícios:** 10 extras
- **Tempo estimado:** 8-10 horas
- **Nível:** Intermediário

---

**🎓 Bons estudos e bom aprendizado com PySpark!**

Se este repositório foi útil, considere dar uma ⭐!

---

**Links Rápidos:**
- [📖 Roteiro Principal](README.md)
- [🆚 Comparação MapReduce vs Spark](COMPARACAO_MAPREDUCE_SPARK.md)
- [💪 Exercícios Extras](EXERCICIOS_EXTRAS.md)
- [📦 Aplicação PySpark](pyspark_app/README.md)
