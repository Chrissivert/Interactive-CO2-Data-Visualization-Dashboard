import streamlit as st
import src.pages.data_exploration
import src.service as s
import src.pages.trend_analysis
import src.page_names as pn
import src.pages.sidebar as sidebar

st.set_page_config(
    page_title="Interactive Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Interactive Data Visualization Dashboard")

default_file_path = "data/owid-co2-data.csv" 
try:
    default_dataframe = s.load_default_file(default_file_path)
    st.write(":green[Default dataset loaded successfully!]")
    dataframes = [default_dataframe]
except FileNotFoundError:
    st.error("Default file not found. Please ensure it exists at the specified path.")
    dataframes = []

if dataframes:
    page, selected_country, selected_year_range = sidebar.display(dataframes)

    match page:
        case pn.Pages.DATA_EXPLORATION.value:
            src.pages.data_exploration.page(dataframes, selected_country, selected_year_range)
        
        case pn.Pages.TREND_ANALYSIS.value:
            src.pages.trend_analysis.page(s.get_metrics(dataframes), selected_country, selected_year_range)
else:
    st.warning("No datasets available. Please check the default file path.")
