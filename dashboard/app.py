import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="E-Commerce Sales Dashboard", page_icon="📈", layout="wide")

# Database connection
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'ecommerce.db')

@st.cache_data
def load_data(query):
    """Executes a SQL query and returns a pandas DataFrame."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Title and Description
st.title("📈 E-Commerce Sales Analytics Dashboard")
st.markdown("**Created by Siddharth Singh**")
st.markdown("Analyze E-commerce performance, customer behavior, and product trends.")

# Ensure DB exists
if not os.path.exists(DB_PATH):
    st.warning("Database not found. Please ensure you have run `data_prep.py` and `sql_analysis.py` first.")
    st.stop()

# Load summary metrics
st.header("Overall KPIs")
metrics_query = """
SELECT 
    COUNT(DISTINCT order_id) as total_orders,
    SUM(sales) as total_revenue,
    SUM(sales) / COUNT(DISTINCT order_id) as average_order_value
FROM sales
"""
metrics_df = load_data(metrics_query)

if not metrics_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", f"{metrics_df['total_orders'][0]:,}")
    col2.metric("Total Revenue", f"${metrics_df['total_revenue'][0]:,.2f}")
    col3.metric("Average Order Value (AOV)", f"${metrics_df['average_order_value'][0]:,.2f}")

st.divider()

# Layout: 2 Columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Revenue Trend")
    monthly_rev_query = """
    SELECT 
        order_year_month, 
        SUM(sales) as total_revenue
    FROM sales
    GROUP BY order_year_month
    ORDER BY order_year_month
    """
    monthly_rev_df = load_data(monthly_rev_query)
    
    if not monthly_rev_df.empty:
        fig1 = px.line(monthly_rev_df, x='order_year_month', y='total_revenue', markers=True, 
                       labels={'order_year_month': 'Month', 'total_revenue': 'Revenue ($)'},
                       title='Revenue Over Time')
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Top Selling Products")
    top_prod_query = """
    SELECT 
        category, 
        SUM(quantity) as total_items_sold 
    FROM sales
    WHERE category != 'unknown'
    GROUP BY category
    ORDER BY total_items_sold DESC
    LIMIT 10
    """
    top_prod_df = load_data(top_prod_query)
    
    if not top_prod_df.empty:
        fig2 = px.bar(top_prod_df, x='total_items_sold', y='category', orientation='h',
                      labels={'total_items_sold': 'Units Sold', 'category': 'Category'},
                      title='Top 10 Product Categories')
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Region")
    state_sales_query = """
    SELECT 
        region, 
        SUM(sales) as total_sales
    FROM sales
    GROUP BY region
    ORDER BY total_sales DESC
    LIMIT 15
    """
    state_sales_df = load_data(state_sales_query)
    
    if not state_sales_df.empty:
        fig3 = px.bar(state_sales_df, x='region', y='total_sales',
                      labels={'region': 'Region', 'total_sales': 'Total Sales ($)'},
                      title='Revenue by Region', color='total_sales', color_continuous_scale='Viridis')
        st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Customer Purchase Frequency")
    freq_query = """
    SELECT 
        purchase_count, 
        COUNT(customer_name) as num_customers
    FROM (
        SELECT 
            customer_name, 
            COUNT(DISTINCT order_id) as purchase_count
        FROM sales
        GROUP BY customer_name
    )
    GROUP BY purchase_count
    ORDER BY purchase_count
    LIMIT 5
    """
    freq_df = load_data(freq_query)
    
    if not freq_df.empty:
        # Map > 1 to "Returning" to simplify
        freq_df['customer_type'] = freq_df['purchase_count'].apply(lambda x: 'One-time' if x == 1 else f'{x} Purchases')
        
        # Don't aggregate by standard string replacement immediately if we want a clean pie, 
        # let's just make a bar chart of frequency distribution.
        fig4 = px.pie(freq_df, names='customer_type', values='num_customers', 
                      title='Distribution of Purchase Frequency', hole=0.4)
        st.plotly_chart(fig4, use_container_width=True)

st.sidebar.header("About")
st.sidebar.info("This dashboard visualizes E-commerce performance, customer behavior, and product trends based on the current dataset.")
st.sidebar.markdown("---")
st.sidebar.markdown("**Tech Stack:**\n- Streamlit\n- Plotly\n- SQLite\n- Pandas")
