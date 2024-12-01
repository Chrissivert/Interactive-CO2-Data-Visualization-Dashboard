import streamlit as st
import pandas as pd
import requests
import numpy as np
import pycountry_convert as pc


@st.cache_data
def load_csv_data(file_paths: list) -> list:
  dataframes = [pd.read_csv(file_path) for file_path in file_paths]
  return dataframes

@st.cache_data
def load_default_file(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def get_unique_column_names(dataframe: pd.DataFrame) -> list:
  return [col for col in dataframe.columns if col not in ['country', 'iso_code', 'year']]

def get_metrics(dataframes: list[pd.DataFrame]) -> dict:
  metrics = {}
  for dataframe in dataframes:
    for column in get_unique_column_names(dataframe):
      metrics[column] = (dataframe, column)
      
  return metrics

def merge_dataframes(dataframes: dict) -> pd.DataFrame:
    """Merge all datasets into a single DataFrame on 'country' and 'year'."""
    merged_df = None
    
    for name, df in dataframes.items():  # Iterate over dictionary items
        # Ensure required columns exist
        if not {'country', 'year'}.issubset(df.columns):
            st.warning(f"Dataset {name} is missing required columns ('country', 'year'). Skipping.")
            continue
        
        if merged_df is None:
            merged_df = df
        else:
            # Merge on common columns ('country', 'year')
            merged_df = pd.merge(merged_df, df, on=['country', 'year', 'Code'], how='outer')
    
    return merged_df


def get_unique_countries(dataframes: list[pd.DataFrame]) -> list:
  unique_countries = set()
  for dataframe in dataframes:
    unique_countries.update(dataframe['country'].unique())
  return sorted(unique_countries)

def get_unique_years(dataframes: list[pd.DataFrame]) -> list:
  unique_years = set()
  for dataframe in dataframes:
    unique_years.update(dataframe['year'].unique())
  return sorted(unique_years)


def get_year_range_from_countries(dataframes: list[pd.DataFrame], countries: list[str]):
  unique_years = set()
  for dataframe in dataframes:
    unique_years.update(dataframe[dataframe["country"].isin(countries)]["year"].unique())
  return sorted(unique_years)




def predict_future_values_with_models(country_specific_data: pd.DataFrame, selected_metric: str, years_to_predict: int, model_to_use):
  x = country_specific_data[["year"]]
  y = country_specific_data[selected_metric]
  
  model = model_to_use
  model.fit(x, y)
  
  future_years = np.array(range(x["year"].max() + 1, x["year"].max() + 1 + years_to_predict)).reshape(-1, 1)
  
  predictions = model.predict(future_years)
  
  return future_years, predictions,


def country_to_continent(country_name):
    try:
        # Convert country name to ISO 2 code
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        # Convert ISO 2 code to continent code
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        # Convert continent code to continent name
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except Exception as e:
        return None
    
def get_unique_continents(dataframes: list) -> list:
    continents = set()  # Initialize an empty set to store continents
    for dataframe in dataframes:
        for country in dataframe['country'].unique():  # Iterate over unique countries
            continent = country_to_continent(country)  # Get continent for the country
            if continent:  # Only add the continent if it's not None
                continents.add(continent)
    return sorted(continents)  # Return the sorted list of unique continents


def get_countries_by_continent(dataframes: list, selected_continent: str) -> list:
    countries_in_continent = set()
    for dataframe in dataframes:
        for country in dataframe['country'].unique():
            try:
                continent = country_to_continent(country)
                if continent == selected_continent:
                    countries_in_continent.add(country)
            except Exception as e:
                pass
    return sorted(countries_in_continent)
    





# Removed unused methods (?)
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