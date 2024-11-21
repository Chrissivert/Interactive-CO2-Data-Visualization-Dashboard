import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import src.service as s
from src.markdown.custom_markdown import CustomMarkdown

def page(metrics, selected_country, selected_year_range):
  st.title("Trend Analysis")
  compare_matrics(metrics, selected_country, selected_year_range)
  predict_future_values(metrics, selected_country)

def predict_future_values(metrics: dict, selected_countries: list) -> None:
  st.header("Future Value Predictions")
  
  years_to_predict = st.number_input(
    "Insert the amount of years to predict into the future", 
    value=5, 
    placeholder="Type the number of years to predict...", 
    min_value=1
  )
  
  metric_to_dataframe_map = {metric: df for metric, (df, _) in metrics.items()}
  available_metrics = list(metric_to_dataframe_map.keys())
  
  selected_metric = st.selectbox("Select a Metric", available_metrics)
  dataframe = metric_to_dataframe_map[selected_metric]
  
  country_data = dataframe[dataframe["Entity"].isin(selected_countries)]
  if country_data.empty:
    st.warning(f"No data found for the selected countries: {', '.join(selected_countries)}.")
    return None
  
  scale_type = st.radio(
    "Select Y-axis scale", 
    ("Linear", "Logarithmic"), 
    key="scale_type"
  )
  
  tab1, tab2, tab3 = st.tabs(["Linear Regression", 
                              "Polynomial Features", 
                              "Random Forest Regressor"]
                             )
  
  degree = tab2.number_input("Insert the level of degree the Polynomial Feature model is to use (range is 2 to 92)", 
                             value=20, 
                             placeholder="Type the level of degree to use...", 
                             min_value=2, 
                             max_value=30)
  
  plot_predict_future_values(
    tab1, 
    selected_countries, 
    country_data, 
    selected_metric, 
    years_to_predict, 
    LinearRegression(), 
    scale_type
    )
  plot_predict_future_values(
    tab2, 
    selected_countries, 
    country_data, 
    selected_metric, 
    years_to_predict, 
    make_pipeline(PolynomialFeatures(degree=degree), LinearRegression()), 
    scale_type
    )
  plot_predict_future_values(
    tab3, 
    selected_countries, 
    country_data, 
    selected_metric, 
    years_to_predict, 
    RandomForestRegressor(n_estimators=100, random_state=42), 
    scale_type)
    

def plot_predict_future_values(tab, selected_countries: list, country_data: pd.DataFrame, selected_metric: str, years_to_predict: int, model, scale_type: str, special_function = None) -> None:
  with tab:
    special_function
    log_scale = scale_type == "Logarithmic" 
    fig_pred = go.Figure()
    for country in selected_countries:
      country_specific_data = country_data[country_data["Entity"] == country]
      country_specific_data = country_specific_data[["Year", selected_metric]].dropna()
      if country_specific_data.empty:
        st.warning(f"No valid data for predictions for: {country}")
        continue
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
      legend_title="Country",
      yaxis_type='log' if log_scale else 'linear'
    )
    st.plotly_chart(fig_pred, use_container_width=True)

# TODO: Fix indent.
def compare_matrics(metrics, selected_country, selected_year_range):
    custom_markdown = CustomMarkdown()
    st.header("Select Metrics for Comparison")

    if len(metrics) > 1:
        col1, col_mid, col2 = st.columns([1, 0.5, 1])

        if "metric1" not in st.session_state:
            st.session_state.metric1 = list(metrics.keys())[0]  
        if "metric2" not in st.session_state:
            st.session_state.metric2 = list(metrics.keys())[1] 

        metric1_label = col1.selectbox(
            "Select Metric for the X-Axis",
            list(metrics.keys()),
            index=list(metrics.keys()).index(st.session_state.metric1),
            key="metric1_widget",
        )
        metric2_label = col2.selectbox(
            "Select Metric for the Y-Axis",
            list(metrics.keys()),
            index=list(metrics.keys()).index(st.session_state.metric2),
            key="metric2_widget",
        )

        st.session_state.metric1 = metric1_label
        st.session_state.metric2 = metric2_label

        with col_mid:
            swap_datasets = st.button("Swap Metrics", use_container_width=True)
            custom_markdown.button_style(margin_top="30px", padding="5px 10px")

        if metric1_label == metric2_label:
            st.warning("Please select two unique metrics for comparison.")
            return None

        if swap_datasets:
            st.session_state.metric1, st.session_state.metric2 = (
                st.session_state.metric2,
                st.session_state.metric1,
            )
            st.rerun() 

        df1, metric1 = metrics[st.session_state.metric1]
        df2, metric2 = metrics[st.session_state.metric2]

        df1_filtered = df1[(
            df1["Entity"].isin(selected_country))
            & (df1["Year"] >= selected_year_range[0])
            & (df1["Year"] <= selected_year_range[1])
        ][["Entity", "Year", "Code", metric1]]

        df2_filtered = df2[(
            df2["Entity"].isin(selected_country))
            & (df2["Year"] >= selected_year_range[0])
            & (df2["Year"] <= selected_year_range[1])
        ][["Entity", "Year", "Code", metric2]]

        merged_df = pd.merge(df1_filtered, df2_filtered, on=["Entity", "Year", "Code"], how="inner")
        displayed_countries = merged_df["Entity"].unique()
        missing_countries = [
            country for country in selected_country if country not in displayed_countries
        ]

        if missing_countries:
            st.warning(
                f"The following countries are not displayed due to missing data for one or both selected metrics: {', '.join(missing_countries)}."
            )

        if not merged_df.empty:
            for country in displayed_countries:
                country_data = merged_df[merged_df["Entity"] == country]

                fig = px.scatter(
                    country_data,
                    x=metric1,
                    y=metric2,
                    trendline="ols",
                    title=f"{st.session_state.metric1} vs {st.session_state.metric2} for {country}",
                    labels={metric1: metric1, metric2: metric2},
                )
                fig.update_traces(
                    line=dict(color="green"),
                    selector=dict(mode="lines"),
                )
                fig.update_traces(mode="lines")

                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select at least one valid entity for this feature to work.")
            return None
    else:
        st.warning("Please upload at least two files to use this feature.")
        return None
