from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///data/askmydata.db")
inspector = inspect(engine)

tables = inspector.get_table_names()
print("Tables in DB:", tables)

for table in tables:
    print(f"\n--- Schema for '{table}' ---")
    columns = inspector.get_columns(table)
    for col in columns:
        print(f"  {col['name']} ({col['type']})")