import streamlit as st
import pandas as pd
import plotly.express as px
import src.service as s
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def page(metrics, selected_country, selected_year_range):
  st.title("Trend Analysis")
    
  compare_matrics(metrics, selected_country, selected_year_range)
  
  predict_future_values(metrics, selected_country)

def predict_future_values(metrics: dict, selected_countries: list) -> None:
  st.header("Future Value Predictions")
  
  years_to_predict = st.number_input(
    "Insert the amount of years to predict into the future", value=1, placeholder="Type the number of years...", min_value=1
  )
  
  metric_to_dataframe_map = {metric: df for metric, (df, _) in metrics.items()}
  available_metrics = list(metric_to_dataframe_map.keys())
  
  selected_metric = st.selectbox("Select a Metric", available_metrics)
  
  dataframe = metric_to_dataframe_map[selected_metric]
  
  country_data = dataframe[dataframe["Entity"].isin(selected_countries)]
  if country_data.empty:
    st.warning(f"No data found for the selected countries: {', '.join(selected_countries)}.")
    return None
  
  tab1, tab2, tab3, = st.tabs(["Linear Regression", "Polynomial Features", "Random Forest Regressor"])
  
  plot_predict_future_values(tab1, selected_countries, country_data, selected_metric, years_to_predict, LinearRegression())
  plot_predict_future_values(tab2, selected_countries, country_data, selected_metric, years_to_predict, make_pipeline(PolynomialFeatures(degree=20), LinearRegression()))
  plot_predict_future_values(tab3, selected_countries, country_data, selected_metric, years_to_predict, RandomForestRegressor(n_estimators=100, random_state=42))
    
def plot_predict_future_values(tab, selected_countries, country_data, selected_metric, years_to_predict, model):
  with tab:
    fig_pred = go.Figure()
    for country in selected_countries:
      country_specific_data = country_data[country_data["Entity"] == country]
      country_specific_data = country_specific_data[["Year", selected_metric]].dropna()
      
      future_years, predictions = s.predict_future_values_with_models(country_specific_data, selected_metric, years_to_predict, model)
      
      fig_pred.add_trace(go.Scatter(
        x=country_specific_data["Year"],
        y=country_specific_data[selected_metric],
        mode="lines",
        name=f"Historical {selected_metric} ({country})"
      ))
      
      fig_pred.add_trace(go.Scatter(
        x=future_years.flatten(),
        y=predictions,
        mode="lines+markers",
        name=f"Predicted {selected_metric} ({country})"
      ))
      
    fig_pred.update_layout(
      title=f"{selected_metric} Prediction for Next {years_to_predict} Years",
      xaxis_title="Year",
      yaxis_title=selected_metric,
      legend_title="Country"
    )
    
    tab.plotly_chart(fig_pred, use_container_width=True)

def compare_matrics(metrics, selected_country, selected_year_range):
  st.header("Select Metrics for Comparison")
  
  if len(metrics) > 1:
    col1, col2 = st.columns(2)
    metric1_label = col1.selectbox("Select Metric for the X-Axis", list(metrics.keys()), key="metric1", index=0)
    metric2_label = col2.selectbox("Select Metric for the Y-Axis", list(metrics.keys()), key="metric2", index=1)

    if metric1_label == metric2_label:
      st.warning("Please select two unique metrics for comparison.")
      return None

    df1, metric1 = metrics[metric1_label]
    df2, metric2 = metrics[metric2_label]

    df1_filtered = df1[(df1["Entity"].isin(selected_country)) 
                       & (df1["Year"] >= selected_year_range[0]) 
                       & (df1["Year"] <= selected_year_range[1])][["Entity", "Year", "Code", metric1]]

    df2_filtered = df2[(df2["Entity"].isin(selected_country)) 
                       & (df2["Year"] >= selected_year_range[0]) 
                       & (df2["Year"] <= selected_year_range[1])][["Entity", "Year", "Code", metric2]]

    merged_df = pd.merge(df1_filtered, df2_filtered, on=["Entity", "Year", "Code"], how="inner")
    displayed_countries = merged_df["Entity"].unique()
    missing_countries = [country for country in selected_country if country not in displayed_countries]

    if missing_countries:
        st.warning(f"The following countries are not displayed due to missing data for one or both selected metrics: {', '.join(missing_countries)}.")

    selected_country_codes = dict(merged_df[['Entity', 'Code']].drop_duplicates().assign(
            Code=lambda df: df['Code'].str.upper()).values)

    if not merged_df.empty:
      for country, iso_code in selected_country_codes.items():
        country_data = merged_df[merged_df["Entity"] == country]
        # country_code = s.get_alpha_2_code(iso_code)
        # flag_image = s.get_flag_url(country_code)

        fig = px.scatter(
          country_data,
          x=metric1,
          y=metric2,
          trendline="ols",
          title=f"{metric1} vs {metric2} for {country}",
          labels={metric1: metric1, metric2: metric2}
        )
        fig.update_traces(
          line=dict(color="green"), 
          selector=dict(mode="lines")
        )
        fig.update_traces(mode="lines")
        # st.write(f'<span style="display: inline-block; font-weight: bold;">{country}</span> <img src="{flag_image}" width="40" style="vertical-align: middle;">', unsafe_allow_html=True)
                
        st.plotly_chart(fig, use_container_width=True)
    else:
      st.warning("Please have at least two files uploaded to be able to use this feature.")
      return None
  else:
    st.warning("Please upload at least teo files to use this feature.")
    return None