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
    "Choose a product to analyze",
    product_names
)
st.write(f"You choose to analyze the {option}")

