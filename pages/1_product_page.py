import pandas as pd
import numpy as np
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.data_loader import load_products_data

df = load_products_data()

st.title("Page for a single product")
product_names = set(df['product_name'].tolist())
print("product_names", product_names)

brand_names = set(df["brand_name"].tolist())
print("brand names ", brand_names)


brand_name = st.selectbox(
    "Choose a brand name to analyze",
    brand_names
)
st.write(f"You choose to analyze the {brand_name}")

products_from_brand = df[df["brand_name"]==brand_name]
products_names = products_from_brand["product_name"]


product_name = st.selectbox(
    "Choose a product to analyze",
    products_names
)

if product_name:
    st.session_state["selected_product"]  = product_name
    st.session_state["selected_brand"] = brand_name

    st.write("You have selected a product. Checkout the product details")

