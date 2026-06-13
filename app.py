import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coffee Dashboard", layout="wide")

# Load Data
df = pd.read_csv("Transactions.csv")

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(df["product_category"].unique())
)

if selected_category != "All":
    filtered_df = df[df["product_category"] == selected_category]
else:
    filtered_df = df

top_n = st.sidebar.slider(
    "Select Top Products",
    min_value=5,
    max_value=20,
    value=10
)

top_products = (
    filtered_df.groupby("product_detail")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)
# Revenue Column
filtered_df["Revenue"] = filtered_df["transaction_qty"] * filtered_df["unit_price"]

st.title("☕ Afficionado Coffee Roasters Dashboard")

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"${filtered_df['Revenue'].sum():,.2f}"
)

col2.metric(
    "Total Transactions",
    len(filtered_df)
)

col3.metric(
    "Total Products",
    filtered_df["product_detail"].nunique()
)

# Category Revenue
st.subheader("Revenue by Category")

category_revenue = filtered_df.groupby(
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
    filtered_df.groupby("product_detail")
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

st.subheader("Category Revenue Share")

category_revenue = (
    filtered_df.groupby("product_category")["Revenue"]
    .sum()
)

fig, ax = plt.subplots(figsize=(8,8))

ax.pie(
    category_revenue,
    labels=category_revenue.index,
    autopct="%1.1f%%"
)

st.pyplot(fig)

st.subheader("Pareto Analysis")

product_revenue = (
    filtered_df.groupby("product_detail")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

pareto = product_revenue.reset_index()

pareto.columns = ["Product","Revenue"]

pareto["Cumulative %"] = (
    pareto["Revenue"].cumsum()
    / pareto["Revenue"].sum()
)*100

st.line_chart(
    pareto.set_index("Product")["Cumulative %"]
)

st.subheader("Popularity vs Revenue")

summary = filtered_df.groupby("product_detail").agg({
    "transaction_qty":"sum",
    "Revenue":"sum"
})

fig, ax = plt.subplots(figsize=(10,6))

ax.scatter(
    summary["transaction_qty"],
    summary["Revenue"]
)

ax.set_xlabel("Sales Volume")
ax.set_ylabel("Revenue")
ax.set_title("Popularity vs Revenue")

st.pyplot(fig)