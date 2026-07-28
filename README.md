# 📊 AskMyData — AI-Powered Text-to-SQL Analytics Agent

AskMyData lets you ask questions about retail sales data in plain English and instantly get SQL queries, data tables, auto-generated charts, and AI-written insights — no SQL knowledge required.

![Demo](screenshots/demo1.png)

##  Features

- **Natural Language to SQL**: Converts plain English questions into valid SQL queries using Google Gemini
- **Instant Query Execution**: Runs the generated SQL against a SQLite database and displays results
- **Auto Chart Generation**: Automatically creates bar charts for multi-row results using Matplotlib
- **AI-Generated Insights**: Produces short, human-readable summaries highlighting key patterns in the data
- **Multi-Model Fallback**: Automatically switches between multiple Gemini models to handle rate limits and downtime gracefully
- **SQL Safety Guardrails**: Restricts AI-generated queries to read-only SELECT statements, blocking destructive commands
- **Interactive Web UI**: Built with Streamlit, includes sample questions, question history, and a clean interface

##  Tech Stack

- **Language**: Python
- **AI/LLM**: Google Gemini API (`google-genai`)
- **Database**: SQLite, SQLAlchemy
- **Data Processing**: Pandas
- **Visualization**: Matplotlib
- **Frontend**: Streamlit

##  Dataset

Superstore Sales dataset — 9,800 rows, 18 columns including Order details, Customer, Region, Category, and Sales data.

##  How It Works

1. User asks a question in plain English (e.g. "What is the total sales by region?")
2. The question + database schema is sent to Gemini, which generates a SQL query
3. The query is validated (SELECT-only) and executed against the SQLite database
4. Results are displayed as a table, converted into a chart (if applicable), and summarized by AI into a plain-English insight

##  Setup & Installation

```bash
git clone https://github.com/Prajjwalkumar-ai/AskMyData.git
cd AskMyData
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Create a `.env` file in the root directory: