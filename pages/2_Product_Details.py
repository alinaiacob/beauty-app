import streamlit as st
from utils import load_products_data


st.title("Product Details Page")


product = st.session_state.get("selected_product")
brand = st.session_state.get("selected_brand")


if not product or not brand:
    st.warning("You should choose a product from Products Page")
    st.stop()


