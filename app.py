import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page configuration
st.set_page_config(page_title="Superstore Sales Analysis", layout="wide")

# Keep full KPI amounts readable on narrower desktop screens.
st.markdown("""<style>
[data-testid="stMetricValue"] { font-size: 1.5rem; }
</style>""", unsafe_allow_html=True)

# Title
st.title("Superstore Sales Performance Analysis")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel(Path(__file__).resolve().parent / "DataSet" / "Superstore_Orders_Data.xlsx")
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
    df['Year'] = df['Order_Date'].dt.year
    df['Month'] = df['Order_Date'].dt.month_name()
    df['Month_Num'] = df['Order_Date'].dt.month
    return df

try:
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Year filter
    years = df['Year'].unique()
    selected_years = st.sidebar.multiselect("Select Years", years, default=years)
    
    # Region filter
    regions = df['Region'].unique()
    selected_regions = st.sidebar.multiselect("Select Regions", regions, default=regions)
    
    # Category filter
    categories = df['Category'].unique()
    selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)
    
    # Segment filter
    segments = df['Segment'].unique()
    selected_segments = st.sidebar.multiselect("Select Segments", segments, default=segments)
    
    # Apply filters
    filtered_df = df[
        (df['Year'].isin(selected_years)) &
        (df['Region'].isin(selected_regions)) &
        (df['Category'].isin(selected_categories)) &
        (df['Segment'].isin(selected_segments))
    ]
    
    if filtered_df.empty:
        st.info("No orders match these filters. Select at least one value in each filter.")
        st.stop()

    # KPI Cards
    st.header("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_quantity = filtered_df['Quantity'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Quantity", f"{total_quantity:,.0f}")
    col4.metric("Profit Margin", f"{profit_margin:.2f}%")
    
    st.markdown("---")
    
    # Row 1: Sales by Category and Region
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales by Category")
        category_sales = filtered_df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        fig_cat = px.bar(category_sales, x='Category', y='Sales', 
                         title="Sales by Category",
                         color='Sales',
                         color_continuous_scale='Blues')
        st.plotly_chart(fig_cat, width='stretch')
    
    with col2:
        st.subheader("Sales by Region")
        region_sales = filtered_df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        fig_region = px.pie(region_sales, values='Sales', names='Region',
                           title="Sales Distribution by Region")
        st.plotly_chart(fig_region, width='stretch')
    
    # Row 2: Monthly Sales Trend
    st.subheader("Monthly Sales Trend")
    monthly_sales = filtered_df.groupby(['Year', 'Month_Num', 'Month']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_sales = monthly_sales.sort_values(['Year', 'Month_Num'])
    
    fig_monthly = px.line(monthly_sales, x='Month', y='Sales', 
                         color='Year',
                         title="Monthly Sales Trend by Year",
                         markers=True)
    st.plotly_chart(fig_monthly, width='stretch')
    
    # Row 3: Top and Bottom Products
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Products by Sales")
        top_products = filtered_df.groupby('Product_Name').agg({
            'Sales': 'sum'
        }).nlargest(10, 'Sales').reset_index()
        fig_top = px.bar(top_products, x='Sales', y='Product_Name',
                       orientation='h',
                       title="Top 10 Products by Sales")
        st.plotly_chart(fig_top, width='stretch')
    
    with col2:
        st.subheader("Bottom 10 Products by Profit")
        bottom_products = filtered_df.groupby('Product_Name').agg({
            'Profit': 'sum'
        }).nsmallest(10, 'Profit').reset_index()
        fig_bottom = px.bar(bottom_products, x='Profit', y='Product_Name',
                          orientation='h',
                          title="Bottom 10 Products by Profit",
                          color='Profit',
                          color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_bottom, width='stretch')
    
    # Row 4: Segment Analysis
    st.subheader("Sales by Customer Segment")
    segment_sales = filtered_df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    fig_segment = px.bar(segment_sales, x='Segment', y='Sales',
                        title="Sales by Customer Segment",
                        color='Profit',
                        color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_segment, width='stretch')
    
    # Row 5: Ship Mode Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ship Mode Usage")
        ship_mode = filtered_df.groupby('Ship_Mode').agg({
            'Sales': 'sum'
        }).reset_index()
        fig_ship = px.pie(ship_mode, values='Sales', names='Ship_Mode',
                         title="Sales by Ship Mode")
        st.plotly_chart(fig_ship, width='stretch')
    
    with col2:
        st.subheader("Profit Margin by Category")
        category_margin = filtered_df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        category_margin['Profit_Margin'] = (category_margin['Profit'] / category_margin['Sales'] * 100)
        fig_margin = px.bar(category_margin, x='Category', y='Profit_Margin',
                          title="Profit Margin by Category (%)",
                          color='Profit_Margin',
                          color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_margin, width='stretch')
    
    # Row 6: Discount Impact
    st.subheader("Discount Impact on Profit")
    discount_impact = filtered_df.groupby(pd.cut(filtered_df['Discount'], 
                                                bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0],
                                                labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50%+'], include_lowest=True), observed=False).agg({
        'Profit': 'mean',
        'Sales': 'sum'
    }).reset_index()
    fig_discount = px.bar(discount_impact, x='Discount', y='Profit',
                         title="Average Profit by Discount Level",
                         color='Profit',
                         color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_discount, width='stretch')
    
    # Data Table
    st.markdown("---")
    st.subheader("Raw Data Preview")
    st.dataframe(filtered_df.head(100))
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please ensure the Excel file is in the DataSet folder.")
