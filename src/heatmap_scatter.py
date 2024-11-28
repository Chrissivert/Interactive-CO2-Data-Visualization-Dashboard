import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm

class HeatmapScatter:
    def __init__(self, dataframes, selected_country, selected_year_range):
        """
        Initialize the Visualization class with loaded dataframes, selected countries, and selected year range.
        
        Args:
        dataframes (dict): A dictionary where keys are dataset names and values are pandas DataFrames.
        selected_country (list): List of selected countries for plotting.
        selected_year_range (tuple): A tuple containing the start and end year for filtering.
        """
        self.dataframes = dataframes
        self.selected_country = selected_country
        self.selected_year_range = selected_year_range
        self.combined_df, self.filtered_df = self.merge_dataframes()


    def merge_dataframes(self):
        """Merge all datasets into a single DataFrame on 'country', 'Code', and 'year'."""
        merged_df = None
        filtered_df = None
        
        for name, df in self.dataframes.items():
            # Ensure required columns exist
            if not {'country', 'Code', 'year'}.issubset(df.columns):
                st.warning(f"Dataset {name} is missing required columns ('country', 'Code', 'year'). Skipping.")
                continue
            
            if merged_df is None:
                merged_df = df
            else:
                # Merge on common columns
                merged_df = pd.merge(merged_df, df, on=['country', 'Code', 'year'], how='outer')
        
        # Apply filtering for selected countries and year range
        if self.selected_country:
            filtered_df = merged_df[merged_df["country"].isin(self.selected_country)]
        if self.selected_year_range:
            start_year, end_year = self.selected_year_range
            merged_df = merged_df[(merged_df["year"] >= start_year) & (merged_df["year"] <= end_year)]
            filtered_df = filtered_df[(filtered_df["year"] >= start_year) & (filtered_df["year"] <= end_year)]
        
        return merged_df, filtered_df


    def display_heatmap(self):
        """Generate and display a heatmap for the combined dataset with option to show only selected countries."""
        if self.combined_df is not None:
            st.subheader("Heatmap of Combined Dataset")

            # Selectbox to toggle between world data and selected countries only
            show_selected_countries_only = st.selectbox(
                "Select dataset for heatmap", 
                ("World (No filtering)", "Selected Countries Only")
            ) == "Selected Countries Only"

            # Use appropriate dataset for heatmap
            data_for_heatmap = self.filtered_df if show_selected_countries_only else self.combined_df
            
            # Only include numerical columns for correlation matrix
            numerical_cols = data_for_heatmap.select_dtypes(include='number')
            
            if numerical_cols.shape[1] > 1:
                # Calculate the correlation matrix
                correlation_matrix = numerical_cols.corr()
                st.write("Correlation Matrix:")
                st.dataframe(correlation_matrix)
                
                # Create the heatmap
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Not enough numerical columns in the combined dataset to create a heatmap.")
        else:
            st.error("No data available to display a heatmap.")


    def display_scatterplot(self):
        """Generate and display scatterplot with OLS trendline for the selected data (selected countries)."""
        if self.filtered_df is not None:
            st.subheader("Scatterplot with OLS Trendline")

            # Dropdown for X and Y-axis selection
            x_variable = st.selectbox("Select X-axis", self.filtered_df.select_dtypes(include='number').columns, index=0, key="scatter_x")
            y_variable = st.selectbox("Select Y-axis", self.filtered_df.select_dtypes(include='number').columns, index=1, key="scatter_y")

            fig = go.Figure()

            # Add scatter points for each country in the filtered data
            for country in self.filtered_df["country"].unique():
                country_data = self.filtered_df[self.filtered_df["country"] == country]
                fig.add_trace(go.Scatter(
                    x=country_data[x_variable],  # Selected X-Axis variable
                    y=country_data[y_variable],  # Selected Y-Axis variable
                    mode="markers",  # Only markers (no lines)
                    name=f"{country} {x_variable} vs {y_variable}",
                    marker=dict(size=8)  # Adjust size of points for visibility
                ))

            # --- Add OLS Trendline ---
            X = self.filtered_df[[x_variable]]  # Independent variable (selected X-Axis)
            X = sm.add_constant(X)  # Add constant term for OLS (intercept)
            y = self.filtered_df[y_variable]  # Dependent variable (selected Y-Axis)

            model = sm.OLS(y, X).fit()
            trendline = model.predict(X)  # Predicted values (trendline)

            # Add the OLS trendline to the scatter plot
            fig.add_trace(go.Scatter(
                x=self.filtered_df[x_variable],  # Selected X-Axis for OLS line
                y=trendline,  # Predicted values
                mode="lines",
                name="OLS Trendline",
                line=dict(color="white", dash="dash")  # Set line color to white (or any other color)
            ))

            # Update layout to improve aesthetics
            fig.update_layout(
                template="plotly_dark",
                title=f"{x_variable} vs {y_variable} with OLS Trendline",
                xaxis_title=x_variable,
                yaxis_title=y_variable
            )

            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected criteria to create a scatterplot.")
