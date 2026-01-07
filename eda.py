from array import array

import pandas as pd
import numpy as np
import streamlit as st
from utils import sum_nan_values, histogramVariable, pieChartVariable, barChartVariable, getIngredients

products_df = pd.read_csv("./dataset/product_info.csv")



num_prod = len(products_df['product_id'].unique())
print("num prod", num_prod)
num_brands = len(products_df["brand_id"].unique())
print("num brands", num_brands)
print("num of products", products_df['product_id'].unique())
#columns used for analysis
products_df = products_df.drop(columns=['product_id','brand_id'])
print("products_df after drop cols\n",products_df)
columns = products_df.columns.tolist()
print(columns)
print("cols ",products_df.columns.tolist())

print(products_df.describe())
statistics = products_df.describe()
print("type of products_df", type(statistics))
print("res for ", statistics["loves_count"])
numeric_columns = statistics.columns.tolist()
print("numeric cols", numeric_columns)
st.title("Beauty Reviews Analyzer App")
st.text(f"We analyzed {num_prod} products from {num_brands}. We aim ")
st.text(f"The columns used for this research {columns}")

option = st.selectbox(
    "Choose a column to analyze",
    numeric_columns
)
st.write("You select", option)
st.write("Statistics for your option ", statistics[option])

st.text(f"Bar chart for {option}")
barChartVariable(products_df, option)


sum_nan = sum_nan_values(products_df)
print(sum_nan)

null_percentage = (sum_nan/len(products_df))*100
print("null percentage\n ", null_percentage)


st.text(f"Null percentage for variables {null_percentage}")
#histogramVariable(products_df, option)

non_numeric_cols = products_df.select_dtypes(include=[object]).columns.tolist()
print("non-numeric cols ", non_numeric_cols)
# for non_num_col in non_numeric_cols:
#     print(f"for col {non_num_col}",set(products_df[non_num_col].values.tolist()))

st.text("Choose a categorical variable to have a look about dataset")
option_non_numeric = st.selectbox(
    "Choose a variable",
    non_numeric_cols
)

pieChartVariable(products_df, option_non_numeric)


products_df = getIngredients(products_df)
print(products_df["ingredients_list"])
print(products_df['ingredients_list'])
print(products_df['variants'])