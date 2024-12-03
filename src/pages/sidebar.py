import streamlit as st
import src.service as s

def display_step_1():
    """Step 1: Allow the user to select the dataset."""
    st.sidebar.header("Step 1: Select Dataset")
    dataset_options = ["Renewable Energy", "CO2 Emissions", "Carbon Tax", "GDP per capita", "Life Expectancy"]
    selected_column = st.sidebar.selectbox("Select Dataset", dataset_options)

    if selected_column == "Renewable Energy":
        target_column = "Renewables"
    elif selected_column == "CO2 Emissions":
        target_column = "co2_per_capita"
    elif selected_column == "Carbon Tax":
        target_column = "Carbon_tax"
    elif selected_column == "GDP per capita":
        target_column = "GDP_per_capita"
    elif selected_column == "Life Expectancy":
        target_column = "Life_expectancy"
    elif selected_column == "Coal Consumption":
        target_column = "Coal_consumption_per_capita"

    return target_column

def filtering(dataframe):
    st.sidebar.header("Step 2: Filter Data")

    # Filter by continent and country
    continents = s.get_unique_continents([dataframe])
    countries = s.get_unique_countries([dataframe])
    selected_continent = st.sidebar.selectbox("Select Continent", ["World"] + continents)

    if selected_continent == "World":
        filtered_countries = countries
    else:
        filtered_countries = s.get_countries_by_continent([dataframe], selected_continent)

    selected_country = st.sidebar.multiselect("Select Country", filtered_countries, default=filtered_countries[:0])

    # Filter by year range
    years = s.get_unique_years([dataframe])
    selected_year_range = st.sidebar.slider(
        "Select Year Range", 
        min(years), 
        max(years), 
        (min(years), max(years))
    )

    # Filter by additional numerical attributes
    st.sidebar.subheader("Filter by Attributes")

    life_expectancy_min, life_expectancy_max = st.sidebar.slider(
        "Filter Life Expectancy", 
        int(dataframe["Life_expectancy"].min()), 
        int(dataframe["Life_expectancy"].max()), 
        (int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max()))
    )


    co2_min, co2_max = st.sidebar.slider(
    "Filter CO₂ per Capita", 
    int(dataframe["co2_per_capita"].min()), 
    30,  # Hardcode the maximum value to 30
    (int(dataframe["co2_per_capita"].min()), 30)  # Default range from min value to 30
)

    # Apply filters to the dataframe
    filtered_data = dataframe[
        (dataframe["Life_expectancy"] >= life_expectancy_min) & 
        (dataframe["Life_expectancy"] <= life_expectancy_max) &
        (dataframe["co2_per_capita"] >= co2_min) & 
        (dataframe["co2_per_capita"] <= co2_max)
    ]

    if selected_country:
        filtered_data = filtered_data[filtered_data["country"].isin(selected_country)]

    filtered_data = filtered_data[
        (filtered_data["year"] >= selected_year_range[0]) & 
        (filtered_data["year"] <= selected_year_range[1])
    ]

    return (
        filtered_data,
        selected_continent, 
        selected_country, 
        selected_year_range)