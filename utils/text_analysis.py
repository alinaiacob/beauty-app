import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(reviews):
    scores = [sia.polarity_scores(t)["compound"] for t in reviews if isinstance(t, str)]

    if not scores:
        return None

    return {
        "mean_sentiment": round(sum(scores)/len(scores), 3),
        "positive_ratio": sum(s > 0.05 for s in scores) / len(scores),
        "negative_ratio": sum(s < 0.05 for s in scores) / len(scores),
    }

def add_sentiment_scores(reviews_df):
    reviews_df = reviews_df.copy()

    reviews_df["polarity_score"] = reviews_df["review_text"].astype(str).apply(
        lambda x: sia.polarity_scores(x)["compound"]
    )

    return reviews_df

def extract_keywords(texts, top_n=10):
    texts = [t for t in texts if isinstance(t, str)]

    if len(texts) < 3:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000
    )

    X = vectorizer.fit_transform(texts)
    scores = X.mean(axis=0).A1
    terms = vectorizer.get_feature_names_out()

    top_idx = scores.argsort()[::-1][:top_n]
    return [terms[i] for i in top_idx]