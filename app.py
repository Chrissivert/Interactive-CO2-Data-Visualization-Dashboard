import streamlit as st

import src.pages.data_exploration
import src.pages.home
import src.service as s
import src.pages.trend_analysis
import src.page_names as pn
import src.pages.sidebar as sidebar

st.set_page_config(
  page_title="Interactive Data Visualization Dashboard",
  layout="wide",
  initial_sidebar_state="expanded"
)
st.title("Interactive Data Visualization Dashboard")

uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
if uploaded_files:
  dataframes = s.load_csv_data(uploaded_files)
  st.write(":green[Datasets loaded successfully!]" if len(dataframes) > 1 else ":green[Dataset loaded successfully!]")
  
  page, selected_country, selected_year_range = sidebar.display(dataframes)

  if page == pn.Pages.HOME.value:
    src.pages.home.page()
      
  elif page == pn.Pages.DATA_EXPLORATION.value:
    src.pages.data_exploration.page(dataframes, selected_country, selected_year_range)

  elif page == pn.Pages.TREND_ANALYSIS.value:
    src.pages.trend_analysis.page(s.get_metrics(dataframes), selected_country, selected_year_range)