#!/usr/bin/env python3
"""
Exemplo de Spark Streaming (Estruturado)
Demonstra processamento de dados em tempo real
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, window, count, sum, avg, explode, split, from_json
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import time

def create_spark_session():
    """Cria SparkSession com suporte a streaming"""
    return SparkSession.builder \
        .appName("SparkStreamingExample") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

def streaming_word_count_example(spark):
    """
    Exemplo básico de streaming: Word Count em tempo real
    Monitora um diretório por novos arquivos de texto
    """
    print("\n" + "="*60)
    print("📡 STREAMING EXAMPLE: Real-Time Word Count")
    print("="*60)
    
    # Define schema para os dados de entrada
    # Neste exemplo, lemos arquivos de texto linha por linha
    
    # Cria streaming DataFrame que monitora um diretório
    lines_stream = spark.readStream \
        .format("text") \
        .option("maxFilesPerTrigger", 1) \
        .load("data/streaming_input/")
    
    # Transformações (lazy, como sempre)
    words = lines_stream.select(
        explode(split(col("value"), " ")).alias("word")
    )
    
    word_counts = words.groupBy("word").count()
    
    # Inicia a query de streaming
    # Output para console
    query = word_counts.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    print("\n📊 Aguardando dados... (Adicione arquivos em data/streaming_input/)")
    print("   Pressione Ctrl+C para parar")
    
    # Aguarda término (ou interrupção)
    try:
        query.awaitTermination(timeout=30)  # 30 segundos para demo
    except KeyboardInterrupt:
        query.stop()
        print("\n⏹️  Streaming interrompido")

def streaming_sales_aggregation(spark):
    """
    Exemplo avançado: Agregação de vendas em janelas de tempo
    Simula análise de vendas em tempo real
    """
    print("\n" + "="*60)
    print("📡 STREAMING EXAMPLE: Real-Time Sales Aggregation")
    print("="*60)
    
    # Define schema para dados de vendas
    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("category", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("region", StringType(), True)
    ])
    
    # Lê stream de arquivos CSV
    sales_stream = spark.readStream \
        .schema(schema) \
        .option("header", True) \
        .csv("data/streaming_sales/")
    
    # Adiciona coluna de receita
    sales_with_revenue = sales_stream.withColumn(
        "revenue",
        col("price") * col("quantity")
    )
    
    # Agregação por janela de tempo (windowed aggregation)
    # Agrupa vendas em janelas de 10 segundos
    windowed_sales = sales_with_revenue \
        .groupBy(
            window(col("timestamp").cast("timestamp"), "10 seconds"),
            col("category")
        ) \
        .agg(
            count("*").alias("num_sales"),
            sum("revenue").alias("total_revenue"),
            avg("revenue").alias("avg_revenue")
        )
    
    # Escreve resultados
    query = windowed_sales.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    print("\n📊 Processando vendas em tempo real...")
    print("   Janelas de 10 segundos")
    
    try:
        query.awaitTermination(timeout=60)
    except KeyboardInterrupt:
        query.stop()
        print("\n⏹️  Streaming interrompido")

def batch_vs_streaming_comparison():
    """
    Demonstra a diferença entre processamento batch e streaming
    """
    print("\n" + "="*60)
    print("📚 BATCH vs STREAMING: Comparação")
    print("="*60)
    
    comparison = """
    ╔════════════════════════════════════════════════════════════╗
    ║              BATCH vs STREAMING PROCESSING                 ║
    ╠════════════════════════════════════════════════════════════╣
    ║                                                            ║
    ║  BATCH PROCESSING (Tradicional)                           ║
    ║  • Processa dados históricos completos                    ║
    ║  • Execução periódica (hourly, daily)                     ║
    ║  • Alta latência (minutos/horas)                          ║
    ║  • Exemplo: Relatórios diários de vendas                  ║
    ║                                                            ║
    ║  STREAMING PROCESSING (Tempo Real)                        ║
    ║  • Processa dados conforme chegam                         ║
    ║  • Execução contínua (near real-time)                     ║
    ║  • Baixa latência (segundos/milissegundos)                ║
    ║  • Exemplo: Detecção de fraude em tempo real              ║
    ║                                                            ║
    ║  SPARK STRUCTURED STREAMING                                ║
    ║  • Mesma API que batch (DataFrames)                       ║
    ║  • Processamento incremental                              ║
    ║  • Suporte a event-time e watermarking                    ║
    ║  • Exactly-once semantics                                 ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    
    print(comparison)
    
    print("\n📊 Casos de Uso Comuns:")
    print("\n   BATCH:")
    print("     • ETL de data warehouses")
    print("     • Relatórios analíticos")
    print("     • Machine Learning training")
    print("     • Agregações históricas")
    
    print("\n   STREAMING:")
    print("     • Monitoramento de sistemas")
    print("     • Detecção de anomalias")
    print("     • Recomendações em tempo real")
    print("     • Processamento de logs/eventos")
    print("     • IoT e sensores")

def create_sample_streaming_data():
    """Cria dados de exemplo para demonstração de streaming"""
    import os
    
    # Cria diretório
    os.makedirs("data/streaming_input", exist_ok=True)
    
    # Arquivo de exemplo
    sample_text = """
    Apache Spark Streaming example
    Real time data processing with PySpark
    Structured Streaming API demonstration
    """
    
    with open("data/streaming_input/sample.txt", "w") as f:
        f.write(sample_text)
    
    print("✅ Dados de exemplo criados em data/streaming_input/")

def main():
    """Função principal"""
    print("=" * 60)
    print("  SPARK STREAMING - EXEMPLOS E CONCEITOS")
    print("=" * 60)
    
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    print(f"\n⚙️  Spark Version: {spark.version}")
    
    # Mostra comparação conceitual
    batch_vs_streaming_comparison()
    
    print("\n" + "="*60)
    print("📝 NOTA SOBRE STREAMING")
    print("="*60)
    print("""
Este exemplo demonstra CONCEITOS de Spark Streaming.

Para executar streaming real, você precisaria:

1. Fonte de dados em streaming (Kafka, socket, files)
2. Ambiente com recursos suficientes para processamento continuo
3. Caso de uso específico em tempo real

O Spark Structured Streaming utiliza a MESMA API dos DataFrames,
mas com processamento incremental contínuo.

Principais diferenças na API:
  • spark.readStream vs spark.read
  • df.writeStream vs df.write
  • Agregações com window()
  • Output modes: complete, append, update

Para este laboratório, focamos em BATCH PROCESSING, que é
mais adequado para ambiente de aprendizado e análises históricas.
    """)
    
    print("\n📚 Recursos para aprender mais sobre Streaming:")
    print("   • https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html")
    print("   • https://www.databricks.com/glossary/structured-streaming")
    
    spark.stop()
    print("\n🔚 SparkSession encerrada.")

if __name__ == "__main__":
    main()
