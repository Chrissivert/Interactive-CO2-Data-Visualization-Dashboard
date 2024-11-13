import streamlit as st
import pandas as pd

@st.cache_data
def load_csv_data(file_paths: list) -> list:
  dataframes = [pd.read_csv(file_path) for file_path in file_paths]
  return dataframes

def get_unique_column_names(dataframe: pd.DataFrame) -> list:
  return [col for col in dataframe.columns if col not in ['Entity', 'Code', 'Year']]

def get_unique_countries(dataframes: list[pd.DataFrame]) -> list:
  unique_countries = set()
  for dataframe in dataframes:
    unique_countries.update(dataframe['Entity'].unique())
  return sorted(unique_countries)

def get_unique_years(dataframes: list[pd.DataFrame]) -> list:
  unique_years = set()
  for dataframe in dataframes:
    unique_years.update(dataframe['Year'].unique())
  return sorted(unique_years)