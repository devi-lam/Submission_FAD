import streamlit as st
import pandas as pd

# CONFIG
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("E-Commerce Dashboard")

# LOAD DATA
df = pd.read_csv("../main_data.csv")

# Preprocessing
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['revenue'] = df['price'] + df['freight_value']


# FILTER INTERAKTIF

st.sidebar.header("Filter Data")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

category_list = df['product_category_name_english'].dropna().unique()

selected_category = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=category_list,
    default=category_list
)


# APPLY FILTER

df_filtered = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(date_range[1])) &
    (df['product_category_name_english'].isin(selected_category))
]


# KPI

st.header("Summary")

total_revenue = df_filtered['revenue'].sum()
total_orders = df_filtered['order_id'].nunique()

col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)


# BUSINESS QUESTION 1

st.header("Produk kategori dengan revenue terbesar (2017–2018)")

df_q1 = df_filtered[
    (df_filtered['order_purchase_timestamp'].dt.year >= 2017) &
    (df_filtered['order_purchase_timestamp'].dt.year <= 2018)
]

category_revenue = (
    df_q1.groupby('product_category_name_english')['revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("Top 10 Category by Revenue")
st.bar_chart(category_revenue)

if not category_revenue.empty:
    top_category = category_revenue.idxmax()
    st.success(f"Kategori dengan revenue terbesar: **{top_category}**")


# BUSINESS QUESTION 2

st.header("Tren order bulanan & puncak transaksi (2016–2018)")

df_q2 = df_filtered[
    (df_filtered['order_purchase_timestamp'].dt.year >= 2016) &
    (df_filtered['order_purchase_timestamp'].dt.year <= 2018)
]

df_q2['month'] = df_q2['order_purchase_timestamp'].dt.to_period('M').astype(str)

monthly_orders = df_q2.groupby('month')['order_id'].nunique()

st.subheader("Monthly Order Trend")
st.line_chart(monthly_orders)

if not monthly_orders.empty:
    peak_month = monthly_orders.idxmax()
    peak_value = monthly_orders.max()

    st.success(f"Puncak transaksi: **{peak_month}** dengan **{peak_value} orders**")


# PENJELASAN INTERAKTIF

st.markdown("""
### 🎛️ Fitur Interaktif
Dashboard ini menyediakan:
- Filter rentang tanggal
- Filter kategori produk

Filter tersebut akan langsung mempengaruhi:
- Total revenue
- Jumlah order
- Grafik kategori dan tren bulanan

Sehingga pengguna dapat melakukan eksplorasi data secara dinamis.
""")