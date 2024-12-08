import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import statsmodels.api as sm
import plotly.express as px

color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]

class HeatmapScatter:
    def __init__(self, dataframes, selected_country, selected_year_range):
        """
        Initialize the HeatmapScatter class.
        
        Parameters:
        - dataframes: A dictionary or list of dataframes.
        - selected_country: The country filter for the data.
        - selected_year_range: The year range filter for the data.
        """
        self.dataframes = dataframes
        self.selected_country = selected_country
        self.selected_year_range = selected_year_range

        self.filtered_df = self.filter_data()

    def filter_data(self) -> pd.DataFrame:
        """Filter the data based on selected country and year range."""
        df = self.dataframes  
        
        if isinstance(df, dict):
            df = df.get(self.selected_country, pd.DataFrame())
        
        if self.selected_year_range:
            df = df[(df['year'] >= self.selected_year_range[0]) & (df['year'] <= self.selected_year_range[1])]
        
        return df

    def display_heatmap(self):
        st.subheader("Heatmap of columns")
        data_source = st.radio("Select data to display:", ["All Countries", "Selected Countries"])
        if data_source == "All Countries":
            self.display_specific_heatmap(self.filtered_df)
        else:
            if len(self.selected_country) == 0:
                st.warning("Please select at least one country to use this feature")
            else:
                self.display_specific_heatmap(self.filtered_df[self.filter_data()["country"].isin(self.selected_country)])
            
            
    def display_specific_heatmap(self, data):
        if self.filtered_df is not None:            
            tab1, tab2 = st.tabs(["Correlation Heatmap", "Raw Data"])
            
            heatmap_data = data
            
            numerical_cols = heatmap_data.select_dtypes(include='number')
            
            if numerical_cols.shape[1] > 1:
                correlation_matrix = numerical_cols.corr()
                
                tab2.dataframe(heatmap_data)  
                
                with tab1: 
                    fig = go.Figure(data=go.Heatmap(
                        z=correlation_matrix.values,
                        x=correlation_matrix.columns,
                        y=correlation_matrix.columns,
                        colorscale='RdBu',
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

                fig = go.Figure()

                color_map = {country: color_palette[i % len(color_palette)] for i, country in enumerate(self.selected_country)}

                
                for country in self.selected_country:
                    country_data = self.filtered_df[self.filtered_df["country"] == country]

                    if country_data.empty:
                        st.warning(f"No data available for {country} to create scatterplot.")
                        continue

                    fig.add_trace(go.Scatter(
                        x=country_data[x_variable],  
                        y=country_data[y_variable],  
                        mode="markers",  
                        name=f"{country} {x_variable} vs {y_variable}",
                        marker=dict(size=8, color=color_map[country])  
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

