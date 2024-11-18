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

# Example usage:
custom_markdown = CustomMarkdown()
custom_markdown.button_style(margin_top="50px", padding="8px 16px")
