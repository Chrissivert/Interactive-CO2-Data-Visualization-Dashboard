import streamlit as st
import src.service as s

def display_step_1():
    """Step 1: Allow the user to select the dataset."""
    st.sidebar.header("Step 1: Select Dataset")
    dataset_options = ["Renewable Energy", "CO2 Emissions", "Carbon Tax"]
    selected_column = st.sidebar.selectbox("Select Dataset", dataset_options)

    if selected_column == "Renewable Energy":
        target_column = "Renewables"
    elif selected_column == "CO2 Emissions":
        target_column = "co2_per_capita"
    elif selected_column == "Carbon Tax":
        target_column = "Carbon_tax"

    return target_column

def display_step_2(dataframe):
    """Step 2: Allow the user to filter the selected dataset."""
    st.sidebar.header("Step 2: Filter Data")
    continents = s.get_unique_continents([dataframe])
    countries = s.get_unique_countries([dataframe])

    selected_continent = st.sidebar.selectbox("Select Continent", ["World"] + continents)

    if selected_continent == "World":
        filtered_countries = countries
    else:
        filtered_countries = s.get_countries_by_continent([dataframe], selected_continent)

    selected_country = st.sidebar.multiselect("Select Country", filtered_countries, default=filtered_countries[:2])

    years = s.get_unique_years([dataframe])
    selected_year_range = st.sidebar.slider("Select Year Range", min(years), max(years), (min(years), max(years)))

    return selected_continent, selected_country, selected_year_range
