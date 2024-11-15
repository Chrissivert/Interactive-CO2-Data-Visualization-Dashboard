import streamlit as st
import pandas as pd
import requests


@st.cache_data
def load_csv_data(file_paths: list) -> list:
  dataframes = [pd.read_csv(file_path) for file_path in file_paths]
  return dataframes

def get_unique_column_names(dataframe: pd.DataFrame) -> list:
  return [col for col in dataframe.columns if col not in ['Entity', 'Code', 'Year']]

def get_metrics(dataframes: list[pd.DataFrame]) -> dict:
  metrics = {}
  for dataframe in dataframes:
    for column in get_unique_column_names(dataframe):
      metrics[column] = (dataframe, column)
      
  return metrics

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

def get_alpha_2_code(alpha_3):
    url = f"https://restcountries.com/v3.1/all"
    response = requests.get(url) 
    countries = response.json()    
    for country in countries:
        if country.get("cca3") == alpha_3:  
            return country.get("cca2") 
  
    return None 



def get_flag_url(country_code):
    return f"https://flagcdn.com/w40/{country_code.lower()}.png"