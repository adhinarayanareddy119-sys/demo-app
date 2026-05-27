import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Region Analysis", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("data/sales.xls", engine="xlrd")

df = load_data()

df.columns = df.columns.str.strip()

# Date conversion
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year

st.title("Region Analysis Dashboard")

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].dropna().unique(),
    default=df["Region"].dropna().unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].dropna().unique(),
    default=df["Category"].dropna().unique()
)

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Region"].isin(region_filter)
]

filtered_df = filtered_df[
    filtered_df["Category"].isin(category_filter)
]

# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("Region Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"{filtered_df['Sales'].sum():,.2f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"{filtered_df['Profit'].sum():,.2f}"
    )

with col3:
    st.metric(
        "Total Orders",
        filtered_df["Order ID"].nunique()
    )

# -----------------------------
# Region Wise Sales
# -----------------------------
st.subheader("Region Wise Sales")

region_sales = filtered_df.groupby(
    "Region",
    as_index=False
)["Sales"].sum()

fig1 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    text_auto=True,
    title="Region Wise Sales"
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

fig2 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Region",
    text_auto=True,
    title="Region Wise Profit"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Region Wise Quantity
# -----------------------------
st.subheader("Region Wise Quantity")

region_qty = filtered_df.groupby(
    "Region",
    as_index=False
)["Quantity"].sum()

fig3 = px.pie(
    region_qty,
    names="Region",
    values="Quantity",
    title="Region Wise Quantity Share"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Region and Category Analysis
# -----------------------------
st.subheader("Region and Category Sales")

region_category = filtered_df.groupby(
    ["Region", "Category"],
    as_index=False
)["Sales"].sum()

fig4 = px.bar(
    region_category,
    x="Region",
    y="Sales",
    color="Category",
    barmode="group",
    title="Region and Category Sales"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Year Wise Regional Sales
# -----------------------------
st.subheader("Year Wise Regional Sales")

if "Year" in filtered_df.columns:

    yearly_region = filtered_df.groupby(
        ["Year", "Region"],
        as_index=False
    )["Sales"].sum()

    fig5 = px.line(
        yearly_region,
        x="Year",
        y="Sales",
        color="Region",
        markers=True,
        title="Year Wise Regional Sales"
    )

    st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# Region Summary Table
# -----------------------------
st.subheader("Region Summary Table")

summary = filtered_df.groupby(
    "Region",
    as_index=False
).agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum",
    "Discount": "mean"
})

st.dataframe(summary, use_container_width=True)