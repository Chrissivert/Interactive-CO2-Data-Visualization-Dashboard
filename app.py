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

file_mapping = {
    "co2_per_capita": "data/co2-emissions-per-capita.csv",
    "Renewables": "data/renewable-share-energy.csv",
    "Carbon_tax": "data/emissions-weighted-carbon-price.csv",
    "Life_expectancy": "data/life-expectancy.csv",
    "GDP_per_capita": "data/gdp-per-capita-worldbank.csv",
}

dataframes = {name: s.load_default_file(path) for name, path in file_mapping.items()}

merged_dataframe = s.merge_dataframes(dataframes)

target_column =  "co2_per_capita"

filted_dataframe, is_filtered, selected_continent, selected_country, selected_year_range = sidebar.filtering(merged_dataframe)

src.pages.data_exploration.page(
    [filted_dataframe], [merged_dataframe], is_filtered, selected_continent, selected_country, selected_year_range, target_column
)

viz = HeatmapScatter(merged_dataframe, selected_country, selected_year_range)
viz.display_heatmap()
viz.display_scatterplot()
