import streamlit as st
import src.service as s

# TODO: Fix indent.
def display(dataframes):
    # TODO: session_state bug - adding country does not work correctly.
    # if 'initialized' not in st.session_state:
    #     st.session_state.initialized = True
    #     # TODO: Remove unscessary comment.
    #     default_countries = s.get_unique_countries(dataframes)[:2]  # Get the first two countries
    # else:
    #     default_countries = st.session_state.get('selected_country', [])

    page = st.sidebar.selectbox("Select Page", ["Home", "Data Exploration", "Trend Analysis"])

    st.sidebar.header("Filter Data")

    countries = s.get_unique_countries(dataframes)
    selected_country = st.sidebar.multiselect("Select Country", countries, default=s.get_unique_countries(dataframes)[:2])

    # st.session_state.selected_country = selected_country

    years = s.get_unique_years(dataframes)
    selected_year_range = st.sidebar.slider("Select Year Range", min(years), max(years), (min(years), max(years)))

    return page, selected_country, selected_year_range
