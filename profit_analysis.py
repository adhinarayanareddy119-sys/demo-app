import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Profit Analysis", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("data/sales.xls", engine="xlrd")

df = load_data()

df.columns = df.columns.str.strip()

# Convert Date
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()

st.title("Profit Analysis Dashboard")

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")

# Category Filter
if "Category" in df.columns:
    category_filter = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].dropna().unique(),
        default=df["Category"].dropna().unique()
    )
else:
    category_filter = []

# Region Filter
if "Region" in df.columns:
    region_filter = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].dropna().unique(),
        default=df["Region"].dropna().unique()
    )
else:
    region_filter = []

filtered_df = df.copy()

if category_filter:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(category_filter)
    ]

if region_filter:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(region_filter)
    ]

# -----------------------------
# KPI Metrics
# -----------------------------
st.subheader("Profit Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Profit",
        f"{filtered_df['Profit'].sum():,.2f}"
    )

with col2:
    st.metric(
        "Average Profit",
        f"{filtered_df['Profit'].mean():,.2f}"
    )

with col3:
    st.metric(
        "Maximum Profit",
        f"{filtered_df['Profit'].max():,.2f}"
    )

# -----------------------------
# Category Wise Profit
# -----------------------------
st.subheader("Category Wise Profit")

category_profit = filtered_df.groupby(
    "Category",
    as_index=False
)["Profit"].sum()

fig1 = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Category",
    text_auto=True,
    title="Category Wise Profit"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Region Wise Profit
# -----------------------------
st.subheader("Region Wise Profit")

region_profit = filtered_df.groupby(
    "Region",
    as_index=False
)["Profit"].sum()

fig2 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Region Wise Profit Share"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Monthly Profit Trend
# -----------------------------
st.subheader("Monthly Profit Trend")

if "Order Date" in filtered_df.columns:

    monthly_profit = filtered_df.groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Profit"].sum().reset_index()

    monthly_profit["Order Date"] = monthly_profit["Order Date"].astype(str)

    fig3 = px.line(
        monthly_profit,
        x="Order Date",
        y="Profit",
        markers=True,
        title="Monthly Profit Trend"
    )

    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Profit vs Discount
# -----------------------------
st.subheader("Profit vs Discount")

fig4 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    title="Discount vs Profit"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Profit Summary Table
# -----------------------------
st.subheader("Profit Summary Table")

summary = filtered_df.groupby(
    ["Category", "Region"],
    as_index=False
).agg({
    "Profit": "sum",
    "Sales": "sum",
    "Quantity": "sum"
})

st.dataframe(summary, use_container_width=True)