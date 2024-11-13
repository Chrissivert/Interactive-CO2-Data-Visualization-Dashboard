import streamlit as st
import plotly.express as px

import service as s

def data_exploration_page(dataframes, selected_country, selected_year_range):
  st.title("Data Exploration")
  for dataframe in dataframes:
    filtered_data = dataframe[(dataframe["Entity"].isin(selected_country)) & (dataframe["Year"] >= selected_year_range[0]) & (dataframe["Year"] <= selected_year_range[1])]
    
    metric_column = s.get_unique_column_names(dataframe)[0]
    
    fig = px.line(filtered_data, x="Year", y=metric_column, color="Entity", title=f"{metric_column} over time")
    
    st.plotly_chart(fig, use_container_width=True)