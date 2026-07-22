from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/askmydata.db")

queries = {
    "Total Sales": "SELECT SUM(Sales) as total_sales FROM sales;",
    "Top 5 Categories by Sales": """
        SELECT Category, SUM(Sales) as total_sales
        FROM sales
        GROUP BY Category
        ORDER BY total_sales DESC
        LIMIT 5;
    """,
    "Sales by Region": """
        SELECT Region, SUM(Sales) as total_sales
        FROM sales
        GROUP BY Region
        ORDER BY total_sales DESC;
    """,
    "Top 5 Customers": """
        SELECT [Customer Name], SUM(Sales) as total_sales
        FROM sales
        GROUP BY [Customer Name]
        ORDER BY total_sales DESC
        LIMIT 5;
    """,
}

with engine.connect() as conn:
    for name, query in queries.items():
        print(f"\n=== {name} ===")
        result = conn.execute(text(query))
        for row in result:
            print(row)