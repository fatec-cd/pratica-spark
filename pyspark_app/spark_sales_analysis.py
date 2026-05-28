#!/usr/bin/env python3
"""
Análise de Vendas de E-commerce com PySpark
Demonstra análises complexas usando DataFrames e SQL
"""

from pyspark.sql.functions import (
    col, sum, count, avg, max, min, round, desc, asc,
    year, month, dayofweek, date_format, to_date, expr
)
from pyspark.sql.window import Window
import time

from spark_environment import local_spark_builder

def create_spark_session():
    """Cria e configura SparkSession com configurações otimizadas"""
    return local_spark_builder(
        app_name="SalesAnalysis-PySpark",
        driver_memory="2g",
        executor_memory="2g",
        shuffle_partitions="8",
    ).config("spark.sql.adaptive.enabled", "true").getOrCreate()

def load_data(spark, file_path):
    """
    Carrega dados de vendas do CSV
    Infere schema automaticamente e valida dados
    """
    print("\n📂 Carregando dados...")
    
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(file_path)
    
    # Converte coluna date para tipo date
    df = df.withColumn("date", to_date(col("date")))
    
    # Adiciona coluna de receita
    df = df.withColumn("revenue", col("quantity") * col("price"))
    
    print(f"✅ {df.count()} transações carregadas com sucesso!")
    
    return df

def explore_data(df):
    """Exploração inicial dos dados"""
    print("\n" + "="*60)
    print("📊 EXPLORAÇÃO INICIAL DOS DADOS")
    print("="*60)
    
    # Schema
    print("\n📋 Schema do DataFrame:")
    df.printSchema()
    
    # Primeiras linhas
    print("\n📄 Primeiras 10 linhas:")
    df.show(10, truncate=False)
    
    # Estatísticas descritivas
    print("\n📈 Estatísticas Descritivas:")
    df.select("quantity", "price", "revenue").describe().show()
    
    # Contagem de valores únicos
    print("\n🔢 Valores Únicos:")
    print(f"   • Clientes: {df.select('customer_id').distinct().count()}")
    print(f"   • Produtos: {df.select('product_id').distinct().count()}")
    print(f"   • Categorias: {df.select('category').distinct().count()}")
    print(f"   • Regiões: {df.select('region').distinct().count()}")

def analysis_revenue_by_category(df):
    """
    Análise 1: Receita Total por Categoria
    Identifica as categorias mais lucrativas
    """
    print("\n" + "="*60)
    print("💰 ANÁLISE 1: RECEITA POR CATEGORIA")
    print("="*60)
    
    result = df.groupBy("category") \
        .agg(
            sum("revenue").alias("total_revenue"),
            count("*").alias("num_transactions"),
            avg("revenue").alias("avg_revenue"),
            sum("quantity").alias("total_quantity")
        ) \
        .withColumn("total_revenue", round(col("total_revenue"), 2)) \
        .withColumn("avg_revenue", round(col("avg_revenue"), 2)) \
        .orderBy(desc("total_revenue"))
    
    print("\n📊 Receita por Categoria:")
    result.show(truncate=False)
    
    # Salva resultado
    result.write.mode("overwrite").csv("data/output/revenue_by_category", header=True)
    print("💾 Resultado salvo em: data/output/revenue_by_category")
    
    return result

def analysis_top_products(df):
    """
    Análise 2: Top 10 Produtos Mais Vendidos
    Identifica os produtos mais populares
    """
    print("\n" + "="*60)
    print("🏆 ANÁLISE 2: TOP 10 PRODUTOS MAIS VENDIDOS")
    print("="*60)
    
    result = df.groupBy("product_id", "product_name", "category") \
        .agg(
            sum("quantity").alias("total_sold"),
            sum("revenue").alias("total_revenue"),
            count("*").alias("num_transactions")
        ) \
        .withColumn("total_revenue", round(col("total_revenue"), 2)) \
        .orderBy(desc("total_sold")) \
        .limit(10)
    
    print("\n🥇 Top 10 Produtos:")
    result.show(truncate=False)
    
    result.write.mode("overwrite").csv("data/output/top_products", header=True)
    print("💾 Resultado salvo em: data/output/top_products")
    
    return result

def analysis_sales_by_region(df):
    """
    Análise 3: Vendas por Região
    Analisa a distribuição geográfica das vendas
    """
    print("\n" + "="*60)
    print("🗺️  ANÁLISE 3: VENDAS POR REGIÃO")
    print("="*60)
    
    result = df.groupBy("region") \
        .agg(
            count("*").alias("num_transactions"),
            sum("revenue").alias("total_revenue"),
            avg("revenue").alias("avg_transaction_value"),
            sum("quantity").alias("total_items_sold")
        ) \
        .withColumn("total_revenue", round(col("total_revenue"), 2)) \
        .withColumn("avg_transaction_value", round(col("avg_transaction_value"), 2)) \
        .orderBy(desc("total_revenue"))
    
    print("\n📍 Vendas por Região:")
    result.show(truncate=False)
    
    # Calcula participação percentual
    total_revenue = df.select(sum("revenue")).first()[0]
    
    result_with_percentage = result.withColumn(
        "percentage",
        round((col("total_revenue") / total_revenue) * 100, 2)
    )
    
    print("\n📊 Participação Percentual:")
    result_with_percentage.select("region", "total_revenue", "percentage").show()
    
    result.write.mode("overwrite").csv("data/output/sales_by_region", header=True)
    print("💾 Resultado salvo em: data/output/sales_by_region")
    
    return result

def analysis_customer_metrics(df):
    """
    Análise 4: Métricas por Cliente
    Calcula ticket médio e identifica clientes VIP
    """
    print("\n" + "="*60)
    print("👥 ANÁLISE 4: MÉTRICAS POR CLIENTE")
    print("="*60)
    
    # Agregação por cliente
    customer_metrics = df.groupBy("customer_id") \
        .agg(
            count("*").alias("num_purchases"),
            sum("revenue").alias("total_spent"),
            avg("revenue").alias("avg_ticket"),
            max("date").alias("last_purchase")
        ) \
        .withColumn("total_spent", round(col("total_spent"), 2)) \
        .withColumn("avg_ticket", round(col("avg_ticket"), 2))
    
    # Top 20 clientes
    top_customers = customer_metrics \
        .orderBy(desc("total_spent")) \
        .limit(20)
    
    print("\n💎 Top 20 Clientes (por valor total):")
    top_customers.show(truncate=False)
    
    # Estatísticas gerais
    print("\n📊 Estatísticas Gerais de Clientes:")
    customer_metrics.select("num_purchases", "total_spent", "avg_ticket") \
        .describe().show()
    
    # Segmentação de clientes
    print("\n🎯 Segmentação de Clientes:")
    segments = customer_metrics.groupBy(
        expr("CASE WHEN total_spent >= 5000 THEN 'VIP' " +
             "WHEN total_spent >= 2000 THEN 'Premium' " +
             "WHEN total_spent >= 500 THEN 'Regular' " +
             "ELSE 'Basic' END").alias("segment")
    ).agg(
        count("*").alias("num_customers"),
        round(avg("total_spent"), 2).alias("avg_spent")
    ).orderBy(desc("avg_spent"))
    
    segments.show()
    
    customer_metrics.write.mode("overwrite").csv("data/output/customer_metrics", header=True)
    print("💾 Resultado salvo em: data/output/customer_metrics")
    
    return customer_metrics

def analysis_temporal_trends(df):
    """
    Análise 5: Tendências Temporais
    Analisa padrões de vendas ao longo do tempo
    """
    print("\n" + "="*60)
    print("📅 ANÁLISE 5: TENDÊNCIAS TEMPORAIS")
    print("="*60)
    
    # Adiciona colunas temporais
    df_with_time = df.withColumn("year", year("date")) \
        .withColumn("month", month("date")) \
        .withColumn("day_of_week", dayofweek("date"))
    
    # Vendas por mês
    print("\n📆 Vendas por Mês:")
    monthly_sales = df_with_time.groupBy("year", "month") \
        .agg(
            sum("revenue").alias("total_revenue"),
            count("*").alias("num_transactions")
        ) \
        .withColumn("total_revenue", round(col("total_revenue"), 2)) \
        .orderBy("year", "month")
    
    monthly_sales.show()
    
    # Vendas por dia da semana
    print("\n📊 Vendas por Dia da Semana:")
    daily_pattern = df_with_time.groupBy("day_of_week") \
        .agg(
            sum("revenue").alias("total_revenue"),
            count("*").alias("num_transactions"),
            avg("revenue").alias("avg_transaction")
        ) \
        .withColumn("total_revenue", round(col("total_revenue"), 2)) \
        .withColumn("avg_transaction", round(col("avg_transaction"), 2)) \
        .orderBy("day_of_week")
    
    # Mapeia números para nomes dos dias
    daily_pattern.withColumn(
        "day_name",
        expr("CASE day_of_week " +
             "WHEN 1 THEN 'Domingo' " +
             "WHEN 2 THEN 'Segunda' " +
             "WHEN 3 THEN 'Terça' " +
             "WHEN 4 THEN 'Quarta' " +
             "WHEN 5 THEN 'Quinta' " +
             "WHEN 6 THEN 'Sexta' " +
             "WHEN 7 THEN 'Sábado' END")
    ).select("day_name", "num_transactions", "total_revenue", "avg_transaction").show()
    
    monthly_sales.write.mode("overwrite").csv("data/output/monthly_trends", header=True)
    print("💾 Resultado salvo em: data/output/monthly_trends")
    
    return monthly_sales

def analysis_product_performance(df):
    """
    Análise 6: Performance de Produtos
    Análise detalhada por produto e categoria
    """
    print("\n" + "="*60)
    print("📦 ANÁLISE 6: PERFORMANCE DE PRODUTOS")
    print("="*60)
    
    # Cria view temporária para SQL
    df.createOrReplaceTempView("sales")
    
    # Query SQL complexa
    query = """
        SELECT 
            category,
            product_name,
            COUNT(*) as num_sales,
            SUM(quantity) as total_quantity,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(AVG(price), 2) as avg_price,
            ROUND(AVG(quantity), 2) as avg_quantity_per_sale
        FROM sales
        GROUP BY category, product_name
        ORDER BY category, total_revenue DESC
    """
    
    result = df.sparkSession.sql(query)
    
    print("\n📊 Performance Detalhada por Produto:")
    result.show(50, truncate=False)
    
    result.write.mode("overwrite").csv("data/output/product_performance", header=True)
    print("💾 Resultado salvo em: data/output/product_performance")
    
    return result

def generate_executive_summary(df):
    """
    Gera resumo executivo com KPIs principais
    """
    print("\n" + "="*60)
    print("📊 RESUMO EXECUTIVO - KPIS PRINCIPAIS")
    print("="*60)
    
    # Calcula KPIs
    total_revenue = df.select(sum("revenue")).first()[0]
    total_transactions = df.count()
    avg_ticket = df.select(avg("revenue")).first()[0]
    num_customers = df.select("customer_id").distinct().count()
    num_products = df.select("product_id").distinct().count()

    kpis = [
        ("💰 Receita Total", f"R$ {total_revenue:,.2f}"),
        ("🛒 Total de Transações", f"{total_transactions:,}"),
        ("🎫 Ticket Médio", f"R$ {avg_ticket:,.2f}"),
        ("👥 Clientes Únicos", f"{num_customers:,}"),
        ("📦 Produtos Únicos", f"{num_products:,}"),
    ]

    label_width = 28
    value_width = 18
    content_width = label_width + value_width + 7

    print()
    print("╔" + "═" * content_width + "╗")
    print("║" + "KPIS PRINCIPAIS".center(content_width) + "║")
    print("╠" + "═" * content_width + "╣")
    for label, value in kpis:
        print(f"║  {label + ':':<{label_width}} {value:>{value_width}}   ║")
    print("╚" + "═" * content_width + "╝")

def main():
    """Função principal - orquestra todas as análises"""
    print("=" * 60)
    print("  ANÁLISE DE VENDAS COM PYSPARK")
    print("  Sistema de Business Intelligence para E-commerce")
    print("=" * 60)
    
    start_time = time.time()
    spark = None
    
    try:
        # Cria SparkSession
        spark = create_spark_session()
        spark.sparkContext.setLogLevel("WARN")
        
        print(f"\n⚙️  Configuração do Spark:")
        print(f"   • Versão: {spark.version}")
        print(f"   • Cores: {spark.sparkContext.defaultParallelism}")
        print(f"   • Memória Driver: 2GB")
        print(f"   • Memória Executor: 2GB")
        
        # Arquivo de entrada
        input_file = "data/sales_data.csv"
        
        # Carrega dados
        df = load_data(spark, input_file)
        
        # Cache do DataFrame para melhor performance
        df.cache()
        
        # Exploração inicial
        explore_data(df)
        
        # Executa análises
        analysis_revenue_by_category(df)
        analysis_top_products(df)
        analysis_sales_by_region(df)
        analysis_customer_metrics(df)
        analysis_temporal_trends(df)
        analysis_product_performance(df)
        
        # Resumo executivo
        generate_executive_summary(df)
        
        # Tempo total
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*60)
        print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print(f"\n⏱️  Tempo total de execução: {elapsed_time:.2f} segundos")
        print(f"📁 Resultados salvos em: data/output/")
        
        print("\n📚 Conceitos PySpark demonstrados:")
        print("   • DataFrames e Schema Inference")
        print("   • Transformações (groupBy, agg, join)")
        print("   • Funções de agregação (sum, avg, count)")
        print("   • Funções de janela (Window)")
        print("   • Spark SQL e views temporárias")
        print("   • Lazy Evaluation e Cache")
        print("   • Gravação de resultados em CSV")
        
    except FileNotFoundError:
        print(f"\n❌ Erro: Arquivo não encontrado!")
        print("💡 Execute primeiro: python3 data_generator.py")
    except RuntimeError as e:
        print(f"\n❌ Ambiente incompatível: {e}")
    except Exception as e:
        print(f"\n❌ Erro durante análise: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Encerra SparkSession
        if spark:
            spark.stop()
            print("\n🔚 SparkSession encerrada.")

if __name__ == "__main__":
    main()
