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

file_mapping = {
    "co2_per_capita": "data/owid-co2-data.csv",
    "Renewables": "data/renewable-share-energy.csv",
    "Carbon_tax": "data/emissions-weighted-carbon-price.csv"
}

default_file_path = "data/owid-co2-data.csv" 
default_dataframe = s.load_default_file(default_file_path)

dataframes = [default_dataframe]
if dataframes:
    selected_continent, selected_country, selected_year_range, target_column = sidebar.display(dataframes)
    
    if target_column in file_mapping:
        file_path = file_mapping[target_column]
        current_dataframe = s.load_default_file(file_path) 
    else:
        current_dataframe = default_dataframe  
        st.warning(f"No specific dataset for target column: **{target_column}**. Using default dataset.")
    
    src.pages.data_exploration.page(
        [current_dataframe], selected_continent, selected_country, selected_year_range, target_column
    )
else:
    st.warning("No datasets available. Please check the default file path.")
