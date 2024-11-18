import streamlit as st

class CustomMarkdown:
    def __init__(self):
        pass
    
    def button_style(self, margin_top: str, padding: str):
        """Method to adjust button position and padding via custom CSS"""
        custom_css = f"""
        <style>
            .stButton button {{
                margin-top: {margin_top};  /* Adjust the top margin to move the button down */
                padding: {padding};  /* Adjust padding dynamically */
            }}
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)


    def polynomial_degree_slider(self, tab, default_degree: int = 4):
        """Method to display the Polynomial Degree slider with a question mark tooltip"""
        with tab:
            st.markdown(
                """
                <span style="font-size: 18px;">Select Polynomial Degree</span>
                <span style="cursor: pointer; color: blue;" title="The degree of the polynomial affects how much the model will fit the data. A higher degree may cause overfitting.">❓</span>
                """, 
                unsafe_allow_html=True
            )
            degree = st.slider("Select Polynomial Degree", 2, 10, default_degree)
            return degree