import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from src.future_prediction import FuturePrediction
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]

def page(filtered_dataframe, merged_dataframe, is_filtered, selected_continent, selected_countries, selected_year_range, target_column):
    for idx, (dataframe, merged_dataframe) in enumerate(zip(filtered_dataframe, merged_dataframe)):
        
        if len(selected_countries) == 0:
            map_fig = map_chart(merged_dataframe, dataframe, is_filtered, selected_continent, selected_year_range, selected_countries, target_column)
            if map_fig is None:
                    return
            st.plotly_chart(map_fig, use_container_width=True)
        else:
            col1, col2 = st.columns([4, 2])
            
            with col1:
                map_fig = map_chart(merged_dataframe, dataframe, is_filtered, selected_continent, selected_year_range, selected_countries, target_column)

                if map_fig is None:
                    return
                st.plotly_chart(map_fig, use_container_width=True)
            
            with col2:
                pie_fig = pie_chart(dataframe, selected_year_range, is_filtered, selected_countries, target_column)
                st.plotly_chart(pie_fig, use_container_width=True)
            
            col_y_axis, col_chart = st.columns([1, 5])
            
            with col_y_axis:
                scale_type = st.radio("Select Y-axis scale", ("Linear", "Logarithmic"), key=f"scale_type_{idx}")
                log_scale = scale_type == "Logarithmic"
                
                predict_the_future = st.checkbox("Predict the Future")
                
                if predict_the_future:
                    years_to_predict = st.number_input("Insert the number of years to predict into the future", value=5, min_value=1)
                    
            with col_chart:
                if len(selected_countries) == 0:
                    st.warning("Please select at least one country to use this feature")
                else:
                    if predict_the_future:
                        future_prediction = FuturePrediction(
                            selected_countries=selected_countries,
                            years_to_predict=years_to_predict,
                            scale_type=log_scale,
                            dataframe=filtered_dataframe[0],
                            target_column=target_column 
                        )
                        
                        tab1, tab2 = st.tabs(["Linear Regression", "Polynomial Features"])
                        
                        future_prediction.plot(tab1, LinearRegression())
                        future_prediction.plot(tab2, make_pipeline(PolynomialFeatures(degree=4), LinearRegression()))
                    else:
                        st.plotly_chart(chart(dataframe, selected_countries, selected_year_range, target_column, log_scale), use_container_width=True)

def chart(dataframe, selected_country, selected_year_range, target_column, log_scale=False):
    filtered_data = dataframe[(dataframe["country"].isin(selected_country)) 
                              & (dataframe["year"] >= selected_year_range[0]) 
                              & (dataframe["year"] <= selected_year_range[1])]

    filtered_data = filtered_data.sort_values(by="year")
    
    color_map = {country: color_palette[i % len(color_palette)] for i, country in enumerate(selected_country)}


    fig = px.line(
        filtered_data, 
        x='year', 
        y=target_column,
        color="country", 
        title=f"{target_column} over time",
        log_y=log_scale,
        category_orders={"country": selected_country}, 
        color_discrete_map=color_map 
    )


    with st.expander("View When Different Global Events Happened:"):
        col11, col12, col13, col14, col15 = st.columns([1,1,1,1,1])
        add_paris_agreement_line = col11.checkbox("Show Paris Agreement", value=True)
        add_covid_outbreak_line = col12.checkbox("Show COVID-19 Outbreak", value=True)
        add_world_war_two_lines = col13.checkbox("Show WW2 Start & End", value=False)
        add_world_war_one_lines = col14.checkbox("Show WW1 Start & End", value=False)
        add_the_great_depression = col15.checkbox("Show The Great Depression Start", value=False)
        
        col21, col22, col23, col24, col25 = st.columns([1,1,1,1,1])
        add_dissolution_of_the_soviet_union = col21.checkbox("Show the Dissolution of the Soviet Union", value=False)
        
        
    if add_dissolution_of_the_soviet_union:
        fig.add_vline(
            x=1991, 
            line=dict(color="red", dash="dash"), 
            annotation_text="End of USSR<br>1991", 
            annotation_position="top left"
        )

    if add_paris_agreement_line:
        fig.add_vline(
            x=2015, 
            line=dict(color="yellow", dash="dash"), 
            annotation_text="Paris Agreement<br>2015", 
            annotation_position="bottom left"
        )

    if add_covid_outbreak_line:
        fig.add_vline(
            x=2019, 
            line=dict(color="red", dash="dash"), 
            annotation_text="COVID-19<br>2019", 
            annotation_position="top left"
        )

    if add_world_war_two_lines:
        fig.add_vline(
            x=1939, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW2 Start<br>1939", 
            annotation_position="top right"
        )
        fig.add_vline(
            x=1945, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW2 End<br>1945", 
            annotation_position="bottom right"
        )

    if add_world_war_one_lines:
        fig.add_vline(
            x=1914, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW1 Start<br>1914", 
            annotation_position="bottom left"
        )
        fig.add_vline(
            x=1918, 
            line=dict(color="green", dash="dash"), 
            annotation_text="WW1 End<br>1918", 
            annotation_position="bottom right"
        )

    if add_the_great_depression:
        fig.add_vline(
            x=1929, 
            line=dict(color="yellow", dash="dash"), 
            annotation_text="Great Depression<br>1929",
            annotation_position="top left"
        )

    return fig

def map_chart(merged_dataframe, filtered_dataframe, is_filtered, selected_continent, selected_year_range, selected_countries, target_column):
    if filtered_dataframe.empty:
        st.warning("None of the selected countries fit the filters.")
        return None

    year_dataframe = filtered_dataframe[
        (filtered_dataframe["year"] >= selected_year_range[0]) & 
        (filtered_dataframe["year"] <= selected_year_range[1])
    ]
    
    year_dataframe = year_dataframe.sort_values(by="year")

    percentile_threshold = merged_dataframe[target_column].quantile(0.98)

    title_text = (
    f"Combined Attribute(s) Map Over Time"
    if is_filtered
    else "Co2 per Capita Map Over Time"
)

    map_fig = px.choropleth(
        year_dataframe, 
        locations="country",
        locationmode="country names", 
        color=target_column,  
        color_continuous_scale="Viridis", 
        labels={target_column: "CO2 per Capita (tonnes)"},
        title=title_text, 
        hover_name="country", 
        hover_data=[target_column],
        animation_frame="year",  
        range_color=[0, percentile_threshold] 
    )

    continent_scope = {
        "World": "world",
        "Europe": "europe",
        "Asia": "asia",
        "North America": "north america",
        "South America": "south america",
        "Africa": "africa"
    }

    map_fig.update_geos(
        scope=continent_scope[selected_continent],  
        showcoastlines=True, 
        coastlinecolor="Black",
        projection_type="natural earth",
    )

    selected_countries_df = filtered_dataframe[filtered_dataframe["country"].isin(selected_countries)]

    scatter_trace = go.Scattergeo(
    locations=selected_countries_df["country"],
    locationmode="country names",
    mode="markers",  
    marker=dict(
        size=4,  
        color="red", 
        line=dict(width=4, color="red"), 
    ),
    showlegend=False,  
    hoverinfo='location', 
)
    map_fig.add_trace(scatter_trace)

    map_fig.update_layout(
        autosize=True,  
        height=600,  
        title=dict(font=dict(size=24))  
    )

    return map_fig

def pie_chart(dataframe, selected_year_range, is_filtered, selected_countries, target_column):
    filtered_dataframe = dataframe[
        (dataframe["year"] >= selected_year_range[0]) & 
        (dataframe["year"] <= selected_year_range[1])
    ]
    
    color_map = {country: color_palette[i % len(color_palette)] for i, country in enumerate(selected_countries)}


    filtered_countries_df = filtered_dataframe[filtered_dataframe["country"].isin(selected_countries)]
    
    data_by_country = filtered_countries_df.groupby("country")[target_column].mean().reset_index()

    total_data = data_by_country[target_column].sum()
    data_by_country["percentage"] = (data_by_country[target_column] / total_data) * 100

    chart_title = (
        f"Combined Attribute(s) <br>(Average from {selected_year_range[0]} to {selected_year_range[1]})"
        if is_filtered
        else f"{target_column} <br>(Average from {selected_year_range[0]} to {selected_year_range[1]})"
    )

    pie_fig = px.pie(
        data_by_country, 
        names="country", 
        values="percentage", 
        title=chart_title,
        labels={"percentage": f"{target_column} (%)"},
        category_orders={"country": selected_countries},  
        color="country",  
        color_discrete_map=color_map  
    )


    pie_fig.update_traces(
        hovertemplate="%{label}: %{value:.2f}%<extra></extra>"  
    )

    description_text = (
    f"Illustrates the distribution of<br>"
    f"{target_column} as a % of the total,<br>"
    f"averaged across the selected years<br>"
    f"({selected_year_range[0]}-{selected_year_range[1]}),<br>"
    f"for the selected countries."
)
    pie_fig.add_annotation(
        text=description_text,
        xref="paper", yref="paper", 
        x=0.5, y=-0.3,               
        showarrow=False,             
        font=dict(size=12),          
        align="center"
    )

    return pie_fig
