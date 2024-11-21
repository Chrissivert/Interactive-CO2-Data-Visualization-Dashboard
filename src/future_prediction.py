import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import src.service as s


class FuturePrediction:
    def __init__(self, selected_countries, years_to_predict, scale_type, dataframe):
        self.selected_countries = selected_countries
        self.years_to_predict = years_to_predict
        self.scale_type = scale_type
        self.dataframe = dataframe

    def predict_with_model(self, model):
        predictions_fig = go.Figure()
        country_data = self.dataframe[self.dataframe["country"].isin(self.selected_countries)]

        # Assuming the metric is 'co2_per_capita' as it was in your previous implementation
        selected_metric = "co2_per_capita"
        
        for country in self.selected_countries:
            country_specific_data = country_data[country_data["country"] == country]
            country_specific_data = country_specific_data[["year", selected_metric]].dropna()

            if country_specific_data.empty:
                st.warning(f"No valid data for predictions for: {country}")
                continue

            future_years, predictions = s.predict_future_values_with_models(
                country_specific_data, selected_metric, self.years_to_predict, model
            )

            predictions_fig.add_trace(go.Scatter(
                x=country_specific_data["year"],
                y=country_specific_data[selected_metric],
                mode="lines",
                name=f"Historical {selected_metric} ({country})"
            ))
            predictions_fig.add_trace(go.Scatter(
                x=future_years.flatten(),
                y=predictions,
                mode="lines+markers",
                name=f"Predicted {selected_metric} ({country})"
            ))

        return predictions_fig

    def plot(self, tab, model, special_function=None):
        with tab:
            special_function
            log_scale = self.scale_type == "Logarithmic"
            fig_pred = self.predict_with_model(model)
            fig_pred.update_layout(
                title=f"Prediction for Next {self.years_to_predict} Years",
                xaxis_title="Year",
                yaxis_title="co2_per_capita",  # Assuming we're using 'co2_per_capita'
                legend_title="Country",
                yaxis_type='log' if log_scale else 'linear'
            )
            st.plotly_chart(fig_pred, use_container_width=True)