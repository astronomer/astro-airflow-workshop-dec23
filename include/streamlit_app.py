import streamlit as st
import pandas as pd
from datetime import datetime
from snowflake.snowpark.context import get_active_session

session = get_active_session()

enriched_sales_df = session.table("DESIGN_REVIEWS.DEV.ENRICHED_SALES").to_pandas()
revenue_by_appliance_type_df = session.table("DESIGN_REVIEWS.DEV.REVENUE_BY_APPLIANCE_TYPE").to_pandas()
program_analysis_df = session.table("DESIGN_REVIEWS.DEV.PROGRAM_ANALYSIS").to_pandas()
top_users_by_spending_df = session.table("DESIGN_REVIEWS.DEV.TOP_USERS_BY_SPENDING").to_pandas()
appliances_df = session.table("DESIGN_REVIEWS.DEV.APPLIANCES").to_pandas()

enriched_sales_df['SALE_DATE'] = pd.to_datetime(enriched_sales_df['SALE_DATE'])

today = datetime.now().date() 
start_of_month = today.replace(day=1)  
start_of_year = today.replace(month=1, day=1)  

sales_today = enriched_sales_df[enriched_sales_df['SALE_DATE'].dt.date == today]['TOTAL_REVENUE'].sum()
sales_this_month = enriched_sales_df[enriched_sales_df['SALE_DATE'].dt.date >= start_of_month]['TOTAL_REVENUE'].sum()
sales_this_year = enriched_sales_df[enriched_sales_df['SALE_DATE'].dt.date >= start_of_year]['TOTAL_REVENUE'].sum()

latest_sales = enriched_sales_df.sort_values(by='SALE_DATE', ascending=False).head(5)[[
    'SALE_DATE', 'USER_NAME', 'APPLIANCE_NAME', 'QUANTITY', 'TOTAL_REVENUE'
]]

st.set_page_config(page_title="Electrify Everything Sales Dashboard", layout="wide")
st.title("Electrify Everything Sales Dashboard")

st.markdown("## Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Sales So Far Today", value=f"${sales_today:,.2f}")
with col2:
    st.metric(label="Total Sales This Month", value=f"${sales_this_month:,.2f}")
with col3:
    st.metric(label="Total Sales This Year", value=f"${sales_this_year:,.2f}")

st.markdown("---")
st.markdown("## Appliances sold")
st.table(appliances_df[['APPLIANCE_NAME']])

st.markdown("---")
st.markdown("## 🛒 5 Latest Sales")
st.dataframe(latest_sales)

st.markdown("---")
st.markdown("## 📊 Revenue by Appliance Type")
st.bar_chart(revenue_by_appliance_type_df.set_index('APPLIANCE_TYPE')['TOTAL_REVENUE'])

st.markdown("---")
st.markdown("## Discount Program Analysis")
st.bar_chart(program_analysis_df.set_index('PROGRAM')['TOTAL_SAVINGS'])

st.markdown("---")
st.markdown("## 🏆 Top Users by Spending")
st.dataframe(top_users_by_spending_df)

st.markdown("---")
st.markdown("© 2024 Electrify Everything Inc.")
