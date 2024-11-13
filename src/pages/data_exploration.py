import streamlit as st
import plotly.express as px

import src.service as s

def page(dataframes, selected_countries, selected_year_range):
  st.title("Data Exploration")
  
  tab1, tab2 = st.tabs(["📈 Chart", "📋 Table"])
  for dataframe in dataframes:
    tab1.plotly_chart(chart(dataframe, selected_countries, selected_year_range), use_container_width=True)
    tab2.write(dataframe[dataframe["Entity"].isin(selected_countries)])
  
def chart(dataframe, selected_country, selected_year_range):
  filtered_data = dataframe[(dataframe["Entity"].isin(selected_country)) & (dataframe["Year"] >= selected_year_range[0]) & (dataframe["Year"] <= selected_year_range[1])]
    
  metric_column = s.get_unique_column_names(dataframe)[0]
    
  return px.line(filtered_data, x="Year", y=metric_column, color="Entity", title=f"{metric_column} over time")