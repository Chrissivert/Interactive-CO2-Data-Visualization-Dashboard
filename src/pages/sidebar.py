import streamlit as st
import src.service as s

def filtering(dataframe):
    help_button()

    is_filtered = False

    continents = s.get_unique_continents([dataframe])
    countries = s.get_unique_countries([dataframe])
    selected_continent = st.sidebar.selectbox("Select Continent", ["World"] + continents)

    if selected_continent == "World":
        filtered_countries = countries
    else:
        filtered_countries = s.get_countries_by_continent([dataframe], selected_continent)

    selected_country = st.sidebar.multiselect(
        "Select Country",
        filtered_countries,  
    )

    if not selected_country:
        st.info("Select a country to unlock more interaction tools!")

    years = s.get_unique_years([dataframe])
    selected_year_range = st.sidebar.slider(
        "Select Year Range", 
        min(years), 
        max(years), 
        (min(years), max(years))
    )

    apply_life_expectancy = False
    apply_gdp = False
    apply_carbon_tax = False
    apply_renewables = False

    life_expectancy_min, life_expectancy_max = int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max())
    co2_min, co2_max = int(dataframe["co2_per_capita"].min()), 30  
    gdp_min, gdp_max = int(dataframe["GDP_per_capita"].min()), int(dataframe["GDP_per_capita"].max())
    carbon_tax_min, carbon_tax_max = int(dataframe["Carbon_tax"].min()), int(dataframe["Carbon_tax"].max())
    renewables_min, renewables_max = int(dataframe["Renewables"].min()), int(dataframe["Renewables"].max())

    co2_min, co2_max = st.sidebar.slider(
        "CO₂ per Capita in tonnes", 
        int(dataframe["co2_per_capita"].min()), 
        30,  
        (int(dataframe["co2_per_capita"].min()), 30) 
    )

    st.sidebar.subheader("Filter by Attributes")

    # Life Expectancy filter
    apply_life_expectancy = st.sidebar.checkbox("Apply Life Expectancy Filter", value=False)
    if apply_life_expectancy:
        life_expectancy_min, life_expectancy_max = st.sidebar.slider(
            "Life Expectancy in years", 
            int(dataframe["Life_expectancy"].min()), 
            int(dataframe["Life_expectancy"].max()), 
            (int(dataframe["Life_expectancy"].min()), int(dataframe["Life_expectancy"].max()))
        )

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
            "Carbon Tax (USD per tonne of CO₂ equivalent)", 
            int(dataframe["Carbon_tax"].min()), 
            int(dataframe["Carbon_tax"].max()), 
            (int(dataframe["Carbon_tax"].min()), int(dataframe["Carbon_tax"].max()))
        )

    # Renewables filter
    apply_renewables = st.sidebar.checkbox("Apply Renewables Filter", value=False)
    if apply_renewables:
        renewables_min, renewables_max = st.sidebar.slider(
            "Renewables (%) (proportion of the total energy consumed by a country, that comes from renewable energy sources in %)", 
            int(dataframe["Renewables"].min()), 
            int(dataframe["Renewables"].max()), 
            (int(dataframe["Renewables"].min()), int(dataframe["Renewables"].max()))
        )

    filtered_data = dataframe
    
    is_filtered = False
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
            The **Map** chart is the first visualization you'll see when opening the application. It shows a world map with various features:
            - **Timeline:** The timeline below the map lets users start or stop to view how CO₂ emissions evolves over time across all countries.
            - **Country Selection:** Selecting countries or multiple countries highlights them on the map, showing only their data during the selected time.
            - **Continent Selection:** You can also choose to view data by continent, enabling a broader geographical focus.
        """)

    with st.expander("Pie"):
        st.write("""
            The **Pie Chart** displays the proportion of total CO₂ emissions from selected countries within a specified year range.
            It illustrates the distribution of CO₂ emissions per capita as a percentage of total emissions, averaged across the selected years for the chosen countries.
        """)

        

    with st.expander("Global Event"):
        st.write("""
            The **Global Events** overlays global events (such as WW1 and WW2) on the timeline, showing how CO₂ emissions changed during those events.
        """)

    with st.expander("Predict the Future"):
        st.write("""
            The **Predict the Future** feature allows you to forecast future CO₂ emissions based on historical data. The chart will display predictions using one of two models:
            - **Linear Regression:** A linear approach to predict trends based on past data.
            - **Polynomial Features:** A more flexible approach that fits a polynomial model to the data for potentially more accurate future predictions.
        """)

    with st.expander("Correlation Heatmap"):
        st.write("""
            The **Correlation Heatmap** shows the relationship between different attributes in the dataset:
            - **Darker Blue** represents a strong positive correlation, indicating that as one variable increases, the other increases as well.
            - **Darker Red** represents a strong negative correlation, where an increase in one variable leads to a decrease in the other.
            - **Lighter Colors** show a weaker or neutral correlation, where changes in one variable do not predict significant changes in the other.

            Correlation values range from **+1** (strong positive) to **-1** (strong negative), with **0** indicating no linear relationship.
        """)

    with st.expander("Raw Data"):
        st.write("""
            The **Raw Data** section provides a simple table of all the data without any interactive features. This allows users to view the underlying dataset, including any missing (NA) values and other raw information.
        """)

    with st.expander("Scatter Plot"):
        st.write("""
            The **Scatter Plot** shows the relationship between two selected attributes. Once you select two variables, the plot will display the relationship between them and indicate the trend between the attributes.
        """)

def help_button():
    if st.sidebar.button("Need Help❓"):
        help_dialog()
    
    