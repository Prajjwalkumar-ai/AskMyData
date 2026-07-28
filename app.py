import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from text_to_sql import generate_sql, execute_sql
from chart_generator import generate_chart
from insight_generator import generate_insight

st.set_page_config(page_title="AskMyData", page_icon="📊", layout="centered")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("About")
    st.write(
        "AskMyData is an AI-powered analytics agent. "
        "Ask questions about the Superstore Sales dataset in plain English "
        "and get instant SQL queries, tables, charts, and AI-generated insights."
    )
    st.markdown("---")
    st.subheader("Try these sample questions")
    sample_questions = [
        "What is the total sales by region?",
        "Which category has the highest sales?",
        "Show me top 5 customers by sales",
        "Compare sales of Technology vs Furniture by region",
        "What is the total sales in the West region?",
    ]
    for sq in sample_questions:
        if st.button(sq, key=sq):
            st.session_state["question_input"] = sq

# ---------- Session state for history ----------
if "history" not in st.session_state:
    st.session_state["history"] = []

if "question_input" not in st.session_state:
    st.session_state["question_input"] = ""

# ---------- Main UI ----------
st.title("📊 AskMyData")
st.caption("Ask questions about your sales data in plain English — powered by AI")

question = st.text_input(
    "Ask a question about your data:",
    value=st.session_state["question_input"],
    placeholder="e.g. What is the total sales by region?",
    key="question_box"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please type a question before clicking Ask.")
        st.stop()

    with st.spinner("Generating SQL query..."):
        try:
            sql_query = generate_sql(question)
        except Exception as e:
            st.error(f"Failed to generate SQL: {e}")
            st.stop()

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    with st.spinner("Running query..."):
        try:
            columns, rows = execute_sql(sql_query)
        except Exception as e:
            st.error(f"Failed to execute SQL: {e}")
            st.stop()

    st.subheader("Result")
    if rows:
        df = pd.DataFrame(rows, columns=list(columns))
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Query ran successfully but returned no rows.")

    chart_path = generate_chart(columns, rows, question)
    if chart_path:
        st.subheader("Chart")
        st.image(chart_path)

    insight = None
    with st.spinner("Generating insight..."):
        try:
            insight = generate_insight(question, columns, rows)
            st.subheader("💡 AI Insight")
            st.write(insight)
        except Exception as e:
            st.warning(f"Could not generate insight: {e}")

    # Save to history
    st.session_state["history"].insert(0, {
        "question": question,
        "sql": sql_query,
        "insight": insight,
    })

# ---------- Question History ----------
if st.session_state["history"]:
    st.markdown("---")
    st.subheader("🕘 Recent Questions")
    for item in st.session_state["history"][:5]:
        with st.expander(item["question"]):
            st.code(item["sql"], language="sql")
            if item["insight"]:
                st.write(item["insight"])