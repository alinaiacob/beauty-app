import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import spacy
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation

nltk.download("vader_lexicon")
nlp =spacy.load("en_core_web_sm", disable=["ner", "parser"])

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

def clean_text(text):
    if text:
     text = text.lower()
     text = re.sub(r"[^a-z\s]", "", text)

     doc = nlp(text)
     tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and len(token) > 2
     ]
     return " ".join(tokens)
    else:
        return ""

def top_words(texts, n=20):
    words = " ".join(texts).split()
    return Counter(words).most_common(n)


def topPositiveNegativeNgrams(reviews_df):
    reviews_df["clean_review"] = reviews_df["review_text"].apply(clean_text)
    positive = reviews_df[reviews_df["polarity_score"] > 0.4]["clean_review"]
    negative = reviews_df[reviews_df["polarity_score"] < -0.3]["clean_review"]

    top_pos = top_words(positive)
    top_neg = top_words(negative)

    vectorizer = CountVectorizer(
        ngram_range=(2, 3),
        min_df=5
    )

    X = vectorizer.fit_transform(reviews_df["clean_review"])
    ngrams = vectorizer.get_feature_names_out()

    sentiment_corr = np.asarray(X.T.dot(reviews_df["polarity_score"]))
    top_ngrams = sorted(
        zip(ngrams, sentiment_corr),
        key=lambda x: x[1],
        reverse=True
    )[:20]
    return top_pos, top_neg, top_ngrams
