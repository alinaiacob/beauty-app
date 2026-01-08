import streamlit as st
from utils.data_loader import load_products_data
from utils.info_product import  getStatisticsForProduct, getReviewsAboutProducts

st.title("Product Details Page")


product = st.session_state.get("selected_product")
brand = st.session_state.get("selected_brand")


if not product or not brand:
    st.warning("You should choose a product from Products Page")
    st.stop()


df = load_products_data()
product_df = df[
    (df["brand_name"]==brand) &
    (df["product_name"]==product)
]

st.write("Info for selected product", product_df)
st.write("Reviews ", product_df['reviews'])
st.write("Primary category", product_df["primary_category"])
st.write("Secondary category", product_df["secondary_category"])
st.write("Rating for this product ", product_df['rating'])

mean_rating = getStatisticsForProduct(product_df)
st.write("Mean rating from other products from same category", mean_rating)

product_id = product_df["product_id"].iloc[0]

reviews = getReviewsAboutProducts(product_id)
st.write("Reviews ", reviews)
#st.write("Reviews for products ", reviews["review_text"])