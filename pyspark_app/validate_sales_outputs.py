#!/usr/bin/env python3
"""Validate generated sales data and reconcile Spark outputs with source totals."""

import csv
from decimal import Decimal
from pathlib import Path


EXPECTED_OUTPUTS = {
    "revenue_by_category",
    "top_products",
    "sales_by_region",
    "customer_metrics",
    "monthly_trends",
    "product_performance",
}
REVENUE_TOLERANCE = Decimal("0.01")


def read_spark_csv(directory):
    part_files = sorted(directory.glob("part-*.csv"))
    if not part_files:
        raise ValueError(f"Nenhum arquivo part-*.csv encontrado em {directory}")

    rows = []
    for part_file in part_files:
        with part_file.open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError(f"CSV sem cabecalho: {part_file}")
            rows.extend(reader)
    if not rows:
        raise ValueError(f"Nenhuma linha de dados encontrada em {directory}")
    return rows


def decimal_value(row, column):
    try:
        return Decimal(row[column])
    except (KeyError, ArithmeticError, ValueError) as error:
        raise ValueError(f"Valor invalido na coluna '{column}': {row}") from error


def require_close(actual, expected, description, tolerance=REVENUE_TOLERANCE):
    if abs(actual - expected) > tolerance:
        raise ValueError(
            f"{description}: esperado {expected}, encontrado {actual} "
            f"(tolerancia {tolerance})"
        )


def validate_sales_outputs():
    data_dir = Path("data")
    output_dir = data_dir / "output"
    source_file = data_dir / "sales_data.csv"

    with source_file.open(encoding="utf-8", newline="") as file:
        sales = list(csv.DictReader(file))
    if not sales:
        raise ValueError(f"Nenhuma transacao encontrada em {source_file}")

    required_columns = {
        "transaction_id", "date", "customer_id", "product_id",
        "product_name", "category", "quantity", "price", "region",
    }
    if not required_columns.issubset(sales[0]):
        missing = sorted(required_columns - set(sales[0]))
        raise ValueError(f"Colunas ausentes em {source_file}: {', '.join(missing)}")

    total_revenue = sum(
        (Decimal(row["quantity"]) * Decimal(row["price"]) for row in sales),
        Decimal("0"),
    )
    expected_groups = {}
    for dimension in ("category", "region"):
        groups = {}
        for sale in sales:
            key = sale[dimension]
            group = groups.setdefault(key, {"count": 0, "quantity": 0, "revenue": Decimal("0")})
            group["count"] += 1
            group["quantity"] += int(sale["quantity"])
            group["revenue"] += Decimal(sale["quantity"]) * Decimal(sale["price"])
        expected_groups[dimension] = groups
    expected_pairs = {}
    for sale in sales:
        key = (sale["region"], sale["category"])
        group = expected_pairs.setdefault(
            key, {"count": 0, "quantity": 0, "revenue": Decimal("0")}
        )
        group["count"] += 1
        group["quantity"] += int(sale["quantity"])
        group["revenue"] += Decimal(sale["quantity"]) * Decimal(sale["price"])

    missing_outputs = sorted(name for name in EXPECTED_OUTPUTS if not (output_dir / name).is_dir())
    if missing_outputs:
        raise ValueError(
            f"Diretorios Spark ausentes em {output_dir}: {', '.join(missing_outputs)}"
        )

    category_rows = read_spark_csv(output_dir / "revenue_by_category")
    if {row["category"] for row in category_rows} != set(expected_groups["category"]):
        raise ValueError("Categorias da saida nao correspondem ao CSV de origem")
    for row in category_rows:
        expected = expected_groups["category"][row["category"]]
        if int(row["num_transactions"]) != expected["count"]:
            raise ValueError(f"Contagem de transacoes divergente para {row['category']}")
        require_close(
            decimal_value(row, "total_revenue"),
            expected["revenue"],
            f"Receita da categoria {row['category']}",
        )
    require_close(
        sum((decimal_value(row, "total_revenue") for row in category_rows), Decimal("0")),
        total_revenue,
        "Soma das receitas por categoria",
        Decimal("0.01") * len(category_rows),
    )

    region_rows = read_spark_csv(output_dir / "sales_by_region")
    if {row["region"] for row in region_rows} != set(expected_groups["region"]):
        raise ValueError("Regioes da saida nao correspondem ao CSV de origem")
    for row in region_rows:
        expected = expected_groups["region"][row["region"]]
        if int(row["num_transactions"]) != expected["count"]:
            raise ValueError(f"Contagem de transacoes divergente para {row['region']}")
        require_close(
            decimal_value(row, "total_revenue"),
            expected["revenue"],
            f"Receita da regiao {row['region']}",
        )
    require_close(
        sum((decimal_value(row, "total_revenue") for row in region_rows), Decimal("0")),
        total_revenue,
        "Soma das receitas por regiao",
        Decimal("0.01") * len(region_rows),
    )

    monthly_rows = read_spark_csv(output_dir / "monthly_trends")
    if sum(int(row["num_transactions"]) for row in monthly_rows) != len(sales):
        raise ValueError("A soma das transacoes mensais nao corresponde ao total de vendas")
    require_close(
        sum((decimal_value(row, "total_revenue") for row in monthly_rows), Decimal("0")),
        total_revenue,
        "Soma das receitas mensais",
        Decimal("0.01") * len(monthly_rows),
    )

    customer_rows = read_spark_csv(output_dir / "customer_metrics")
    if sum(int(row["num_purchases"]) for row in customer_rows) != len(sales):
        raise ValueError("A soma das compras por cliente nao corresponde ao total de vendas")
    customer_tolerance = Decimal("0.01") * len(customer_rows)
    require_close(
        sum((decimal_value(row, "total_spent") for row in customer_rows), Decimal("0")),
        total_revenue,
        "Soma dos gastos por cliente",
        customer_tolerance,
    )

    product_rows = read_spark_csv(output_dir / "product_performance")
    if sum(int(row["num_sales"]) for row in product_rows) != len(sales):
        raise ValueError("A soma das vendas por produto nao corresponde ao total de vendas")
    require_close(
        sum((decimal_value(row, "total_revenue") for row in product_rows), Decimal("0")),
        total_revenue,
        "Soma das receitas por produto",
        Decimal("0.01") * len(product_rows),
    )

    top_products = read_spark_csv(output_dir / "top_products")
    if len(top_products) != min(10, len(product_rows)):
        raise ValueError("A saida de top_products nao tem ate 10 produtos como esperado")

    optional_path = output_dir / "revenue_by_region_category"
    if optional_path.is_dir():
        extra_rows = read_spark_csv(optional_path)
        expected_extra_columns = {
            "region", "category", "total_revenue", "total_quantity", "num_transactions",
        }
        if not expected_extra_columns.issubset(extra_rows[0]):
            raise ValueError(
                "A analise opcional precisa das colunas region, category, total_revenue, "
                "total_quantity e num_transactions"
            )
        actual_pairs = {(row["region"], row["category"]) for row in extra_rows}
        if actual_pairs != set(expected_pairs):
            raise ValueError("Grupos da analise opcional nao correspondem ao CSV de origem")
        for row in extra_rows:
            expected = expected_pairs[(row["region"], row["category"])]
            if int(row["num_transactions"]) != expected["count"]:
                raise ValueError(
                    f"Contagem de transacoes divergente para {row['region']}/{row['category']}"
                )
            if int(row["total_quantity"]) != expected["quantity"]:
                raise ValueError(
                    f"Quantidade divergente para {row['region']}/{row['category']}"
                )
            require_close(
                decimal_value(row, "total_revenue"),
                expected["revenue"],
                f"Receita de {row['region']}/{row['category']}",
            )
        if sum(int(row["num_transactions"]) for row in extra_rows) != len(sales):
            raise ValueError("A analise opcional nao reconcilia o total de transacoes")
        require_close(
            sum((decimal_value(row, "total_revenue") for row in extra_rows), Decimal("0")),
            total_revenue,
            "Receita da analise opcional",
            Decimal("0.01") * len(extra_rows),
        )
        print("OK: saida opcional por regiao e categoria validada.")

    print(
        f"OK: {len(sales)} transacoes; receita total {total_revenue:.2f}; "
        "saidas por categoria, regiao, mes, cliente e produto reconciliadas."
    )


def main():
    try:
        validate_sales_outputs()
    except (OSError, ValueError, KeyError) as error:
        print(f"ERRO: validacao das saidas falhou: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
