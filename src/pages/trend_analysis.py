import streamlit as st
import pandas as pd
import plotly.express as px
import flag
import requests

# Function to get the flag URL
def get_flag_url(iso_code):
    return f"https://flagcdn.com/w320/{iso_code.lower()}.png"

def page(metrics, selected_country, selected_year_range):
    st.title("Trend Analysis")
    if len(metrics) >= 2:
        st.header("Select Metrics for Comparison")

        col1, col2 = st.columns(2)
        metric1_label = col1.selectbox("Select Metric for the X-Axis", list(metrics.keys()), key="metric1")
        metric2_label = col2.selectbox("Select Metric for the Y-Axis", list(metrics.keys()), key="metric2")

        df1, metric1 = metrics[metric1_label]
        df2, metric2 = metrics[metric2_label]

        df1_filtered = df1[(df1["Entity"].isin(selected_country)) & 
                           (df1["Year"] >= selected_year_range[0]) & 
                           (df1["Year"] <= selected_year_range[1])][["Entity", "Year", "Code", metric1]]

        df2_filtered = df2[(df2["Entity"].isin(selected_country)) & 
                           (df2["Year"] >= selected_year_range[0]) & 
                           (df2["Year"] <= selected_year_range[1])][["Entity", "Year", "Code", metric2]]

        merged_df = pd.merge(df1_filtered, df2_filtered, on=["Entity", "Year", "Code"], how="inner")

        selected_country_codes = dict(merged_df[['Entity', 'Code']].drop_duplicates().assign(
        Code=lambda df: df['Code'].str[:2].str.upper()).values)

        if not merged_df.empty:
            for country, iso_code in selected_country_codes.items():
                country_data = merged_df[merged_df["Entity"] == country]
                flag_url = get_flag_url(iso_code)  # Fetch flag URL


                fig = px.scatter(
                    country_data,
                    x=metric1,
                    y=metric2,
                    trendline="ols",
                    title=f"{metric1} vs {metric2} for {country}",
                    labels={metric1: metric1, metric2: metric2}
                )
                fig.update_traces(
                    line=dict(color="green"),
                    selector=dict(mode="lines")
                )
                fig.update_traces(mode="lines")
                st.write(f'<span style="display: inline-block; font-weight: bold;">{country}</span> <img src="{flag_url}" width="40" style="vertical-align: middle;">', unsafe_allow_html=True)
                
                st.plotly_chart(fig, use_container_width=True)
