import streamlit as st

import src.pages.data_exploration
import src.service as s
import src.pages.trend_analysis

st.set_page_config(
  page_title="Data Visualization Dashboard",
  layout="wide",
  initial_sidebar_state="expanded"
)
st.title("Interactive Data Visualization Dashboard")

uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
if uploaded_files:
  dataframes = s.load_csv_data(uploaded_files)
  st.write(":green[Datasets loaded successfully!]" if len(dataframes) > 1 else ":green[Dataset loaded successfully!]")
  
  page = st.sidebar.selectbox("Select Page", [
    "Home", "Data Exploration", "Trend Analysis"
  ])

  metrics = {}
  for dataframe in dataframes:
    for column in s.get_unique_column_names(dataframe):
      metrics[column] = (dataframe, column)

  st.sidebar.header("Filter Data")
  countries = s.get_unique_countries(dataframes)
  selected_country = st.sidebar.multiselect("Select Country", countries, default=countries[:2])

  years = s.get_unique_years(dataframes)
  selected_year_range = st.sidebar.slider("Select Year Range", min(years), max(years), (min(years), max(years)))

  if page == "Home":
    st.title("Welcome to the Data Visualization Dashboard")
      
  elif page == "Data Exploration":
    src.pages.data_exploration.page(dataframes, selected_country, selected_year_range)

  elif page == "Trend Analysis":
    src.pages.trend_analysis.page(metrics, selected_country, selected_year_range)