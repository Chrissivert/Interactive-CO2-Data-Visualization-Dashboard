import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from src.future_prediction import FuturePrediction
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor

def page(dataframes, selected_continent, selected_countries, selected_year_range, target_column):
    
    for idx, dataframe in enumerate(dataframes):
        col1, col2 = st.columns([2, 1])  
        
        with col1:
            map_fig, pie_fig = map_chart(dataframe, selected_continent, selected_year_range, selected_countries, target_column)
            st.plotly_chart(map_fig, use_container_width=True)
        
        with col2:
            st.plotly_chart(pie_fig, use_container_width=True)
            
        col_y_axis, col_chart = st.columns([1,5])
        
        with col_y_axis:
            scale_type = st.radio("Select Y-axis scale", ("Linear", "Logarithmic"), key=f"scale_type_{idx}")
            log_scale = scale_type == "Logarithmic"
            
            advanced_settings = st.checkbox("Advanced Settings")
            
            if (advanced_settings):
                years_to_predict = st.number_input("Insert the number of years to predict into the future", value=5, min_value=1)
                
        with col_chart:
            if advanced_settings:
                # st.header("Future Predictions")
    
                # years_to_predict = st.number_input("Insert the number of years to predict into the future", 
                #                                 value=5, min_value=1)
                
                future_prediction = FuturePrediction(
                    selected_countries=selected_countries,
                    years_to_predict=years_to_predict,
                    scale_type=log_scale,
                    dataframe=dataframes[0]
                    # target_column=target_column  # Pass the target_column here
                )
                
                # Create tabs for different prediction models
                tab1, tab2, tab3 = st.tabs(["Linear Regression", "Polynomial Features", "Random Forest Regressor"])
                
                # Generate predictions for each model
                future_prediction.plot(tab1, LinearRegression())
                future_prediction.plot(tab2, make_pipeline(PolynomialFeatures(degree=10), LinearRegression()))
                future_prediction.plot(tab3, RandomForestRegressor(n_estimators=100, random_state=42))
            else:
                st.plotly_chart(chart(dataframe, selected_countries, selected_year_range, target_column, log_scale), use_container_width=True)


def chart(dataframe, selected_country, selected_year_range, target_column, log_scale=False):
    filtered_data = dataframe[(dataframe["country"].isin(selected_country)) 
                              & (dataframe["year"] >= selected_year_range[0]) 
                              & (dataframe["year"] <= selected_year_range[1])]

    # Sort the filtered data by year to ensure the x-axis is from low to high
    filtered_data = filtered_data.sort_values(by="year")

    # Create the line chart
    fig = px.line(
        filtered_data, 
        x='year', 
        y=target_column,  # Use target_column instead of hardcoding the column name
        color="country", 
        title=f"{target_column} over time",
        log_y=log_scale
    )
    
    # Add vertical lines for the Paris Agreement and COVID-19 outbreak
    with st.expander("View When Different Global Events Happened:"):
        col11, col12, col13, col14, col15 = st.columns([1,1,1,1,1])
        add_paris_agreement_line = col11.checkbox("Show Paris Agreement", value=True)
        add_covid_outbreak_line = col12.checkbox("Show COVID-19 Outbreak", value=True)
        add_world_war_two_lines = col13.checkbox("Show WW2 Start & End", value=False)
        add_world_war_one_lines = col14.checkbox("Show WW1 Start & End", value=False)
        add_the_great_depression = col15.checkbox("Show The Great Depression Start", value=False)
        
        col21, col22, col23, col24, col25 = st.columns([1,1,1,1,1])
        add_dissolution_of_the_soviet_union = col21.checkbox("Show the Dissolution of the Soviet Union", value=False)
        add_first_man_in_space = col22.checkbox("Show First Man in Space")
        
    if add_first_man_in_space:
        fig.add_vline(
            x=1961, 
            line=dict(color="red", dash="dash"), 
            annotation_text="First Man in Space (1961)", 
            annotation_position="bottom right"
        )
        
    if add_dissolution_of_the_soviet_union:
        fig.add_vline(
            x=1991, 
            line=dict(color="red", dash="dash"), 
            annotation_text="Dissolution of the Soviet Union (1991)", 
            annotation_position="top right"
        )
        
    if add_paris_agreement_line:
        fig.add_vline(
            x=2015, 
            line=dict(color="yellow", dash="dash"), 
            annotation_text="Paris Agreement (2015)", 
            annotation_position="top right"
        )
        
    if add_covid_outbreak_line:
        annotation_position = "bottom right" if add_paris_agreement_line else "top right"
        fig.add_vline(
            x=2019, 
            line=dict(color="red", dash="dash"), 
            annotation_text="COVID-19 Outbreak (2019)", 
            annotation_position=annotation_position
        )
        
    if add_world_war_two_lines:
        # annotation_position = "bottom left" if add_world_war_two_line else "top right"
        fig.add_vline(
            x=1939, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW2 Start Point (1939)", 
            annotation_position="bottom left" if add_world_war_two_lines else "top left"
        )
        fig.add_vline(
            x=1945, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW2 End Point (1945)", 
            annotation_position="bottom right" if add_world_war_two_lines else "top right"
        )
        
    if add_world_war_one_lines:
        fig.add_vline(
            x=1914, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW1 Start Point (1914)", 
            annotation_position="top left" if add_world_war_two_lines else "bottom left"
        )
        fig.add_vline(
            x=1918, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW1 End Point (1918)", 
            annotation_position="top right" if add_world_war_two_lines else "bottom right"
        )
        
    if add_the_great_depression:
        fig.add_vline(
            x=1929, 
            line=dict(color="blue", dash="dash"), 
            annotation_text="The Great Depression (1929)"
            # annotation_position="bottom left" if add_world_war_two_lines else "top left"
        )

    return fig

def map_chart(dataframe, selected_continent, selected_year_range, selected_countries, target_column):
    # Cap outliers in the existing dataframe
    cap_value = dataframe[target_column].quantile(0.98)
    dataframe[target_column] = dataframe[target_column].clip(upper=cap_value)

    # Filter the dataframe based on the selected year range
    filtered_dataframe = dataframe[(dataframe["year"] >= selected_year_range[0]) & 
                                   (dataframe["year"] <= selected_year_range[1])]

    # Filter further for the selected countries
    filtered_countries_df = filtered_dataframe[filtered_dataframe["country"].isin(selected_countries)]
    
    # Aggregate data for the selected countries for the given year
    data_by_country = filtered_countries_df.groupby("country")[target_column].mean().reset_index()
    
    # Calculate percentage of total for each country
    total_data = data_by_country[target_column].sum()
    data_by_country["percentage"] = (data_by_country[target_column] / total_data) * 100

    # Create the pie chart
    pie_fig = px.pie(
        data_by_country, 
        names="country", 
        values="percentage", 
        title=f"{target_column} (Average from {selected_year_range[0]} to {selected_year_range[1]})",
        labels={"percentage": f"{target_column} (%)"}
    )

    # Set up the map's continent scope
    continent_scope = {
        "World": "world",
        "Europe": "europe",
        "Asia": "asia",
        "North America": "north america",
        "South America": "south america",
        "Africa": "africa",
        "Oceania": "oceania"
    }

    # Create the choropleth map
    map_fig = px.choropleth(
        filtered_dataframe,
        locations="country",  # Column with country names
        locationmode="country names",  # Use country names for the map
        color=target_column,  # Use target_column for coloring the countries
        color_continuous_scale="Viridis",  # Color scale from light (low) to dark (high)
        labels={target_column: f"{target_column} per Capita"},
        title=f"{target_column} Map Over Time",
        hover_name="country",  # Show country name on hover
        hover_data=[target_column],  # Show data for target_column on hover
        animation_frame="year",  # Create an animation for the years
        range_color=[0, filtered_dataframe[target_column].max()]  # Set the range for color scale based on filtered data
    )

    # Apply the selected continent's scope
    map_fig.update_geos(
        scope=continent_scope[selected_continent],  # Set the map scope to the selected continent
        showcoastlines=True, 
        coastlinecolor="Black",
        projection_type="natural earth",
    )

    # Increase the size of the map
    map_fig.update_layout(
        autosize=True,  # Automatically adjust size
        height=600,  # Set a fixed height for the map (adjust as needed)
        title=dict(font=dict(size=24))  # Increase title font size for better readability
    )

    return map_fig, pie_fig
