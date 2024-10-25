import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

data = pd.read_csv("owid-co2-data.csv")

st.set_page_config(
  page_title="IE500417 - Final Project",
  layout="wide"
)

st.title('Data Visualisation')

st.subheader("Data preview (head)")
st.write(data.head())

st.sidebar.header("User Input")
country = st.sidebar.selectbox("Choose a filter", options=data['country'].unique())

filtered_data = data[data['country'] == country]

st.subheader(f"Population Over Time in {country}")
fig = px.line(
  filtered_data,
  x="year",
  y="population",
  title=f"Population Trend in {country}",
  labels={"year": "Year", "population": "Population"}
)

fig.update_traces(
  hovertemplate="Year: %{x}<br>Population: %{y}:,"
)

st.plotly_chart(fig)