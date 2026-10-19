import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="AI Powered Data Analyst Dashboard", layout="wide")
st.title("📊 AI Data Analytics & Insights Dashboard")

# 1. Data Upload
uploaded_file = st.sidebar.file_uploader("Apni CSV File Upload Karein", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # 2. Data Cleaning & Preview
    st.subheader("1. Raw Data & Cleaning")
    if st.checkbox("Show Raw Data"):
        st.dataframe(df.head())
        
    st.write(f"**Total Rows:** {df.shape[0]} | **Total Columns:** {df.shape[1]}")
    
    # Handling Missing Values
    if df.isnull().sum().sum() > 0:
        st.warning("Data me missing values hain. Cleaning in progress...")
        df = df.fillna(method='ffill').fillna(method='bfill')
        st.success("Missing values fix ho chuki hain!")

    # 3. Automated KPI Summary
    st.subheader("2. Key Metrics & Summary")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if numeric_cols:
        col1, col2, col3 = st.columns(3)
        col1.metric("Select Metric Total", f"{df[numeric_cols[0]].sum():,.2f}")
        col2.metric("Average Value", f"{df[numeric_cols[0]].mean():,.2f}")
        col3.metric("Max Value", f"{df[numeric_cols[0]].max():,.2f}")

    # 4. Interactive Visualizations
    st.subheader("3. Data Visualizations")
    col_left, col_right = st.columns(2)

    with col_left:
        if numeric_cols and categorical_cols:
            fig_bar = px.bar(df, x=categorical_cols[0], y=numeric_cols[0], title=f"{numeric_cols[0]} by {categorical_cols[0]}", color=categorical_cols[0])
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        if len(numeric_cols) >= 2:
            fig_scatter = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
            st.plotly_chart(fig_scatter, use_container_width=True)

    # 5. AI Prompt Generator for Client Report
    st.subheader("4. AI Executive Summary (Client Report)")
    st.info("Niche diye gaye summary text ko copy karke ChatGPT / Claude me daalein aur client-ready insight report paayein:")
    
    summary_text = f"Dataset Summary:\nTotal Records: {len(df)}\nColumns: {list(df.columns)}\nStatistical Summary:\n{df.describe().to_string()}"
    st.code(summary_text, language="text")

else:
    st.info("👈 Dashboard test karne ke liye left sidebar se koi bhi CSV file upload karein.")