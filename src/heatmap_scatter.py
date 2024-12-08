import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import statsmodels.api as sm
import plotly.express as px
import numpy as np
import statsmodels.api as sm
import src.service as s
from colormap import Colormap as cm

color_palette = cm.COLORMAP.value

class HeatmapScatter:
    def __init__(self, dataframes, selected_country, selected_year_range, selected_continent):
        """
        Initialize the HeatmapScatter class.
        
        Parameters:
        - dataframes: A dictionary or list of dataframes.
        - selected_country: The country filter for the data.
        - selected_year_range: The year range filter for the data.
        - selected_continent: The continent filter for the data.
        """
        self.dataframes = dataframes
        self.selected_country = selected_country
        self.selected_year_range = selected_year_range
        self.selected_continent = selected_continent

        self.filtered_df = self.filter_data()

    def filter_data(self) -> pd.DataFrame:
        """Filter the data based on selected country, year range, and continent."""
        df = self.dataframes

        if isinstance(df, dict):
            df = pd.concat(df.values(), ignore_index=True)

        if self.selected_continent and self.selected_continent != "World":
            countries_in_continent = s.get_countries_by_continent([df], self.selected_continent)
            df = df[df["country"].isin(countries_in_continent)]

        if self.selected_country:
            df = df[df["country"].isin(self.selected_country)]

        if self.selected_year_range:
            df = df[(df["year"] >= self.selected_year_range[0]) & (df["year"] <= self.selected_year_range[1])]

        return df
    
    def filter_dataframe_by_continent(self, continent: str):
        return self.dataframes[self.dataframes["country"].isin(s.get_countries_by_continent([self.dataframes], continent))]

    def display_heatmap(self):
        """Display the heatmap based on the selected data source."""
        st.subheader("Heatmap of Columns")
        data_source = st.radio("Select Data to Display:", ["Selected Continent", "Selected Countries"])
        
        if data_source == "Selected Continent":
            data_df = None
            match self.selected_continent:
                case "World":
                    data_df = self.dataframes.copy()
                
                case "Africa":
                    data_df = self.filter_dataframe_by_continent("Africa")
                    
                case "Asia":
                    data_df = self.filter_dataframe_by_continent("Asia")
                
                case "Europe":
                    data_df = self.filter_dataframe_by_continent("Europe")
                    
                case "North America":
                    data_df = self.filter_dataframe_by_continent("North America")
                    
                case "South America":
                    data_df = self.filter_dataframe_by_continent("South America")
                    
                case _:
                    data_df = self.filter_data()
                    self.display_specific_heatmap(data_df)    
                
            if isinstance(data_df, dict):
                data_df = pd.concat(data_df.values(), ignore_index=True)
            self.display_specific_heatmap(data_df)
            
        elif data_source == "Selected Countries":
            if not self.selected_country:
                st.warning("Please select at least one country to use this feature.")
            else:
                self.display_specific_heatmap(self.filtered_df)

    def display_specific_heatmap(self, data):
        """Render the heatmap and raw data views."""
        if data is not None:
            tab1, tab2 = st.tabs(["Correlation Heatmap", "Raw Data"])

            numerical_cols = data.select_dtypes(include="number")
            
            if numerical_cols.shape[1] > 1:
                correlation_matrix = numerical_cols.corr()

                tab2.dataframe(data)

                with tab1:
                    fig = go.Figure(data=go.Heatmap(
                        z=correlation_matrix.values,
                        x=correlation_matrix.columns,
                        y=correlation_matrix.columns,
                        colorscale="RdBu",
                        zmin=-1,
                        zmax=1,
                        colorbar=dict(title="Correlation"),
                        hoverongaps=False
                    ))

                    fig.update_layout(
                        title="Correlation Heatmap",
                        xaxis_title="Columns",
                        yaxis_title="Columns",
                        autosize=True,
                        height=700,
                        width=900
                    )

                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough numerical columns in the dataset to create a heatmap.")

    def display_scatterplot(self):
        if len(self.selected_country) != 0:
            if self.filtered_df is not None:
                st.subheader("Scatter plot")

                self.filtered_df = self.filtered_df.dropna()
                col1, col2 = st.columns([1, 1])
                x_variable = col1.selectbox("Select X-axis", self.filtered_df.select_dtypes(include='number').columns, index=0, key="scatter_x")
                y_variable = col2.selectbox("Select Y-axis", self.filtered_df.select_dtypes(include='number').columns, index=1, key="scatter_y")

                show_country_trendline = st.checkbox("Show Country Trendlines", value=False, key="country_trendline")
                show_general_trendline = st.checkbox("Show General Trendline", value=False, key="general_trendline")

                fig = go.Figure()

                color_map = {country: color_palette[i % len(color_palette)] for i, country in enumerate(self.selected_country)}

                all_x = []
                all_y = []
                
                for country in self.selected_country:
                    country_data = self.filtered_df[self.filtered_df["country"] == country]

                    if country_data.empty:
                        st.warning(f"No data available for **{country}** to create scatterplot.")
                        continue

                    all_x.extend(country_data[x_variable].values)
                    all_y.extend(country_data[y_variable].values)

                    fig.add_trace(go.Scatter(
                        x=country_data[x_variable],  
                        y=country_data[y_variable],  
                        mode="markers",  
                        name=f"{country} {x_variable} vs {y_variable}",
                        marker=dict(size=8, color=color_map[country])  
                    ))

                    if show_country_trendline:
                        x = country_data[x_variable].values
                        y = country_data[y_variable].values
                        x_with_const = sm.add_constant(x)
                        model = sm.OLS(y, x_with_const).fit()
                        trendline = model.predict(x_with_const)

                        fig.add_trace(go.Scatter(
                            x=x,
                            y=trendline,
                            mode="lines",
                            name=f"{country} Trendline",
                            line=dict(color=color_map[country], dash="dash")
                        ))

                if show_general_trendline:
                    all_x = np.array(all_x)
                    all_y = np.array(all_y)
                    all_x_with_const = sm.add_constant(all_x)
                    general_model = sm.OLS(all_y, all_x_with_const).fit()
                    general_trendline = general_model.predict(all_x_with_const)

                    fig.add_trace(go.Scatter(
                        x=all_x,
                        y=general_trendline,
                        mode="lines",
                        name="General Trendline",
                        line=dict(color="white", dash="dash")
                    ))

                fig.update_layout(
                    template="plotly_dark",
                    title=f"{x_variable} vs {y_variable} for {self.selected_country[0]}" if len(self.selected_country) == 1 else f"{x_variable} vs {y_variable}",
                    xaxis_title=x_variable,
                    yaxis_title=y_variable,
                    legend_title="Country",
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for the selected criteria to create a scatterplot.")
