import streamlit as st
import src.pages.data_exploration
import src.service as s
import src.pages.sidebar as sidebar
from src.heatmap_scatter import HeatmapScatter  # Import the Visualization class

st.set_page_config(
    page_title="Interactive Data Visualization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Interactive Data Visualization Dashboard")

# Map and load datasets
file_mapping = {
    "co2_per_capita": "data/co2-emissions-per-capita.csv",
    "Renewables": "data/renewable-share-energy.csv",
    "Carbon_tax": "data/emissions-weighted-carbon-price.csv",
    "Life_expectancy": "data/life-expectancy.csv",
    "GDP_per_capita": "data/gdp-per-capita-worldbank.csv"
}

dataframes = {name: s.load_default_file(path) for name, path in file_mapping.items()}

# Sidebar step 1: Target column selection
target_column = sidebar.display_step_1()

if target_column in file_mapping:
    current_dataframe = dataframes[target_column]
    st.write(f"Loaded dataset for target column: **{target_column}**")
else:
    st.error(f"No file found for target column: **{target_column}**")
    st.stop()

# Sidebar step 2: Filter by continent, country, year
selected_continent, selected_country, selected_year_range = sidebar.display_step_2(current_dataframe)

# Main page for data exploration
src.pages.data_exploration.page(
    [current_dataframe], selected_continent, selected_country, selected_year_range, target_column
)
# Sidebar: Add checkbox or radio button for choosing the heatmap mode
show_selected_countries_only = st.sidebar.checkbox("Show heatmap for selected countries only", value=True)

# Visualization section
st.header("Additional Visualizations")
viz = HeatmapScatter(dataframes, selected_country, selected_year_range)

# Display heatmap with the user-selected option
st.subheader("Heatmaps")
viz.display_heatmap(show_selected_countries_only=show_selected_countries_only)

st.subheader("Scatterplots")
viz.display_scatterplot()
