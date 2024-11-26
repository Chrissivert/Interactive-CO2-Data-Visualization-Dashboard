import streamlit as st
import src.pages.data_exploration
import src.service as s
import src.pages.sidebar as sidebar

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

target_column = sidebar.display_step_1()

if target_column in file_mapping:
    file_path = file_mapping[target_column]
    current_dataframe = s.load_default_file(file_path)
    st.write(f"Loaded dataset for target column: **{target_column}**")
else:
    st.error(f"No file found for target column: **{target_column}**")
    st.stop()

selected_continent, selected_country, selected_year_range = sidebar.display_step_2(current_dataframe)

src.pages.data_exploration.page(
    [current_dataframe], selected_continent, selected_country, selected_year_range, target_column
)
