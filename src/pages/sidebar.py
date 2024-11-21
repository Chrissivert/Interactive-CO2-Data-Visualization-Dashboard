import streamlit as st
import src.service as s

def display(dataframes):
    page = st.sidebar.selectbox("Select Page", ["Data Exploration", "Trend Analysis"])

    st.sidebar.header("Filter Data")

    countries = s.get_unique_countries(dataframes)
    selected_country = st.sidebar.multiselect("Select Country", countries, default=s.get_unique_countries(dataframes)[:2])

    years = s.get_unique_years(dataframes)
    selected_year_range = st.sidebar.slider("Select Year Range", min(years), max(years), (min(years), max(years)))

    return page, selected_country, selected_year_range
