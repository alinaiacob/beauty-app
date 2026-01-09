from utils.data_loader import load_products_data
from utils.text_analysis import combineSentimentScoreReview
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def getStatisticsForProduct(product_df):
    df = load_products_data()
    category = product_df["primary_category"].iloc[0]
    product_same_category = df[df["primary_category"] == category]
    mean_same_category = product_same_category["rating"].mean()
    return mean_same_category

def getReviewsFromCsv(fileName, product_id):
    reviews_df = pd.read_csv(fileName)
    reviews_df["product_id"] = reviews_df["product_id"].astype(str)
    product_id =str(product_id)
    reviews_about_product_df = reviews_df[reviews_df["product_id"]==product_id]
    return reviews_about_product_df

def getReviewsAboutProducts(product_id):
    firstReviews_df = getReviewsFromCsv("./dataset/reviews_0-250.csv", product_id)
    secondReviews_df = getReviewsFromCsv("./dataset/reviews_500-750.csv", product_id)
    thirdReviews_df = getReviewsFromCsv("./dataset/reviews_1250-end.csv", product_id)
    forthReviews_df = getReviewsFromCsv("./dataset/reviews_1250-end.csv", product_id)

    dfs = [firstReviews_df, secondReviews_df, thirdReviews_df, forthReviews_df]

    df = pd.concat(dfs, ignore_index=True)
    return df

def chartPlotProduct(reviews):
    all_reviews_scores_df = combineSentimentScoreReview()
    plt.figure(figsize=(12, 6))
    plt.title("Line chart for reviews and scores")
    plt.xlabel(all_reviews_scores_df[""])
