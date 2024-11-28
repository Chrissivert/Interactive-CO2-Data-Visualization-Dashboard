import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm

class HeatmapScatter:
    def __init__(self, dataframes, selected_country, selected_year_range):
        self.dataframes = dataframes
        self.selected_country = selected_country
        self.selected_year_range = selected_year_range
        self.combined_df = self.merge_dataframes()
        self.combined_df_filtered = self.merge_dataframes(selected_only=True)

    def merge_dataframes(self, selected_only=False):
        """Merge all datasets into a single DataFrame on 'country', 'Code', and 'year'."""
        merged_df = None
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
        
        # Apply filtering for selected countries and year range only for scatterplot or specific visualizations
        if selected_only and self.selected_country:
            merged_df = merged_df[merged_df["country"].isin(self.selected_country)]
        if self.selected_year_range:
            start_year, end_year = self.selected_year_range
            merged_df = merged_df[(merged_df["year"] >= start_year) & (merged_df["year"] <= end_year)]
        
        return merged_df

    def display_heatmap(self):
        """Generate and display a heatmap for the combined dataset, with option to show only selected countries."""
        if self.combined_df is not None:
            st.subheader("Heatmap of columns")
            
            # Radio button to toggle between world (no filter) and selected countries
            data_source = st.radio("Select data to display:", ["World (No Filter)", "Selected Countries"])

            # Choose the appropriate DataFrame based on the user's selection
            if data_source == "World (No Filter)":
                heatmap_data = self.combined_df
            else:
                heatmap_data = self.combined_df_filtered

            # Only include numerical columns for correlation matrix
            numerical_cols = heatmap_data.select_dtypes(include='number')
            
            if numerical_cols.shape[1] > 1:
                # Calculate the correlation matrix
                correlation_matrix = numerical_cols.corr()
                st.write("Correlation Matrix:")
                
                # Checkbox to show/hide raw data
                show_raw_data = st.checkbox("Show Raw Data", value=False)
                if show_raw_data:
                    st.dataframe(heatmap_data)  # Display the raw data table
                
                # Create the heatmap
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Not enough numerical columns in the combined dataset to create a heatmap.")
        else:
            st.error("No data available to display a heatmap.")

    def display_scatterplot(self):
        """Generate and display scatterplot with OLS trendline for the selected data."""
        if self.combined_df_filtered is not None:
            st.subheader("Scatterplot with OLS Trendline")

            # Dropdown for X and Y-axis selection
            x_variable = st.selectbox("Select X-axis", self.combined_df_filtered.select_dtypes(include='number').columns, index=0, key="scatter_x")
            y_variable = st.selectbox("Select Y-axis", self.combined_df_filtered.select_dtypes(include='number').columns, index=1, key="scatter_y")

            fig = go.Figure()

            # Add scatter points for each country
            for country in self.combined_df_filtered["country"].unique():
                country_data = self.combined_df_filtered[self.combined_df_filtered["country"] == country]
                fig.add_trace(go.Scatter(
                    x=country_data[x_variable],  # Selected X-Axis variable
                    y=country_data[y_variable],  # Selected Y-Axis variable
                    mode="markers",  # Only markers (no lines)
                    name=f"{country} {x_variable} vs {y_variable}",
                    marker=dict(size=8)  # Adjust size of points for visibility
                ))

            # --- Add OLS Trendline ---
            X = self.combined_df_filtered[[x_variable]]  # Independent variable (selected X-Axis)
            X = sm.add_constant(X)  # Add constant term for OLS (intercept)
            y = self.combined_df_filtered[y_variable]  # Dependent variable (selected Y-Axis)

            model = sm.OLS(y, X).fit()
            trendline = model.predict(X)  # Predicted values (trendline)

            # Add the OLS trendline to the scatter plot
            fig.add_trace(go.Scatter(
                x=self.combined_df_filtered[x_variable],  # Selected X-Axis for OLS line
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
