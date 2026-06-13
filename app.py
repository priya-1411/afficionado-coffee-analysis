import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coffee Dashboard", layout="wide")

# Load Data
df = pd.read_csv("Transactions.csv")

# Revenue Column
df["Revenue"] = df["transaction_qty"] * df["unit_price"]

st.title("☕ Afficionado Coffee Roasters Dashboard")

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"${df['Revenue'].sum():,.2f}"
)

col2.metric(
    "Total Transactions",
    len(df)
)

col3.metric(
    "Total Products",
    df["product_detail"].nunique()
)

# Category Revenue
st.subheader("Revenue by Category")

category_revenue = df.groupby(
    "product_category"
)["Revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()

category_revenue.plot(
    kind="bar",
    ax=ax
)

st.pyplot(fig)

# Top Products
st.subheader("Top 10 Products by Sales Volume")

top_products = (
    df.groupby("product_detail")
    ["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()

top_products.plot(
    kind="bar",
    ax=ax2
)

st.pyplot(fig2)

# Dataset Preview
st.subheader("Dataset Preview")

st.dataframe(df.head())
