import streamlit as st
import src.pages.data_exploration
import src.service as s
import src.pages.sidebar as sidebar

# Set Streamlit configuration
st.set_page_config(
    page_title="Interactive Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Interactive Data Visualization Dashboard")

# Load the default dataset
default_file_path = "data/owid-co2-data.csv" 
test = "data/renewable-share-energy.csv"
try:
    default_dataframe = s.load_default_file(test)
    st.write(":green[Default dataset loaded successfully!]")  # Inform the user that the dataset is loaded
    dataframes = [default_dataframe]
except FileNotFoundError:
    st.error("Default file not found. Please ensure it exists at the specified path.")
    dataframes = []

if dataframes:
    # Display sidebar for continent, country, and year selection
    selected_continent, selected_country, selected_year_range, target_column = sidebar.display(dataframes)
    
    # Pass selected continent, selected country, selected year range, and target column to the data exploration page
    src.pages.data_exploration.page(dataframes, selected_continent, selected_country, selected_year_range, target_column)
else:
    st.warning("No datasets available. Please check the default file path.")
