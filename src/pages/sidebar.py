import streamlit as st
import src.service as s

def display(dataframes):
    # Get continents and countries
    continents = s.get_unique_continents(dataframes)  # Assuming this function exists
    countries = s.get_unique_countries(dataframes)

    # Sidebar for continent selection
    st.sidebar.header("Filter Data")
    selected_continent = st.sidebar.selectbox("Select Continent", ["World"] + continents)

    # Filter countries based on selected continent
    if selected_continent == "World":
        filtered_countries = countries
    else:
        filtered_countries = s.get_countries_by_continent(dataframes, selected_continent)

    # Sidebar for country and year selection
    selected_country = st.sidebar.multiselect("Select Country", filtered_countries, default=filtered_countries[:2])

    years = s.get_unique_years(dataframes)
    selected_year_range = st.sidebar.slider("Select Year Range", min(years), max(years), (min(years), max(years)))

    # Sidebar for selecting the target column based on the dataset
    dataset_options = ["Renewable Energy", "CO2 Emissions"]
    selected_dataset = st.sidebar.selectbox("Select Dataset", dataset_options)

    # Define the target column based on dataset selection
    if selected_dataset == "Renewable Energy":
        target_column = "Renewables"  # Assuming 'Renewables' is the column name in the renewable dataset
    elif selected_dataset == "CO2 Emissions":
        target_column = "co2_per_capita"  # Assuming 'co2_per_capita' is the column name in the CO2 dataset

    # Return selected continent, countries, year range, and target column
    return selected_continent, selected_country, selected_year_range, target_column
