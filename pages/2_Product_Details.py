import streamlit as st
import pandas as pd
from utils.data_loader import load_products_data
from utils.info_product import  getStatisticsForProduct, getReviewsAboutProducts, plotReviewsScore
from utils.text_analysis import analyze_sentiment, extract_keywords, add_sentiment_scores

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

reviews_df = getReviewsAboutProducts(product_id)
reviews_df["submission_time"] = pd.to_datetime(reviews_df["submission_time"])

sentiment = analyze_sentiment(reviews_df["review_text"])
st.write("Reviews for selected product ", reviews_df)
keywords = extract_keywords(reviews_df["review_text"])


st.subheader("Text analysis - Reviews")

if sentiment:
    mean_sentiment, positive_ratio, negative_reviews, scores = st.columns(4)
    mean_sentiment.metric("Mean sentiment ", sentiment["mean_sentiment"])
    positive_ratio.metric("Positive reviews ", sentiment["positive_ratio"])
    negative_reviews.metric("Negative reviews ", sentiment["negative_ratio"])

if keywords:
    st.write("Most frequent keywords")
    st.write(",".join(keywords))

result_df = add_sentiment_scores(reviews_df)

plot_df = (
    result_df
    .sort_values("submission_time")
    .reset_index(drop=True)
    [["submission_time","polarity_score","review_text"]]

)

plotReviewsScore(plot_df)
