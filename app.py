import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
  page_title="Final Project | IE500417 - Data processing and visualization",
  layout="wide",
  initial_sidebar_state="expanded")
st.title("Interactive CO₂ Emissions & Greenhouse Gas Dashboard")

@st.cache_data
def load_data(file_path):
  return pd.read_csv(file_path)

uploaded_file = st.file_uploader("Upload the primary CO₂ CSV file", type=["csv"])
if uploaded_file:
  df = load_data(uploaded_file)
  st.write(":green[Dataset loaded successfully!]")

  st.sidebar.header("Filter Data")
    
  countries = df["country"].unique()
  selected_country = st.sidebar.multiselect("Select Country", countries, default=countries[:2])

  years = df["year"].unique()
  selected_year_range = st.sidebar.slider("Select Year Range", min(years), max(years), (min(years), max(years)))
    
  filtered_data = df[(df["country"].isin(selected_country)) &
                       (df["year"] >= selected_year_range[0]) &
                       (df["year"] <= selected_year_range[1])]

  metrics = ["co2", "co2_per_capita", "co2_growth_abs", "cement_co2", "coal_co2", 
               "gas_co2", "oil_co2", "methane", "nitrous_oxide", "primary_energy_consumption"]
  selected_metric = st.sidebar.selectbox("Select Metric for Analysis", metrics)

  st.subheader(f"{selected_metric} Over Time for Selected Countries")
  fig = px.line(filtered_data, x="year", y=selected_metric, color="country", title=f"{selected_metric} Over Time")
  st.plotly_chart(fig, use_container_width=True)

  selected_metrics = st.sidebar.multiselect("Select Metrics for Multi-Metric Comparison", metrics, default=metrics[:2])
  fig_multi = go.Figure()
  for metric in selected_metrics:
    for country in selected_country:
      data = filtered_data[filtered_data["country"] == country]
      fig_multi.add_trace(go.Scatter(x=data["year"], y=data[metric], mode="lines", name=f"{metric} - {country}"))
  fig_multi.update_layout(title="Multi-Metric Comparison", xaxis_title="Year", yaxis_title="Metric Value")
  st.plotly_chart(fig_multi, use_container_width=True)

  st.subheader("Country Comparison for a Specific Metric")
  fig_country = px.line(filtered_data, x="year", y=selected_metric, color="country",
                          title=f"{selected_metric} Across Selected Countries")
  st.plotly_chart(fig_country, use_container_width=True)

  if st.sidebar.checkbox("Show CO₂ Emission Prediction for Next 3 Years"):
    st.subheader("CO₂ Emissions Prediction (Next 3 Years)")
    country_for_pred = st.selectbox("Select Country for Prediction", selected_country)
    country_data = filtered_data[filtered_data["country"] == country_for_pred][["year", "co2"]]
    country_data = country_data.dropna()

    x = country_data[["year"]]
    y = country_data["co2"]
    model = LinearRegression()
    model.fit(x, y)
    future_years = np.array([[year] for year in range(x["year"].max() + 1, x["year"].max() + 4)])
    predictions = model.predict(future_years)
    
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=country_data["year"], y=country_data["co2"], mode="lines", name="Historical CO₂"))
    fig_pred.add_trace(go.Scatter(x=future_years.flatten(), y=predictions, mode="lines+markers", name="Predicted CO₂"))
    fig_pred.update_layout(title="CO₂ Emissions Prediction for Next 3 Years", xaxis_title="Year", yaxis_title="CO₂ Emissions")
    st.plotly_chart(fig_pred, use_container_width=True)
      
  st.subheader("Summary Statistics")
  st.write(filtered_data.describe())

  csv = filtered_data.to_csv(index=False)
  st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")

  st.subheader("Incorporate an Additional Dataset")
  additional_file = st.file_uploader("Upload an additional dataset (optional)", type=["csv"])
  if additional_file:
    additional_data = pd.read_csv(additional_file)
    st.write("Additional Dataset Loaded Successfully!")
    st.write(additional_data.head())
        
    combined_data = pd.merge(filtered_data, additional_data, on=["country", "year"], how="inner")
    st.write("Merged Dataset Preview:")
    st.write(combined_data.head())

    st.sidebar.header("Correlation Analysis")
    metric_co2 = st.sidebar.selectbox("Select CO₂ Metric", metrics)
    metric_additional = st.sidebar.selectbox("Select Additional Metric", additional_data.columns)
        
    st.subheader(f"Correlation between {metric_co2} and {metric_additional}")
    fig_corr = px.scatter(combined_data, x=metric_additional, y=metric_co2, color="country",
                          title=f"Correlation between {metric_co2} and {metric_additional}")
    st.plotly_chart(fig_corr, use_container_width=True)