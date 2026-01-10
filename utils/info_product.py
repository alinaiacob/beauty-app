from utils.data_loader import load_products_data
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events

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


def plotReviewsScore(plot_df):
    # 1️⃣ Scatter pentru reviews (CLICKABLE)
    fig = px.scatter(
        plot_df,
        x="submission_time",
        y="polarity_score",
        labels={
            "submission_time": "Review date",
            "polarity_score": "Sentiment polarity"
        },
        opacity=0.4
    )

    fig.update_traces(marker=dict(size=6))

    # 2️⃣ Linie de smoothing (TREND)
    plot_df["polarity_smooth"] = plot_df["polarity_score"].rolling(10).mean()

    fig.add_scatter(
        x=plot_df["submission_time"],
        y=plot_df["polarity_smooth"],
        mode="lines",
        name="Smoothed sentiment",
        line=dict(width=3)
    )

    fig.update_layout(
        hovermode="closest",
        yaxis=dict(range=[-1, 1])
    )

    # 3️⃣ CLICK HANDLER — pe figura FINALĂ
    selected_points = plotly_events(
        fig,
        click_event=True,
        hover_event=False,
        select_event=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # 4️⃣ Afișezi review-ul
    if selected_points:
        idx = selected_points[0]["pointIndex"]
        selected_review = plot_df.iloc[idx]

        st.divider()
        st.subheader("Selected review")
        st.write(selected_review["review_text"])

        score = selected_review["polarity_score"]
        if score > 0.5:
            st.success("Positive sentiment")
        elif score < -0.3:
            st.error("Negative sentiment")
        else:
            st.info("Neutral / mixed sentiment")
