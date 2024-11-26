import streamlit as st
import src.pages.data_exploration
import src.service as s
import src.pages.sidebar as sidebar

import plotly.graph_objects as go

st.set_page_config(
    page_title="Interactive Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Interactive Data Visualization Dashboard")

default_file_path = "data/owid-co2-data.csv" 
test = "data/renewable-share-energy.csv"
test2 = "data/emissions-weighted-carbon-price.csv"
# try:
default_dataframe = s.load_default_file(default_file_path)
dataframes = [default_dataframe]

if dataframes:
    selected_continent, selected_country, selected_year_range, target_column = sidebar.display(dataframes)
    
    src.pages.data_exploration.page(dataframes, selected_continent, selected_country, selected_year_range, target_column)
else:
    st.warning("No datasets available. Please check the default file path.")
