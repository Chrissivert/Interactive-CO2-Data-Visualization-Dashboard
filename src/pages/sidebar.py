import streamlit as st
import src.service as s

def filtering(dataframe):
    help_button()

    is_filtered = False

    # Initialize session state for selected_country
    # if "selected_country" not in st.session_state:
    #     st.session_state.selected_country = []

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
    # st.session_state.selected_country = [
    #     country for country in st.session_state.selected_country if country in filtered_countries
    # ]

    # Let the user update the selected countries
    selected_country = st.sidebar.multiselect(
        "Select Country",
        filtered_countries,  # Current options
        # default=st.session_state.selected_country  # Default to preserved selections
    )
    # st.session_state.selected_country = selected_country  # Update session state

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

    co2_min, co2_max = st.sidebar.slider(
        "CO₂ per Capita in tonnes", 
        int(dataframe["co2_per_capita"].min()), 
        30,  # Hardcode the maximum value to 30
        (int(dataframe["co2_per_capita"].min()), 30)  # Default range from min value to 30
    )

    st.sidebar.subheader("Filter by Attributes")

    # Add checkboxes to toggle the application of filters
    # apply_life_expectancy = st.sidebar.checkbox("Apply Life Expectancy Filter", value=False)
    # apply_co2 = st.sidebar.checkbox("Apply CO₂ per Capita Filter", value=False)
    # apply_gdp = st.sidebar.checkbox("Apply GDP per Capita Filter", value=False)
    # apply_carbon_tax = st.sidebar.checkbox("Apply Carbon Tax Filter", value=False)
    # apply_renewables = st.sidebar.checkbox("Apply Renewables Filter", value=False)

    # Life Expectancy filter
    apply_life_expectancy = st.sidebar.checkbox("Apply Life Expectancy Filter", value=False)
    if apply_life_expectancy:
        life_expectancy_min, life_expectancy_max = st.sidebar.slider(
            "Life Expectancy in years", 
            int(dataframe["Life_expectancy"].min()), 
            int(dataframe["Life_expectancy"].max()), 
            (int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max()))
        )

    # CO₂ per Capita filter
    # apply_co2 = st.sidebar.checkbox("Apply CO₂ per Capita Filter", value=False)
    # co2_min, co2_max = st.sidebar.slider(
    #     "CO₂ per Capita in tonnes", 
    #     int(dataframe["co2_per_capita"].min()), 
    #     30,  # Hardcode the maximum value to 30
    #     (int(dataframe["co2_per_capita"].min()), 30)  # Default range from min value to 30
    # )

    # GDP per capita filter
    apply_gdp = st.sidebar.checkbox("Apply GDP per Capita Filter", value=False)
    if apply_gdp:
        gdp_min, gdp_max = st.sidebar.slider(
            "GDP per Capita in USD", 
            int(dataframe["GDP_per_capita"].min()), 
            int(dataframe["GDP_per_capita"].max()), 
            (int(dataframe["GDP_per_capita"].min()), int(dataframe["GDP_per_capita"].max()))
        )
        
    # Carbon Tax filter
    apply_carbon_tax = st.sidebar.checkbox("Apply Carbon Tax Filter", value=False)
    if apply_carbon_tax:
        carbon_tax_min, carbon_tax_max = st.sidebar.slider(
            "Carbon Tax ($ per tonne of CO₂ equivalent)", 
            int(dataframe["Carbon_tax"].min()), 
            int(dataframe["Carbon_tax"].max()), 
            (int(dataframe["Carbon_tax"].min()), int(dataframe["Carbon_tax"].max()))
        )

    # Renewables filter
    apply_renewables = st.sidebar.checkbox("Apply Renewables Filter", value=False)
    if apply_renewables:
        renewables_min, renewables_max = st.sidebar.slider(
            "Renewables (%)", 
            int(dataframe["Renewables"].min()), 
            int(dataframe["Renewables"].max()), 
            (int(dataframe["Renewables"].min()), int(dataframe["Renewables"].max()))
        )

    # Apply filters only for selected attributes
    filtered_data = dataframe
    
    is_filtered = True
    filtered_data = filtered_data[(
        filtered_data["co2_per_capita"] >= co2_min) & 
        (filtered_data["co2_per_capita"] <= co2_max)
    ]

    if apply_life_expectancy:
        is_filtered = True
        filtered_data = filtered_data[(
            filtered_data["Life_expectancy"] >= life_expectancy_min) & 
            (filtered_data["Life_expectancy"] <= life_expectancy_max)
        ]

    # is_filtered = True
    # filtered_data = filtered_data[(
    #     filtered_data["co2_per_capita"] >= co2_min) & 
    #     (filtered_data["co2_per_capita"] <= co2_max)
    # ]

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

    return filtered_data, is_filtered, selected_continent, selected_country, selected_year_range

@st.dialog("Help")
def help_dialog():
    st.write("""
        - **Select a country** to get more interactive options and tools.
        - **Filters** are available to refine the data by continent, year, and various attributes.
        - **Charts** will update based on your selected filters and data.
        
        Read about the different charts here:
        """)
    
    with st.expander("Map"):
        st.write("""
            The **Map chart** is the first chart you see when opening the application. It shows a map over the world. This map has a few functions:
            - **Timeline:** Under the map, there is a timeline that users can play and stop as they wish, this provides a viewing opertinuty for users to see how the world (all countries) has developed over the years.
            - **Country Selection:** When choosing a country (or multiple), only the selected countries are highlighted on the map, and only those countries will change over time whilst every other country is white.
            - **Continent Selection:** Unlike the 'Country Selection', this feature allows the map to take forms of continents by choosing the desired continent from the sidebar.
            """)
        
    with st.expander("Pie"):
        st.write("""
                The **Pie-chart** displays the percentage of the average CO2 emissions between selected countries between a selected year-range.
                
                *For example:* The user has selected three countries. Country #1 has 50% emissions, country #2 has 30% emissions, and country #3 has 20% emissions. This means country #1 has as much CO2 emissions has country #2 and #3 combined thoughout the selected year-range.
            """)
        
    with st.expander("Global event"):
        st.write("""
                The **Global event chart** has two main areas of function:
                - **Global Events:** When applying global events, the user can view when the different global events, such as WW1 and WW2, happened and how it effected the CO2 emissions.
                - **Timeline:** Since the x-axis of the chart represents time, this chart will also display the change of the selected countries over the years.
            """)
        
    with st.expander("Predict the future"):
        st.write("""
                The **Predict the future** function displays above the **Global events chart** due to its similarity. Where the only difference is its ability to predict the outcome of the selected years into the future.
                - **Prediction:** Based on the numerical input of the user, the chart will display the estimated prediction of how the chart will behave. The chart will behave based on two different models, based on which model is chosen by the user:
                    - **Linear Regression:** This model will make a linear prediction of the data given to the model.
                    - **Polynomial Features:** This model will make a polynomial prediction of the data given to the model.
                - **Timeline:** Since the x-axis of the chart represents time, this chart will also display the change of the selected countries over the years.
            """)
        
    with st.expander("Correlation Heatmap"):
        st.write("""
                The **Correlation Heatmap**, as the name suggests, shows the correlation of the different attributes. The way to identify the correlation goes as such:
                - The more **blue** the point of intersection is, the higher correlation it is.
                - The more **red** the point of intersection is, the less correlation it is.
                - The lighter the color of the point of intersection is, the more neutral correlation it is.
                 
                **Correlation** shows how two variables are linearly related, meaning they change together at a consistant rate*
            """)
        
    with st.expander("Raw data"):
        st.write("""
                The **Raw data** sections shows all data in a table format. No colors, no major interaction. Just simple, raw data. Here one can view the different attributes the data consists of. E.g. wether is has NA values, or not.
            """)
        
    with st.expander("Scatter plot"):
        st.write("""
                The **Scatter plot** provides the user with the ability to vew the correlation and/or trendline of two selected attributes. Once selected two attributes, a *OLS Trendline* will appear to show the trend between the two features.
                """)
    
def help_button():
    if st.sidebar.button("Need Help❓"):
        help_dialog()
    
    