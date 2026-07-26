import os
import re
import time
from dotenv import load_dotenv
from google import genai
from schema_context import SCHEMA_CONTEXT
from sqlalchemy import create_engine, text

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_sql(user_question: str, max_retries: int = 3) -> str:
    prompt = f"""You are an expert SQL assistant. Convert the user's question into a valid SQLite SQL query.

Database schema:
{SCHEMA_CONTEXT}

Rules:
- Only return the SQL query, nothing else. No explanation, no markdown formatting.
- Use double quotes for column names that contain spaces (e.g. "Customer Name").
- The table name is "sales".
- Always add LIMIT 100 if the query could return many rows, unless user asks for aggregated/summary data.

User question: {user_question}

SQL query:"""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            sql = response.text.strip()
            sql = re.sub(r"^```sql\s*|\s*```$", "", sql, flags=re.MULTILINE).strip()
            sql = re.sub(r"^```\s*|\s*```$", "", sql, flags=re.MULTILINE).strip()
            return sql
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                raise


def execute_sql(sql_query: str):
    engine = create_engine("sqlite:///data/askmydata.db")
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        rows = result.fetchall()
        columns = result.keys()
        return columns, rows


if __name__ == "__main__":
    print("=== AskMyData: AI Data Analyst Agent ===")
    print("Ask Your Question: ? (Or Type 'exit' To End Terminal)\n")

    while True:
        test_question = input("Your Question: ").strip()

        if test_question.lower() in ("exit", "quit"):
            print("Session end. Bye!")
            break

        if not test_question:
            continue

        try:
            sql_query = generate_sql(test_question)
            print("\nGenerated SQL:\n", sql_query)

            columns, rows = execute_sql(sql_query)
            print("\nColumns:", list(columns))
            print("Result:")
            for row in rows:
                print(row)
        except Exception as e:
            print("\nError:", e)

        print("\n" + "-" * 50 + "\n")