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
    is_filtered = False

    # Initialize session state for selected_country
    if "selected_country" not in st.session_state:
        st.session_state.selected_country = []

    # Filter by continent and country
    continents = s.get_unique_continents([dataframe])
    countries = s.get_unique_countries([dataframe])
    selected_continent = st.sidebar.selectbox("Select Continent", ["World"] + continents)

    # Update the list of filtered countries based on the selected continent
    if selected_continent == "World":
        filtered_countries = countries
    else:
        filtered_countries = s.get_countries_by_continent([dataframe], selected_continent)

    # Preserve previously selected countries if still in the filtered list
    st.session_state.selected_country = [
        country for country in st.session_state.selected_country if country in filtered_countries
    ]

    # Let the user update the selected countries
    selected_country = st.sidebar.multiselect(
        "Select Country",
        filtered_countries,  # Current options
        default=st.session_state.selected_country  # Default to preserved selections
    )
    st.session_state.selected_country = selected_country  # Update session state

    if not selected_country:
        st.info("Select a country to unlock more interaction tools!")

    # Filter by year range
    years = s.get_unique_years([dataframe])
    selected_year_range = st.sidebar.slider(
        "Select Year Range", 
        min(years), 
        max(years), 
        (min(years), max(years))
    )

    # Default filter values (set initial values)
    apply_life_expectancy = False
    apply_co2 = False
    apply_gdp = False
    apply_carbon_tax = False
    apply_renewables = False

    life_expectancy_min, life_expectancy_max = int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max())
    co2_min, co2_max = int(dataframe["co2_per_capita"].min()), 30  # Set hardcoded max for CO2
    gdp_min, gdp_max = int(dataframe["GDP_per_capita"].min()), int(dataframe["GDP_per_capita"].max())
    carbon_tax_min, carbon_tax_max = int(dataframe["Carbon_tax"].min()), int(dataframe["Carbon_tax"].max())
    renewables_min, renewables_max = int(dataframe["Renewables"].min()), int(dataframe["Renewables"].max())

    st.sidebar.subheader("Filter by Attributes")

    # Add checkboxes to toggle the application of filters
    apply_life_expectancy = st.sidebar.checkbox("Apply Life Expectancy Filter", value=False)
    apply_co2 = st.sidebar.checkbox("Apply CO₂ per Capita Filter", value=False)
    apply_gdp = st.sidebar.checkbox("Apply GDP per Capita Filter", value=False)
    apply_carbon_tax = st.sidebar.checkbox("Apply Carbon Tax Filter", value=False)
    apply_renewables = st.sidebar.checkbox("Apply Renewables Filter", value=False)

    # Life Expectancy filter
    if apply_life_expectancy:
        life_expectancy_min, life_expectancy_max = st.sidebar.slider(
            "Life Expectancy in years", 
            int(dataframe["Life_expectancy"].min()), 
            int(dataframe["Life_expectancy"].max()), 
            (int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max()))
        )

    # CO₂ per Capita filter
    if apply_co2:
        co2_min, co2_max = st.sidebar.slider(
            "CO₂ per Capita in tonnes", 
            int(dataframe["co2_per_capita"].min()), 
            30,  # Hardcode the maximum value to 30
            (int(dataframe["co2_per_capita"].min()), 30)  # Default range from min value to 30
        )

    # GDP per capita filter
    if apply_gdp:
        gdp_min, gdp_max = st.sidebar.slider(
            "GDP per Capita in USD", 
            int(dataframe["GDP_per_capita"].min()), 
            int(dataframe["GDP_per_capita"].max()), 
            (int(dataframe["GDP_per_capita"].min()), int(dataframe["GDP_per_capita"].max()))
        )

    # Carbon Tax filter
    if apply_carbon_tax:
        carbon_tax_min, carbon_tax_max = st.sidebar.slider(
            "Carbon Tax ($ per tonne of CO₂ equivalent)", 
            int(dataframe["Carbon_tax"].min()), 
            int(dataframe["Carbon_tax"].max()), 
            (int(dataframe["Carbon_tax"].min()), int(dataframe["Carbon_tax"].max()))
        )

    # Renewables filter
    if apply_renewables:
        renewables_min, renewables_max = st.sidebar.slider(
            "Renewables (%)", 
            int(dataframe["Renewables"].min()), 
            int(dataframe["Renewables"].max()), 
            (int(dataframe["Renewables"].min()), int(dataframe["Renewables"].max()))
        )

    # Apply filters only for selected attributes
    filtered_data = dataframe

    if apply_life_expectancy:
        is_filtered = True
        filtered_data = filtered_data[(
            filtered_data["Life_expectancy"] >= life_expectancy_min) & 
            (filtered_data["Life_expectancy"] <= life_expectancy_max)
        ]

    if apply_co2:
        is_filtered = True
        filtered_data = filtered_data[(
            filtered_data["co2_per_capita"] >= co2_min) & 
            (filtered_data["co2_per_capita"] <= co2_max)
        ]

    if apply_gdp:
        is_filtered = True
        filtered_data = filtered_data[(
            filtered_data["GDP_per_capita"] >= gdp_min) & 
            (filtered_data["GDP_per_capita"] <= gdp_max)
        ]

    if apply_carbon_tax:
        is_filtered = True
        filtered_data = filtered_data[(
            filtered_data["Carbon_tax"] >= carbon_tax_min) & 
            (filtered_data["Carbon_tax"] <= carbon_tax_max)
        ]

    if apply_renewables:
        is_filtered = True
        filtered_data = filtered_data[(
            filtered_data["Renewables"] >= renewables_min) & 
            (filtered_data["Renewables"] <= renewables_max)
        ]

    # Apply country and year filters
    if selected_country:
        filtered_data = filtered_data[filtered_data["country"].isin(selected_country)]

    filtered_data = filtered_data[(
        filtered_data["year"] >= selected_year_range[0]) & 
        (filtered_data["year"] <= selected_year_range[1])
    ]
    help_button()

    return filtered_data, is_filtered, selected_continent, selected_country, selected_year_range

def help_button():
    with st.sidebar.expander("Need Help? ❓"):
        st.write("""
            ### Help Information:
            - **Select a country** to get more interactive options and tools.
            - **Filters** are available to refine the data by continent, year, and various attributes.
            - **Charts** will update based on your selected filters and data.
        """)