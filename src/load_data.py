import pandas as pd
from sqlalchemy import create_engine

# Apni CSV file ka naam yahan daalo
csv_path = "data/sales.csv"
table_name = "sales"

df = pd.read_csv(csv_path)
print("Data loaded. Shape:", df.shape)
print(df.head())

engine = create_engine("sqlite:///data/askmydata.db")
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Table '{table_name}' successfully created in SQLite DB.")