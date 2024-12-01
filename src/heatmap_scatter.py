import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import statsmodels.api as sm
import plotly.express as px

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

        # Filter the data based on the selected country and year range
        self.filtered_df = self.filter_data()

    def filter_data(self) -> pd.DataFrame:
        """Filter the data based on selected country and year range."""
        df = self.dataframes  # Assuming dataframes is a single dataframe or a dict of dataframes.
        
        if isinstance(df, dict):
            # If data is passed as a dictionary of dataframes, access the relevant dataframe
            df = df.get(self.selected_country, pd.DataFrame())
        
        # Filter by year range if necessary
        if self.selected_year_range:
            df = df[(df['year'] >= self.selected_year_range[0]) & (df['year'] <= self.selected_year_range[1])]
        
        return df

    # def display_heatmap(self):
    #     """Generate and display a heatmap for the dataset."""
    #     if self.filtered_df is not None:
    #         st.subheader("Heatmap of columns")
            
    #         # Radio button to toggle between world (no filter) and selected countries
    #         data_source = st.radio("Select data to display:", ["World (No Filter)", "Selected Countries"])

    #         # Choose the appropriate DataFrame based on the user's selection
    #         heatmap_data = self.filtered_df

    #         # Only include numerical columns for correlation matrix
    #         numerical_cols = heatmap_data.select_dtypes(include='number')
            
    #         if numerical_cols.shape[1] > 1:
    #             # Calculate the correlation matrix
    #             correlation_matrix = numerical_cols.corr()
    #             st.write("Correlation Matrix:")
                
    #             # Checkbox to show/hide raw data
    #             show_raw_data = st.checkbox("Show Raw Data", value=False)
    #             if show_raw_data:
    #                 st.dataframe(heatmap_data)  # Display the raw data table
                
    #             # Create the heatmap
    #             fig, ax = plt.subplots(figsize=(10, 8))
    #             # sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
                
    #             st.pyplot(fig, use_container_width=False)
    #         else:
    #             st.warning("Not enough numerical columns in the dataset to create a heatmap.")
    #     else:
    #         st.error("No data available to display a heatmap.")
    
    def display_heatmap(self):
      if len(self.selected_country) == 0:
        """Generate and display a heatmap for the dataset using Plotly."""
        if self.filtered_df is not None:
            st.subheader("Heatmap of columns")
            
            # Radio button to toggle between world (no filter) and selected countries
            data_source = st.radio("Select data to display:", ["World (No Filter)", "Selected Countries"])
            
            tab1, tab2 = st.tabs(["Correlation Heatmap", "Raw Data"])
            
            # World data heatmap
            if data_source == "World (No Filter)":
                # Choose the appropriate DataFrame based on the user's selection
                heatmap_data = self.filtered_df
                
                # Only include numerical columns for correlation matrix
                numerical_cols = heatmap_data.select_dtypes(include='number')
                
                if numerical_cols.shape[1] > 1:
                    # Calculate the correlation matrix
                    correlation_matrix = numerical_cols.corr()
                    # st.write("Correlation Matrix:")
                    
                    # Checkbox to show/hide raw data
                    # show_raw_data = st.checkbox("Show Raw Data", value=False)
                    # if show_raw_data:
                    tab2.dataframe(heatmap_data)  # Display the raw data table
                       
                    with tab1: 
                        # Create the heatmap with Plotly
                        fig = go.Figure(data=go.Heatmap(
                            z=correlation_matrix.values,
                            x=correlation_matrix.columns,
                            y=correlation_matrix.columns,
                            colorscale='RdBu',  # Color scale
                            colorbar=dict(title="Correlation"),
                            hoverongaps=False  # Hide gaps on hover,
                        ))
                        
                        # Update layout for better visualization
                        fig.update_layout(
                            title="Correlation Heatmap",
                            xaxis_title="Columns",
                            yaxis_title="Columns",
                            autosize=True,
                            height=700,  # Set height of the heatmap
                            width=900   # Set width of the heatmap
                        )
                        
                        # Display the Plotly figure
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Not enough numerical columns in the dataset to create a heatmap.")
                    
            # Selected countries heatmap
            else:
                if len(self.selected_country) == 0:
                    st.warning("Please select at least one country to use this feature")
                else:
                    heatmap_data = self.filtered_df[self.filter_data()["country"].isin(self.selected_country)]
                    # Only include numerical columns for correlation matrix
                    numerical_cols = heatmap_data.select_dtypes(include='number')
                    
                    if numerical_cols.shape[1] > 1:
                        # Calculate the correlation matrix
                        correlation_matrix = numerical_cols.corr()
                        # st.write("Correlation Matrix:")
                        
                        # Checkbox to show/hide raw data
                        # show_raw_data = st.checkbox("Show Raw Data", value=False)
                        # if show_raw_data:
                        tab2.dataframe(heatmap_data)  # Display the raw data table
                            
                        with tab1:
                            # Create the heatmap with Plotly
                            fig = go.Figure(data=go.Heatmap(
                                z=correlation_matrix.values,
                                x=correlation_matrix.columns,
                                y=correlation_matrix.columns,
                                colorscale='RdBu',  # Color scale
                                colorbar=dict(title="Correlation"),
                                hoverongaps=False  # Hide gaps on hover,
                            ))
                            
                            # Update layout for better visualization
                            fig.update_layout(
                                title="Correlation Heatmap",
                                xaxis_title="Columns",
                                yaxis_title="Columns",
                                autosize=True,
                                height=700,  # Set height of the heatmap
                                width=900   # Set width of the heatmap
                            )
                            
                            # Display the Plotly figure
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Not enough numerical columns in the dataset to create a heatmap.")
        else:
            st.error("No data available to display a heatmap.")

    def display_scatterplot(self):
        """Generate and display scatterplot with OLS trendline for the selected data."""
        if self.filtered_df is not None:
            st.subheader("Scatterplot with OLS Trendline")

            # Dropdown for X and Y-axis selection
            col1, col2 = st.columns([1,1])
            
            x_variable = col1.selectbox("Select X-axis", self.filtered_df.select_dtypes(include='number').columns, index=0, key="scatter_x")
            y_variable = col2.selectbox("Select Y-axis", self.filtered_df.select_dtypes(include='number').columns, index=1, key="scatter_y")

            fig = go.Figure()

            # Add scatter points for each country
            for country in self.filtered_df[self.filter_data()["country"].isin(self.selected_country)]["country"].unique():
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
