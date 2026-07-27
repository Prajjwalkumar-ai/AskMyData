import matplotlib.pyplot as plt
import os


def generate_chart(columns, rows, question: str):
    """
    Generates a bar chart if data is suitable (2 columns, multiple rows).
    Returns the chart file path, or None if chart isn't applicable.
    """
    columns = list(columns)

    # Chart tabhi banao jab exactly 2 columns hon aur kam se kam 2 rows hon
    if len(columns) != 2 or len(rows) < 2:
        return None

    labels = [str(row[0]) for row in rows]
    values = [row[1] for row in rows]

    # Ensure values numeric hain
    try:
        values = [float(v) for v in values]
    except (ValueError, TypeError):
        return None

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color="#4C72B0")
    plt.xlabel(columns[0])
    plt.ylabel(columns[1])
    plt.title(question[:60])
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    os.makedirs("charts", exist_ok=True)
    chart_path = os.path.join("charts", "latest_chart.png")
    plt.savefig(chart_path)
    plt.close()

    return chart_path