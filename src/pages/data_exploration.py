import streamlit as st
import plotly.express as px
import src.service as s
import numpy as np

def page(dataframes, selected_countries, selected_year_range):
    st.title("Data Exploration")
    
    tab1, tab2 = st.tabs(["📈 Chart", "📋 Table"])
    
    for idx, dataframe in enumerate(dataframes):
        with tab1:
            scale_type = st.radio("Select Y-axis scale", ("Linear", "Logarithmic"), key=f"scale_type_{idx}")
            log_scale = scale_type == "Logarithmic"  
            tab1.plotly_chart(chart(dataframe, selected_countries, selected_year_range, log_scale), use_container_width=True)
        
        with tab2:
            tab2.write(dataframe[dataframe["Entity"].isin(selected_countries)])

def chart(dataframe, selected_country, selected_year_range, log_scale=False):
    filtered_data = dataframe[(dataframe["Entity"].isin(selected_country)) & 
                              (dataframe["Year"] >= selected_year_range[0]) & 
                              (dataframe["Year"] <= selected_year_range[1])]
    
    last_column = filtered_data.columns[-1]
    
    if log_scale:
        filtered_data[last_column] = np.log10(filtered_data[last_column])

    return px.line(filtered_data, 
                   x="Year", 
                   y=last_column, 
                   color="Entity", 
                   title=f"{last_column} over time",
                   log_y=log_scale)  