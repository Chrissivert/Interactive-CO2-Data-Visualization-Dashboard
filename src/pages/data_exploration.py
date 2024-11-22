import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from src.future_prediction import FuturePrediction
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor

def page(dataframes, selected_continent, selected_countries, selected_year_range, target_column):
    st.title("Data Exploration")
    
    # Existing chart and table tabs
    tab1, tab2 = st.tabs(["📈 Chart", "📋 Table"])
    
    for idx, dataframe in enumerate(dataframes):
        with tab1:
            # Create a two-column layout for map and pie chart
            col1, col2 = st.columns([2, 1])  # Adjust the width ratio as needed
            
            # Map chart in the first column
            with col1:
                map_fig, pie_fig = map_chart(dataframe, selected_continent, selected_year_range, selected_countries, target_column)
                st.plotly_chart(map_fig, use_container_width=True)

                # Move the scale type selection beneath the map
                scale_type = st.radio("Select Y-axis scale", ("Linear", "Logarithmic"), key=f"scale_type_{idx}")
                log_scale = scale_type == "Logarithmic"
            
            # Pie chart in the second column
            with col2:
                st.plotly_chart(pie_fig, use_container_width=True)

            # Line chart below the map and pie chart
            st.plotly_chart(chart(dataframe, selected_countries, selected_year_range, target_column, log_scale), use_container_width=True)
        
        with tab2:
            st.write(dataframe[dataframe["country"].isin(selected_countries)])

    # Future Predictions Section
    st.header("Future Predictions")
    
    years_to_predict = st.number_input("Insert the number of years to predict into the future", 
                                       value=5, min_value=1)
    
    future_prediction = FuturePrediction(
        selected_countries=selected_countries,
        years_to_predict=years_to_predict,
        scale_type=st.radio("Select Y-axis scale for prediction", ("Linear", "Logarithmic")),
        dataframe=dataframes[0],
        target_column=target_column  # Pass the target_column here
    )
    
    # Create tabs for different prediction models
    tab1, tab2, tab3 = st.tabs(["Linear Regression", "Polynomial Features", "Random Forest Regressor"])
    
    # Generate predictions for each model
    future_prediction.plot(tab1, LinearRegression())
    future_prediction.plot(tab2, make_pipeline(PolynomialFeatures(degree=10), LinearRegression()))
    future_prediction.plot(tab3, RandomForestRegressor(n_estimators=100, random_state=42))

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
        annotation_position = "bottom right" if add_paris_agreement_line else "top right"
        fig.add_vline(
            x=2020, 
            line=dict(color="red", dash="dash"), 
            annotation_text="COVID-19 Outbreak (2020)", 
            annotation_position=annotation_position
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
        title=f"{target_column} per Capita over Time",
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
        projection_type="natural earth"
    )

    # Increase the size of the map
    map_fig.update_layout(
        autosize=True,  # Automatically adjust size
        height=600,  # Set a fixed height for the map (adjust as needed)
        title=dict(font=dict(size=24))  # Increase title font size for better readability
    )

    return map_fig, pie_fig
