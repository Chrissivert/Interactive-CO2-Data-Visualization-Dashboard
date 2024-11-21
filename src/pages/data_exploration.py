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
            
            # Fixed the Y-axis column to 'co2_per_capita'
            selected_column = "co2_per_capita"  # This is fixed for the map and chart
            
            # Dropdown for selecting a continent
            continent_options = ["World", "Europe", "Asia", "North America", "South America", "Africa", "Oceania"]
            selected_continent = st.selectbox("Select continent", continent_options, key=f"continent_select_{idx}")
            
            # Plot the choropleth map for the selected continent (animation for the years)
            tab1.plotly_chart(map_chart(dataframe, selected_continent, selected_year_range), use_container_width=True)
            
            # Plot the line chart below the map
            tab1.plotly_chart(chart(dataframe, selected_countries, selected_year_range, selected_column, log_scale), use_container_width=True)
        
        with tab2:
            tab2.write(dataframe[dataframe["country"].isin(selected_countries)])
def chart(dataframe, selected_country, selected_year_range, selected_column, log_scale=False):
    min_year = dataframe["year"].min()
    
    # Filter the data based on selected countries and year range
    filtered_data = dataframe[(dataframe["country"].isin(selected_country)) 
                              & (dataframe["year"] >= selected_year_range[0]) 
                              & (dataframe["year"] <= selected_year_range[1])]

    # Sort the filtered data by year to ensure the x-axis is from low to high
    filtered_data = filtered_data.sort_values(by="year")

    # Create the line chart
    fig = px.line(
        filtered_data, 
        x='year', 
        y=selected_column, 
        color="country", 
        title=f"{selected_column} over time",
        log_y=log_scale
    )
    
    # Add vertical lines for the Paris Agreement and COVID-19 outbreak
    # User checkboxes to enable/disable the lines
    add_paris_agreement_line = st.checkbox("Show Paris Agreement (2015)", value=True)
    add_covid_outbreak_line = st.checkbox("Show COVID-19 Outbreak (2020)", value=True)
    
    if add_paris_agreement_line:
        fig.add_vline(
            x=2015, 
            line=dict(color="blue", dash="dash"), 
            annotation_text="Paris Agreement (2015)", 
            annotation_position="top right"
        )
        
    if add_covid_outbreak_line:
        # If both lines are shown, adjust the annotation position for COVID-19
        annotation_position = "bottom right" if add_paris_agreement_line else "top right"
        fig.add_vline(
            x=2020, 
            line=dict(color="red", dash="dash"), 
            annotation_text="COVID-19 Outbreak (2020)", 
            annotation_position=annotation_position
        )

    return fig



def map_chart(dataframe, selected_continent, selected_year_range):
    # Cap outliers in the existing dataframe
    cap_value = dataframe["co2_per_capita"].quantile(0.98)
    dataframe["co2_per_capita"] = dataframe["co2_per_capita"].clip(upper=cap_value)

    # Filter the dataframe based on the selected year range
    filtered_dataframe = dataframe[(dataframe["year"] >= selected_year_range[0]) & 
                                   (dataframe["year"] <= selected_year_range[1])]

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

    # Create the choropleth map with animation frame for year, using filtered data
    fig = px.choropleth(
        filtered_dataframe,
        locations="country",  # Column with country names
        locationmode="country names",  # Use country names for the map
        color="co2_per_capita",  # The column to use for coloring the countries
        color_continuous_scale="Viridis",  # Color scale from light (low) to dark (high)
        labels={"co2_per_capita": "CO2 per Capita"},
        title="CO2 per Capita over Time",
        hover_name="country",  # Show country name on hover
        hover_data=["co2_per_capita"],  # Show CO2 per capita value on hover
        animation_frame="year",  # Create an animation for the years
        range_color=[0, filtered_dataframe["co2_per_capita"].max()]  # Set the range for color scale based on filtered data
    )

    # Apply the selected continent's scope
    fig.update_geos(
        scope=continent_scope[selected_continent],  # Set the map scope to the selected continent
        showcoastlines=True, 
        coastlinecolor="Black", 
        projection_type="natural earth"
    )

    # Increase the size of the map
    fig.update_layout(
        autosize=True,  # Automatically adjust size
        height=600,  # Set a fixed height for the map (adjust as needed)
        title=dict(font=dict(size=24))  # Increase title font size for better readability
    )

    return fig
