import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from text_to_sql import generate_sql, execute_sql
from chart_generator import generate_chart
from insight_generator import generate_insight

st.set_page_config(page_title="AskMyData", page_icon="📊", layout="centered")

st.title("📊 AskMyData")
st.caption("Ask questions about your sales data in plain English — powered by AI")

question = st.text_input("Ask a question about your data:", placeholder="e.g. What is the total sales by region?")

if st.button("Ask") and question.strip():
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
        import pandas as pd
        df = pd.DataFrame(rows, columns=list(columns))
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Query ran successfully but returned no rows.")

    chart_path = generate_chart(columns, rows, question)
    if chart_path:
        st.subheader("Chart")
        st.image(chart_path)

    with st.spinner("Generating insight..."):
        try:
            insight = generate_insight(question, columns, rows)
            st.subheader("💡 AI Insight")
            st.write(insight)
        except Exception as e:
            st.warning(f"Could not generate insight: {e}")