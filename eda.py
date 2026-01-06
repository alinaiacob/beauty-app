import pandas as pd
import numpy as np
import streamlit as st

products_df = pd.read_csv("./dataset/product_info.csv")


columns = products_df.columns.tolist()
print(columns)
num_prod = len(products_df['product_id'].unique())
print("num prod", num_prod)
num_brands = len(products_df["brand_id"].unique())
print("num brands", num_brands)
print("num of products", products_df['product_id'].unique())
#columns used for analysis
products_df = products_df.drop(columns=['product_id','brand_id'])
print("products_df after drop cols\n",products_df)
print("cols ",products_df.columns.tolist())

print(products_df.describe())

st.title("Beauty Reviews Analyzer App")
st.text(f"We analyzed {num_prod} products from ${num_brands}. We aim ")
