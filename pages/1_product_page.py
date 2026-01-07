import pandas as pd
import numpy as np
import streamlit as st

df = pd.read_csv("./dataset/product_info.csv")

st.title("Page for a single product")
product_names = set(df['product_name'].tolist())
print("product_names", product_names)

brand_names = set(df["brand_name"].tolist())
print("brand names ", brand_names)


option = st.selectbox(
    "Choose a brand name to analyze",
    brand_names
)
st.write(f"You choose to analyze the {option}")
products_from_brand = df[df["brand_name"]==option]
products_names = products_from_brand["product_name"]
print("product_names")
st.write(f"All products from {option} ", products_names)

