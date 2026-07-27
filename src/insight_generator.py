import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_insight(question: str, columns, rows) -> str:
    columns = list(columns)
    data_preview = "\n".join(
        [", ".join(str(v) for v in row) for row in rows[:20]]
    )

    prompt = f"""You are a data analyst. Based on the following query result, write a short,
insightful summary in 2-3 sentences. Highlight key patterns, top/bottom performers,
or notable differences. Be specific with numbers. Do not repeat the raw data table.

User's question: {question}

Columns: {', '.join(columns)}

Data:
{data_preview}

Insight summary:"""

    models_to_try = [
    "gemini-flash-lite-latest",
    "gemini-2.0-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
]

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Insight model '{model_name}' failed: {e}")

    return "(Insight generation failed — could not reach any AI model.)"