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

    # Show/Hide Attributes Button
    show_attributes = st.sidebar.button("Show/Hide Attributes")

    # Use session state to track visibility
    if "attributes_visible" not in st.session_state:
        st.session_state.attributes_visible = False

    if show_attributes:
        st.session_state.attributes_visible = not st.session_state.attributes_visible

    if st.session_state.attributes_visible:
        st.sidebar.subheader("Filter by Attributes")

        # Life Expectancy filter
        life_expectancy_min, life_expectancy_max = st.sidebar.slider(
            "Life Expectancy in years", 
            int(dataframe["Life_expectancy"].min()), 
            int(dataframe["Life_expectancy"].max()), 
            (int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max()))
        )

        # CO₂ per Capita filter
        co2_min, co2_max = st.sidebar.slider(
            "CO₂ per Capita in tonnes", 
            int(dataframe["co2_per_capita"].min()), 
            30,  # Hardcode the maximum value to 30
            (int(dataframe["co2_per_capita"].min()), 30)  # Default range from min value to 30
        )

        # GDP per capita filter
        gdp_min, gdp_max = st.sidebar.slider(
            "GDP per Capita in USD", 
            int(dataframe["GDP_per_capita"].min()), 
            int(dataframe["GDP_per_capita"].max()), 
            (int(dataframe["GDP_per_capita"].min()), int(dataframe["GDP_per_capita"].max()))
        )

        carbon_tax_min, carbon_tax_max = st.sidebar.slider(
            "Carbon Tax ($ per tonne of CO₂ equivalent)", 
            int(dataframe["Carbon_tax"].min()), 
            int(dataframe["Carbon_tax"].max()), 
            (int(dataframe["Carbon_tax"].min()), int(dataframe["Carbon_tax"].max()))
    )

        # Renewables filter
        renewables_min, renewables_max = st.sidebar.slider(
            "Renewables (%)", 
            int(dataframe["Renewables"].min()), 
            int(dataframe["Renewables"].max()), 
            (int(dataframe["Renewables"].min()), int(dataframe["Renewables"].max()))
        )

    else:
        # Default ranges
        life_expectancy_min, life_expectancy_max = int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max())
        co2_min, co2_max = int(dataframe["co2_per_capita"].min()), 30
        gdp_min, gdp_max = int(dataframe["GDP_per_capita"].min()), int(dataframe["GDP_per_capita"].max())
        carbon_tax_min, carbon_tax_max = int(dataframe["Carbon_tax"].min()), int(dataframe["Carbon_tax"].max())
        renewables_min, renewables_max = int(dataframe["Renewables"].min()), int(dataframe["Renewables"].max())

    # Apply filters to the dataframe
    filtered_data = dataframe[
        (dataframe["Life_expectancy"] >= life_expectancy_min) & 
        (dataframe["Life_expectancy"] <= life_expectancy_max) & 
        (dataframe["co2_per_capita"] >= co2_min) & 
        (dataframe["co2_per_capita"] <= co2_max) &
        (dataframe["GDP_per_capita"] >= gdp_min) & 
        (dataframe["GDP_per_capita"] <= gdp_max) &
        (dataframe["Carbon_tax"] >= carbon_tax_min) & 
        (dataframe["Carbon_tax"] <= carbon_tax_max) &
        (dataframe["Renewables"] >= renewables_min) & 
        (dataframe["Renewables"] <= renewables_max)
    ]

    if selected_country:
        filtered_data = filtered_data[filtered_data["country"].isin(selected_country)]

    filtered_data = filtered_data[
        (filtered_data["year"] >= selected_year_range[0]) & 
        (filtered_data["year"] <= selected_year_range[1])
    ]

    # Displaying the current filter ranges
    st.sidebar.write(f"Life Expectancy range: {life_expectancy_min} - {life_expectancy_max} years.")
    st.sidebar.write(f"CO₂ per Capita range: {co2_min} - {co2_max} tons.")
    st.sidebar.write(f"GDP per Capita range: {gdp_min} - {gdp_max} USD.")
    st.sidebar.write(f"Carbon Tax range: {carbon_tax_min} - {carbon_tax_max} USD.")
    st.sidebar.write(f"Renewables range: {renewables_min} - {renewables_max} %.")

    return (
        filtered_data,
        selected_continent, 
        selected_country, 
        selected_year_range
    )
