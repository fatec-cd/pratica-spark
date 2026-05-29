# Atividade Pratica: PySpark com Python

## Informacoes Gerais

**Publico-alvo:** Alunos de graduacao em Ciencia de Dados  
**Tematica:** Processamento de dados com Apache Spark e PySpark  
**Nivel:** Intermediario

---

## Objetivos de Aprendizagem

Ao final desta atividade, voce sera capaz de:

1. Compreender a arquitetura e os conceitos fundamentais do Apache Spark
2. Diferenciar RDDs, DataFrames, transformacoes e acoes
3. Executar scripts PySpark em um ambiente padronizado no GitHub Codespaces
4. Processar dados estruturados e nao estruturados usando PySpark
5. Aplicar operacoes de analise de dados em um caso de e-commerce
6. Interpretar resultados de negocio produzidos por consultas Spark
7. Comparar o paradigma Spark com MapReduce tradicional

---

## Pre-requisitos

- Conhecimento basico de Python
- Familiaridade com linha de comando
- Conceitos basicos de SQL, desejavel
- Conta no GitHub com acesso ao GitHub Codespaces
- Navegador web moderno

---

## Recursos Necessarios

Esta atividade deve ser executada no **GitHub Codespaces**. O objetivo e manter a turma em um ambiente padronizado e reduzir problemas causados por diferencas entre sistemas operacionais.

Voce usara:

- **GitHub Codespaces**: ambiente de desenvolvimento na nuvem
- **Python 3.11, Java 17 e PySpark 3.5.x**: execucao dos scripts de analise
- **Scripts do repositorio**: preparacao das dependencias e dos dados
- **Dataset sintetico**: dados de vendas de e-commerce

### Como usar este roteiro

Siga as partes na ordem. Cada checkpoint indica o que deve estar funcionando antes de avancar. Se um comando falhar, consulte primeiro o **Apendice A: Troubleshooting**.

Ao longo da execucao, sempre que aparecer um bloco **Evidencia**, faca a copia de tela naquele momento. Nao deixe para capturar tudo apenas no final, pois algumas saidas podem sair do historico do terminal ou ficar dificeis de localizar depois.

Ao longo da atividade, procure diferenciar tres camadas:

1. **Conceito**: o que Spark faz e por que faz dessa forma
2. **Implementacao**: como o conceito aparece nos scripts PySpark
3. **Interpretacao**: o que os resultados dizem sobre o problema de negocio

---

## Parte 1: Fundamentos do Apache Spark

### 1.1 O que e Apache Spark?

Apache Spark e um framework de processamento de dados distribuido de codigo aberto, projetado para ser rapido, escalavel e facil de usar. Foi desenvolvido na UC Berkeley em 2009 e se tornou um projeto Apache em 2013.

Principais caracteristicas:

- **Velocidade**: usa processamento em memoria e pode ser muito mais rapido que MapReduce em cargas iterativas
- **Facilidade de uso**: oferece APIs em Python, Scala, Java, R e SQL
- **Generalidade**: suporta batch, streaming, machine learning e processamento de grafos
- **Flexibilidade**: pode executar localmente ou em clusters gerenciados

### 1.2 Arquitetura do Spark

```text
SPARK APPLICATION
|
+-- DRIVER PROGRAM
|   +-- SparkSession / SparkContext
|   +-- Converte o programa em tarefas
|   +-- Agenda e monitora a execucao
|
+-- CLUSTER MANAGER
|   +-- Gerencia recursos disponiveis
|
+-- EXECUTORS
    +-- Executam tasks
    +-- Mantem dados em cache quando necessario
    +-- Enviam resultados ao driver
```

Componentes da arquitetura:

1. **Driver Program**
   - Executa a funcao principal da aplicacao
   - Cria a SparkSession ou o SparkContext
   - Converte o codigo em um DAG, ou grafo aciclico direcionado
   - Divide o trabalho em stages e tasks

2. **Cluster Manager**
   - Gerencia recursos para a aplicacao Spark
   - Pode ser Standalone, YARN, Mesos ou Kubernetes em ambientes de cluster

3. **Executors**
   - Processos que executam as tasks
   - Armazenam dados em cache ou memoria
   - Enviam resultados parciais ao driver

4. **Tasks**
   - Menor unidade de trabalho executada pelo Spark
   - Processam particoes dos dados

Nesta atividade, os scripts usam `local[*]`, ou seja, executam Spark no proprio Codespace usando os nucleos disponiveis no ambiente.

### 1.3 RDDs

RDD, ou Resilient Distributed Dataset, e uma colecao distribuida e imutavel de objetos.

Caracteristicas:

- **Resiliente**: pode ser reconstruido em caso de falha
- **Distribuido**: os dados podem ser particionados
- **Imutavel**: transformacoes criam novos RDDs

Exemplos:

```python
# A partir de uma colecao
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])

# A partir de arquivo
rdd = spark.sparkContext.textFile("data/input.txt")
```

### 1.4 DataFrames

DataFrames sao colecoes distribuidas organizadas em colunas nomeadas, semelhantes a tabelas SQL ou DataFrames do pandas.

Vantagens:

- Otimizacao automatica pelo Catalyst Optimizer
- Suporte a SQL
- Schema estruturado
- API de alto nivel

Exemplos:

```python
# A partir de arquivo CSV
df = spark.read.csv("data/sales_data.csv", header=True, inferSchema=True)

# A partir de dados em memoria
data = [(1, "Joao", 1000), (2, "Maria", 1500)]
df = spark.createDataFrame(data, ["id", "nome", "salario"])
```

### 1.5 Transformacoes vs acoes

**Transformacoes** criam novos RDDs ou DataFrames e sao avaliadas de forma preguicosa.

Exemplos:

- `map()`
- `filter()`
- `select()`
- `where()`
- `groupBy()`
- `join()`

**Acoes** disparam a execucao do plano construido pelo Spark.

Exemplos:

- `count()`
- `collect()`
- `first()`
- `show()`
- `write.csv()`

### 1.6 Lazy evaluation

Spark usa avaliacao preguicosa: transformacoes nao sao executadas imediatamente. Primeiro, Spark monta um plano. A execucao acontece quando uma acao e chamada.

Fluxo simplificado:

```text
Codigo -> DAG -> Logical Plan -> Physical Plan -> Execucao
```

Exemplo:

```python
# Nada e executado ainda
df_filtered = df.filter(df.price > 100)
df_selected = df_filtered.select("product_name", "price")

# A execucao acontece aqui
df_selected.count()
```

### 1.7 Spark vs MapReduce

| Caracteristica | MapReduce | Spark |
| --- | --- | --- |
| Velocidade | Mais lento em tarefas iterativas | Mais rapido por usar memoria e otimizacoes |
| Facilidade | API mais verbosa | APIs em Python, SQL e DataFrames |
| Processamento | Principalmente batch | Batch, streaming, ML e grafos |
| Iteracoes | Depende muito de I/O em disco | Pode reutilizar dados em memoria |
| Nivel da API | Baixo nivel | Alto nivel |

### Checkpoint 1.1

Antes de prosseguir, confirme:

- [ ] Voce compreende a diferenca entre driver e executor
- [ ] Voce entende o que sao RDDs e DataFrames
- [ ] Voce sabe diferenciar transformacoes e acoes
- [ ] Voce compreende o conceito de lazy evaluation
- [ ] Voce consegue comparar Spark com MapReduce

---

## Parte 2: Caso de Uso - Analise de Vendas de E-commerce

### 2.1 Contexto do problema

Uma empresa de e-commerce precisa analisar suas vendas para apoiar decisoes estrategicas.

Objetivos da analise:

1. Calcular receita total por categoria de produto
2. Identificar os produtos mais vendidos
3. Analisar padroes de vendas por regiao
4. Calcular metricas por cliente
5. Identificar tendencias temporais de vendas
6. Avaliar a performance dos produtos

Dataset principal: `sales_data.csv`

Estrutura dos dados:

```csv
transaction_id,date,customer_id,product_id,product_name,category,quantity,price,region
TX001,2024-01-15,C101,P501,Notebook,Electronics,1,2500.00,Southeast
TX002,2024-01-15,C102,P502,Mouse,Electronics,2,45.00,South
TX003,2024-01-16,C103,P503,Book,Books,3,35.00,Northeast
```

Campos:

- `transaction_id`: identificador unico da transacao
- `date`: data da venda
- `customer_id`: identificador do cliente
- `product_id`: identificador do produto
- `product_name`: nome do produto
- `category`: categoria do produto
- `quantity`: quantidade vendida
- `price`: preco unitario
- `region`: regiao da venda

### 2.2 Analises a realizar

1. **Receita por categoria**: calcula `quantity * price` e agrupa por categoria
2. **Top 10 produtos**: identifica produtos com maior quantidade vendida
3. **Vendas por regiao**: compara receita e volume por localidade
4. **Metricas de clientes**: calcula gastos, ticket medio e segmentacao
5. **Analise temporal**: observa tendencias ao longo do tempo
6. **Performance de produtos**: combina volume, receita e desempenho por item

### Checkpoint 2.1

Verifique:

- [ ] Voce compreende o contexto do problema de negocio
- [ ] Voce entende a estrutura dos dados
- [ ] Voce sabe quais perguntas serao respondidas pelas analises
- [ ] Voce consegue identificar colunas de dimensao e colunas de medida

---

## Parte 3: Configuracao do Ambiente

### 3.1 Criando o ambiente no GitHub Codespaces

**Passo 1:** acesse o GitHub e faca login.

**Passo 2:** faca um fork do repositorio do laboratorio.

1. Acesse o repositorio original fornecido pelo professor
2. Clique em **Fork**
3. Selecione sua conta como destino
4. Aguarde a criacao do fork

**Evidencia 1:** capture uma copia de tela mostrando seu fork do repositorio no GitHub.

**Passo 3:** abra seu fork no GitHub Codespaces.

1. No seu fork, clique em **Code**
2. Selecione a aba **Codespaces**
3. Clique em **Create codespace on main**
4. Aguarde o ambiente carregar

**Evidencia 2:** quando o Codespace abrir, capture uma copia de tela mostrando o editor com os arquivos do projeto.

### 3.2 Preparando dependencias e dados

No terminal do Codespaces, execute:

```bash
chmod +x init-repo.sh
./init-repo.sh
```

Esse script verifica Python e Java, instala as dependencias Python e gera os dados iniciais.

Criterio de sucesso: ao final, o terminal deve informar que o setup foi concluido e que os dados de exemplo foram gerados.

**Evidencia 3:** capture uma copia de tela do terminal mostrando o `./init-repo.sh` concluido com sucesso.

### 3.3 Verificando o ambiente

Execute:

```bash
python3 --version
java -version
python3 -m pip show pyspark
ls -la pyspark_app/
```

**Evidencia 4:** capture uma copia de tela mostrando a estrutura do projeto com `ls -la pyspark_app/`.

Voce deve encontrar estes arquivos principais:

- `data_generator.py`: gera os dados sinteticos
- `spark_word_count.py`: exemplo introdutorio com texto
- `spark_sales_analysis.py`: analise completa de vendas
- `spark_stream_example.py`: exemplo complementar de streaming
- `requirements.txt`: dependencias Python
- `data/`: diretorio de datasets e resultados

### Situacoes que podem prejudicar a execucao

| Situacao | Como prevenir ou corrigir |
| --- | --- |
| Dependencias Python ausentes | Execute `./init-repo.sh` na raiz do repositorio |
| Java ausente ou versao incompativel | Execute `./init-repo.sh` para instalar/configurar OpenJDK 17 |
| Dataset ausente | Execute `python3 data_generator.py` dentro de `pyspark_app` |
| Comando executado no diretorio errado | Entre em `pyspark_app` antes de rodar os scripts |
| Codespace parado ou expirado | Reabra o Codespace pelo GitHub; faca commits para preservar alteracoes |
| Memoria insuficiente | Reduza configuracoes de memoria nos scripts ou reinicie o Codespace |

### Checkpoint 3.1

Verifique:

- [ ] Fork do repositorio foi criado com sucesso
- [ ] Codespace foi aberto a partir do seu fork
- [ ] Python 3 esta instalado
- [ ] Java esta instalado
- [ ] PySpark esta instalado
- [ ] Dados de exemplo foram gerados
- [ ] Arquivos da aplicacao estao presentes

---

## Parte 4: Implementacao com PySpark

### 4.1 Explorando a estrutura do projeto

Entre no diretorio da aplicacao:

```bash
cd pyspark_app
ls -la
```

Estrutura esperada:

```text
pyspark_app/
|-- spark_sales_analysis.py    # Analise completa de vendas
|-- spark_word_count.py        # Exemplo basico
|-- data_generator.py          # Geracao de dados de teste
|-- spark_stream_example.py    # Exemplo complementar de streaming
|-- requirements.txt           # Dependencias Python
`-- data/                      # Datasets e resultados
```

### 4.2 Gerando e entendendo o dataset

Se voce executou `./init-repo.sh`, os dados ja foram criados. Para recriar os arquivos, execute:

```bash
python3 data_generator.py
```

Visualize as primeiras linhas:

```bash
head -20 data/sales_data.csv
```

**Evidencia 5:** capture uma copia de tela mostrando a geracao dos dados ou a saida de `head -20 data/sales_data.csv`.

Perguntas de observacao:

- Quais colunas representam dimensoes, como categoria e regiao?
- Quais colunas permitem calcular metricas, como quantidade, preco e receita?
- Cada linha representa qual evento de negocio?

### 4.3 Exemplo simples: Word Count com PySpark

Antes da analise de vendas, abra `spark_word_count.py` no editor do Codespaces. Use o Explorer lateral ou pressione `Ctrl+P`, digite `spark_word_count.py` e confirme com Enter.

Com o arquivo aberto no editor, localize:

- A funcao que cria a SparkSession
- A leitura de `data/input.txt`
- As tres abordagens de Word Count: RDD, DataFrame e SQL
- A chamada que exibe o plano de execucao

Depois, execute o exemplo no terminal:

```bash
python3 spark_word_count.py
```

O script demonstra:

1. Criacao de uma SparkSession
2. Leitura de arquivo de texto
3. Uso de RDDs, DataFrames e Spark SQL
4. Aplicacao de transformacoes
5. Execucao de acoes
6. Visualizacao do plano de execucao

Criterio de sucesso: o terminal deve exibir rankings de palavras e o plano de execucao do Spark.

**Evidencia 6:** capture uma copia de tela mostrando os resultados do Word Count.

**Evidencia 7:** capture outra copia de tela mostrando o plano de execucao exibido pelo script. Se a saida ficar longa, role o terminal ate a secao do plano antes de capturar.

### 4.4 Analise de vendas: leitura e exploracao

Abra `spark_sales_analysis.py` no editor do Codespaces. Use o Explorer lateral ou `Ctrl+P` para localizar o arquivo rapidamente.

Observe no codigo:

- Criacao da SparkSession
- Leitura do CSV com inferencia de schema
- Conversao da coluna `date`
- Criacao da coluna `revenue`
- Impressao do schema e das primeiras linhas

### 4.5 Analise de vendas: transformacoes e agregacoes

Exemplo de receita por categoria:

```python
df.groupBy("category") \
    .agg(sum("revenue").alias("total_revenue")) \
    .orderBy(desc("total_revenue"))
```

Exemplo de top produtos:

```python
df.groupBy("product_name") \
    .agg(sum("quantity").alias("total_sold")) \
    .orderBy(desc("total_sold")) \
    .limit(10)
```

Exemplo de vendas por regiao:

```python
df.groupBy("region") \
    .agg(
        count("*").alias("num_transactions"),
        sum("revenue").alias("total_revenue")
    )
```

Durante a leitura, tente marcar no codigo:

- Onde ha transformacoes
- Onde ha acoes
- Onde o resultado e persistido em `data/output/`
- Onde aparecem decisoes de negocio, como segmentacao de clientes

### 4.6 Executando a analise completa

Execute:

```bash
python3 spark_sales_analysis.py
```

Durante a execucao, acompanhe a saida no terminal e capture as evidencias assim que cada secao aparecer. Se alguma secao passar na tela, voce pode rolar o terminal ou executar novamente o script.

Observe a saida:

- Schema do DataFrame
- Estatisticas descritivas
- Receita por categoria
- Top produtos
- Vendas por regiao
- Metricas e segmentacao de clientes
- Tendencias temporais
- Resultados salvos em `data/output/`

**Evidencia 8:** capture a tela da secao que mostra o schema do DataFrame de vendas.

**Evidencia 9:** capture a tela da secao de receita por categoria.

**Evidencia 10:** capture a tela da secao de top produtos.

**Evidencia 11:** capture a tela da secao de vendas por regiao.

**Evidencia 12:** capture a tela da secao de metricas de clientes ou tendencias temporais.

Depois que a analise terminar, confirme os diretorios de saida:

```bash
ls -la data/output/
```

**Evidencia 13:** capture uma copia de tela mostrando os diretorios criados em `data/output/`.

### 4.7 Desafio opcional desejavel: criando uma nova analise

Esta etapa e opcional, mas altamente recomendada. Ate aqui voce executou e observou analises prontas. Agora voce deve modificar o codigo para responder a uma nova pergunta de negocio.

Pergunta do desafio:

> Qual e a receita total de cada categoria em cada regiao?

Objetivo esperado: ao executar `python3 spark_sales_analysis.py`, o terminal deve exibir uma nova secao chamada `ANALISE EXTRA: RECEITA POR REGIAO E CATEGORIA`, com as colunas `region`, `category`, `total_revenue`, `total_quantity` e `num_transactions`. O resultado tambem deve ser salvo em `data/output/revenue_by_region_category/`.

Para realizar o desafio:

1. Abra `spark_sales_analysis.py` no editor do Codespaces.
2. Crie uma nova funcao depois de `analysis_sales_by_region(df)`.
3. Use `groupBy("region", "category")` para agrupar os dados.
4. Calcule receita total, quantidade total e numero de transacoes.
5. Ordene por `region` e por maior receita dentro de cada regiao.
6. Salve o resultado em `data/output/revenue_by_region_category`.
7. Chame a nova funcao dentro de `main()`, depois da chamada de `analysis_sales_by_region(df)`.

**Evidencia opcional 14:** capture uma copia de tela do editor mostrando a nova funcao criada no codigo.

**Evidencia opcional 15:** capture uma copia de tela do terminal mostrando a nova secao `ANALISE EXTRA: RECEITA POR REGIAO E CATEGORIA`.

**Evidencia opcional 16:** capture uma copia de tela mostrando o diretorio `data/output/revenue_by_region_category/` criado apos a execucao.

Perguntas de reflexao:

- Quais analises usam apenas agregacao?
- Quais analises usam ordenacao ou limite?
- Onde uma janela temporal seria util?
- Por que `show()` dispara execucao?
- Quais resultados seriam mais importantes para uma decisao comercial?
- No desafio opcional, por que faz sentido agrupar por duas dimensoes ao mesmo tempo?

### Checkpoint 4.1

Verifique:

- [ ] Dados de vendas foram gerados
- [ ] Word Count executou com sucesso
- [ ] Analise de vendas executou completamente
- [ ] Resultados foram gravados em `data/output/`
- [ ] Voce identificou transformacoes e acoes nos scripts
- [ ] Voce consegue interpretar os resultados de negocio
- [ ] Opcional: voce criou e executou a analise extra por regiao e categoria

---

## Parte 5: Entregaveis da Atividade

### 5.1 O que deve ser entregue

Para comprovar a conclusao desta atividade pratica, entregue screenshots das execucoes na tarefa indicada pelo professor.

### 5.2 Lista de screenshots obrigatorios

Use a lista abaixo como checklist final. As copias de tela devem ter sido capturadas durante as etapas indicadas no roteiro.

1. **Fork do repositorio**: screenshot mostrando seu fork do repositorio no GitHub
2. **Codespaces em execucao**: screenshot do GitHub Codespaces aberto com os arquivos do projeto
3. **Estrutura do projeto**: screenshot do terminal mostrando `ls -la pyspark_app/`
4. **Setup concluido**: screenshot da execucao de `./init-repo.sh` concluida com sucesso
5. **Geracao ou verificacao dos dados**: screenshot de `head -20 data/sales_data.csv` ou da execucao de `data_generator.py`
6. **Execucao do Word Count**: screenshot da execucao de `spark_word_count.py` mostrando resultados
7. **Plano de execucao do Word Count**: screenshot mostrando a parte do plano de execucao exibida pelo script
8. **Analise de vendas: schema**: screenshot mostrando o schema do DataFrame de vendas
9. **Analise de vendas: receita por categoria**: screenshot mostrando os resultados da receita por categoria
10. **Analise de vendas: top produtos**: screenshot mostrando os produtos mais vendidos
11. **Analise de vendas: vendas por regiao**: screenshot mostrando a distribuicao de vendas por regiao
12. **Analise de vendas: metricas de clientes ou tendencias temporais**: screenshot mostrando uma dessas secoes da analise completa
13. **Resultados gerados**: screenshot mostrando os diretorios criados em `data/output/`

### 5.3 Evidencias opcionais desejaveis

Se voce realizou o desafio opcional da secao 4.7, inclua tambem:

14. **Codigo da analise extra**: screenshot do editor mostrando a funcao `analysis_revenue_by_region_category(df)` criada em `spark_sales_analysis.py`
15. **Execucao da analise extra**: screenshot do terminal mostrando a secao `ANALISE EXTRA: RECEITA POR REGIAO E CATEGORIA`
16. **Resultado da analise extra**: screenshot mostrando o diretorio `data/output/revenue_by_region_category/`

### 5.4 Orientacoes para os screenshots

Requisitos:

1. Screenshots devem estar legiveis
2. A saida relevante do comando deve estar visivel
3. Use formato PNG ou JPG
4. Nomeie arquivos de forma descritiva, por exemplo `01_fork_repositorio.png`

### 5.5 Checklist pre-entrega

Antes de submeter, verifique:

- [ ] Todos os 13 screenshots obrigatorios foram capturados
- [ ] Screenshots estao legiveis
- [ ] Scripts executaram sem erro
- [ ] Resultados foram gerados em `data/output/`
- [ ] Voce consegue explicar ao menos duas transformacoes e duas acoes usadas
- [ ] Voce consegue interpretar os principais resultados de negocio
- [ ] Se realizou o desafio opcional, incluiu as evidencias 14, 15 e 16

### 5.6 Duvidas frequentes

**P: Posso trabalhar localmente ao inves de usar Codespaces?**  
R: Para esta atividade, use Codespaces como ambiente padrao. A execucao local so deve ser usada se o professor autorizar.

**P: O que fazer se meu Codespace expirar?**  
R: Reabra ou recrie o Codespace a partir do seu fork. Faca commits para preservar alteracoes importantes.

**P: Preciso alterar os scripts?**  
R: Nao para concluir a atividade principal. A secao 4.7 traz um desafio opcional desejavel em que voce altera o codigo para criar uma nova analise.

**P: Preciso usar cluster Spark real?**  
R: Nao. Nesta atividade, Spark executa em modo local no Codespace para facilitar o foco nos conceitos.

---

## Parte 6: Recursos Adicionais e Proximos Passos

### 6.1 Conceitos avancados para estudo

1. Spark SQL
2. Spark Streaming
3. Spark MLlib
4. GraphX
5. Delta Lake
6. Otimizacao de particionamento e cache

### 6.2 Recursos de aprendizagem

Documentacao oficial:

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

Cursos online:

- [Databricks Academy](https://www.databricks.com/learn/training)
- [Coursera - Big Data Specialization](https://www.coursera.org/specializations/big-data)

Livros:

- "Learning Spark" (O'Reilly)
- "Spark: The Definitive Guide" (O'Reilly)
- "High Performance Spark" (O'Reilly)

Comunidade:

- [Stack Overflow - Apache Spark](https://stackoverflow.com/questions/tagged/apache-spark)
- [Spark User Mailing List](https://spark.apache.org/community.html)

### 6.3 Proximos passos

1. Reexecutar as analises com filtros diferentes
2. Criar novas metricas de cliente ou produto
3. Comparar execucoes com diferentes numeros de particoes
4. Explorar Spark SQL com views temporarias
5. Implementar uma analise propria usando o mesmo dataset

---

## Apendice A: Troubleshooting

### Problema: "Java not found"

Solucao:

```bash
sudo apt-get update
sudo apt-get install -y openjdk-17-jdk
java -version
```

Se voce executou `./init-repo.sh`, essa verificacao ja foi feita pelo script.

### Problema: `java.util.ServiceConfigurationError: org.apache.hadoop.fs.FileSystem: Provider org.apache.hadoop.fs.viewfs.ViewFileSystem could not be instantiated`

Causas provaveis:

- Java novo demais para a combinacao Spark/Hadoop usada no roteiro, especialmente Java 21 ou superior
- Codespace criado antes da configuracao padronizada do repositorio
- Instalacao de PySpark fora da linha 3.5.x esperada pelo laboratorio
- Uso de Python fora da faixa 3.8 a 3.11 em execucao local

Solucao recomendada no Codespaces:

```bash
./init-repo.sh
cd pyspark_app
python3 -m pip install --force-reinstall -r requirements.txt
python3 spark_word_count.py
```

Se o Codespace ainda estiver usando Java 21 ou superior, recrie o Codespace. O repositorio agora inclui uma configuracao `.devcontainer` com Python 3.11 e Java 17.

Para verificar:

```bash
java -version
python3 -m pip show pyspark
```

O Java deve ser 11 ou 17, preferencialmente 17, e o PySpark deve estar na linha 3.5.x.

Em execucao local fora do Codespaces, use Python 3.8 a 3.11. Python 3.12 pode fazer os workers do PySpark falharem durante as acoes do Spark.

### Problema: "ModuleNotFoundError: No module named 'pyspark'"

Causa provavel: as dependencias Python ainda nao foram instaladas.

Solucao na raiz do repositorio:

```bash
./init-repo.sh
```

Ou, dentro de `pyspark_app`:

```bash
python3 -m pip install -r requirements.txt
```

### Problema: `data/sales_data.csv` nao encontrado

Causa provavel: os dados sinteticos ainda nao foram gerados ou foram apagados.

Solucao:

```bash
cd pyspark_app
python3 data_generator.py
```

### Problema: comando executado no diretorio errado

Se o script nao encontrar arquivos dentro de `data/`, confirme o diretorio atual:

```bash
pwd
ls -la
```

Para executar os scripts, entre em:

```bash
cd pyspark_app
```

### Problema: "Out of Memory"

Solucao possivel: reduza configuracoes de memoria no script ou reinicie o Codespace. Para datasets pequenos desta atividade, o erro geralmente indica ambiente instavel ou configuracao alterada.

Exemplo de configuracao mais conservadora:

```python
spark = SparkSession.builder \
    .appName("SalesAnalysis") \
    .master("local[*]") \
    .config("spark.driver.memory", "1g") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

### Problema: "Permission denied" ao executar script

Solucao:

```bash
chmod +x *.py
```

Tambem e possivel executar explicitamente com Python:

```bash
python3 spark_sales_analysis.py
```

---

## Apendice B: Comandos Uteis

### Verificar ambiente

```bash
python3 --version
java -version
python3 -m pip show pyspark
```

### Recriar dados

```bash
cd pyspark_app
python3 data_generator.py
```

### Executar exemplos

```bash
cd pyspark_app
python3 spark_word_count.py
python3 spark_sales_analysis.py
```

### Executar com spark-submit

```bash
cd pyspark_app
spark-submit \
  --master local[*] \
  --driver-memory 2g \
  spark_sales_analysis.py
```

---

## Conclusao

Ao concluir o laboratorio, voce tera praticado:

- Arquitetura e conceitos do Apache Spark
- Diferenca entre RDDs e DataFrames
- Transformacoes, acoes e lazy evaluation
- Leitura e analise de dados com PySpark
- Agregacoes, ordenacoes, filtros e metricas de negocio
- Interpretacao de resultados em um caso de e-commerce
- Comparacao entre Spark e MapReduce

Continue praticando com novas perguntas sobre o dataset e tente implementar suas proprias analises.
