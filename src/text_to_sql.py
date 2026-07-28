import os
import re
import time
from dotenv import load_dotenv
from google import genai
from schema_context import SCHEMA_CONTEXT
from sqlalchemy import create_engine, text
from chart_generator import generate_chart
from insight_generator import generate_insight

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_sql(user_question: str, max_retries: int = 2) -> str:
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

    models_to_try = [
    "gemini-flash-lite-latest",
    "gemini-2.0-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
]

    last_error = None
    for model_name in models_to_try:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                sql = response.text.strip()
                sql = re.sub(r"^```sql\s*|\s*```$", "", sql, flags=re.MULTILINE).strip()
                sql = re.sub(r"^```\s*|\s*```$", "", sql, flags=re.MULTILINE).strip()
                return sql
            except Exception as e:
                last_error = e
                print(f"Model '{model_name}', attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(8)

    raise Exception(f"All models failed. Last error: {last_error}")


def execute_sql(sql_query: str):
   
    forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    sql_upper = sql_query.strip().upper()

    if not sql_upper.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed for safety reasons.")

    if any(keyword in sql_upper for keyword in forbidden_keywords):
        raise ValueError("Query contains a forbidden keyword and was blocked for safety.")

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
            chart_path = generate_chart(columns, rows, test_question)
            if chart_path:
                print(f"\n📊 Chart saved at: {chart_path}")
            else:
                print("\n(No chart generated — data not suitable for a chart)")

            insight = generate_insight(test_question, columns, rows)
            print(f"\n💡 Insight: {insight}")
        except Exception as e:
            print("\nError:", e)

        print("\n" + "-" * 50 + "\n")