import streamlit as st
import plotly.express as px
import numpy as np

def page(dataframes, selected_countries, selected_year_range):
    st.title("Data Exploration")
    
    tab1, tab2 = st.tabs(["📈 Chart", "📋 Table"])
    
    for idx, dataframe in enumerate(dataframes):
        with tab1:
            scale_type = st.radio("Select Y-axis scale", ("Linear", "Logarithmic"), key=f"scale_type_{idx}")
            log_scale = scale_type == "Logarithmic"
            
            # Fix the Y-axis column to 'co2_per_capita'
            selected_column = "co2_per_capita"  # This is fixed for the map and chart
            
            # Dropdown for selecting a continent
            continent_options = ["World", "Europe", "Asia", "North America", "South America", "Africa", "Oceania"]
            selected_continent = st.selectbox("Select continent", continent_options, key=f"continent_select_{idx}")
            
            # Create the line chart to select the year
            years = dataframe["year"].unique()
            selected_year = st.slider(
                "Select year for map visualization",
                min_value=min(years),
                max_value=max(years),
                value=min(years),
                step=1
            )
            
            # Plot the choropleth map for the selected year
            tab1.plotly_chart(map_chart(dataframe, selected_year, selected_continent), use_container_width=True)
            
            # Plot the line chart below the map
            tab1.plotly_chart(chart(dataframe, selected_countries, selected_year_range, selected_column, log_scale), use_container_width=True)
        
        with tab2:
            tab2.write(dataframe[dataframe["country"].isin(selected_countries)])

def chart(dataframe, selected_country, selected_year_range, selected_column, log_scale=False):
    # Filter the data based on selected countries and year range
    filtered_data = dataframe[(dataframe["country"].isin(selected_country)) 
                              & (dataframe["year"] >= selected_year_range[0]) 
                              & (dataframe["year"] <= selected_year_range[1])]
    
    # Apply logarithmic scale if selected
    if log_scale:
        filtered_data[selected_column] = np.log10(filtered_data[selected_column])

    # Create and return the line chart
    return px.line(
        filtered_data, 
        x="year", 
        y=selected_column, 
        color="country", 
        title=f"{selected_column} over time",
        log_y=log_scale
    )

def map_chart(dataframe, selected_year, selected_continent):
    # Filter the dataframe for the selected year
    year_data = dataframe[dataframe["year"] == selected_year]
    
    # Set the scope based on the selected continent
    continent_scope = {
        "World": "world",
        "Europe": "europe",
        "Asia": "asia",
        "North America": "north america",
        "South America": "south america",
        "Africa": "africa",
        "Oceania": "oceania"
    }
    
    # Create the choropleth map with the specified scope
    fig = px.choropleth(
        year_data,
        locations="country",  # Column with country names
        locationmode="country names",  # Use country names for the map
        color="co2_per_capita",  # The column to use for coloring the countries
        color_continuous_scale="Viridis",  # Color scale from light (low) to dark (high)
        labels={"co2_per_capita": "CO2 per Capita"},
        title=f"CO2 per Capita for {selected_year}",
        hover_name="country",  # Show country name on hover
        hover_data=["co2_per_capita"],  # Show CO2 per capita value on hover
    )
    
    # Apply the selected continent's scope
    fig.update_geos(
        scope=continent_scope[selected_continent],  # Set the map scope to the selected continent
        showcoastlines=True, 
        coastlinecolor="Black", 
        projection_type="natural earth"
    )
    
    return fig
