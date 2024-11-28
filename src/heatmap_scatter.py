import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class HeatmapScatter:
    def __init__(self, dataframes):
        """
        Initialize the Visualization class with loaded dataframes.
        
        Args:
        dataframes (dict): A dictionary where keys are dataset names and values are pandas DataFrames.
        """
        self.dataframes = dataframes
        self.combined_df = self.merge_dataframes()

    def merge_dataframes(self):
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
        
        return merged_df

    def display_heatmap(self):
        """Generate and display a single heatmap for the combined dataset."""
        if self.combined_df is not None:
            st.subheader("Heatmap of Combined Dataset")
            numerical_cols = self.combined_df.select_dtypes(include='number')
            if numerical_cols.shape[1] > 1:
                correlation_matrix = numerical_cols.corr()
                st.write("Correlation Matrix:")
                st.dataframe(correlation_matrix)
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Not enough numerical columns in the combined dataset to create a heatmap.")
        else:
            st.error("No data available to display a heatmap.")

    def display_scatterplot(self):
        """Display a single scatterplot for the combined dataset."""
        if self.combined_df is not None:
            st.subheader("Scatterplot for Combined Dataset")
            numerical_cols = self.combined_df.select_dtypes(include='number').columns.tolist()
            if len(numerical_cols) >= 2:
                col_x = st.selectbox("Select X-axis", numerical_cols, key="scatter_x")
                col_y = st.selectbox("Select Y-axis", numerical_cols, key="scatter_y")
                if col_x and col_y:
                    scatter_fig = px.scatter(self.combined_df, x=col_x, y=col_y,
                                             title=f"{col_x} vs {col_y}",
                                             labels={"x": col_x, "y": col_y})
                    st.plotly_chart(scatter_fig)
            else:
                st.warning("Not enough numerical columns in the combined dataset to create a scatterplot.")
        else:
            st.error("No data available to create a scatterplot.")
