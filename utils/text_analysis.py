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
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import hdbscan

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

        pos_phrases = []
        for text in positive:
            pos_phrases.extend(extract_opinion_phrases(text))

        neg_phrases = []
        for text in negative:
            neg_phrases.extend(extract_opinion_phrases(text))

        top_pos = Counter(pos_phrases).most_common(20)
        top_neg = Counter(neg_phrases).most_common(20)

        return top_pos, top_neg


def extract_opinion_phrases(text):
    doc = nlp(text)
    phrases = []

    for token in doc:
        if token.pos_ == "ADJ":
            phrases.append(token.lemma_)

        if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
            phrases.append(f"{token.lemma_} {token.head.lemma_}")

        if token.pos_ == "VERB":
            for child in token.children:
                if child.pos_ == "ADJ":
                    phrases.append(f"{token.lemma_} {child.lemma_}")

    return phrases

ASPECTS = {
    "fragrance": [
        "smell", "scent", "fragrance", "perfume", "odor"
    ],
    "texture": [
        "texture", "greasy", "oily", "thick", "light",
        "sticky", "smooth", "silky"
    ],
    "irritation": [
        "irritation", "burn", "burning", "sting",
        "redness", "rash", "itch", "breakout"
    ],
    "hydration": [
        "dry", "hydrating", "moisturizing", "moisture",
        "dehydrated"
    ],
    "price": [
        "price", "expensive", "cheap", "worth", "value"
    ],
    "performance": [
        "remove", "cleans", "works", "effective",
        "cleansing"
    ]
}

import nltk
nltk.download("punkt")

from nltk.tokenize import sent_tokenize

def extract_aspect_sentences(review):
    sentences = sent_tokenize(review.lower())
    aspect_sentences = []

    for sent in sentences:
        for aspect, keywords in ASPECTS.items():
            if any(k in sent for k in keywords):
                aspect_sentences.append({
                    "aspect":aspect,
                    "sentence":sent
                })
    return aspect_sentences

def score_sentence(sentence):
    return sia.polarity_scores(sentence)["compound"]

def aspect_based_sentiment(reviews_df):
    rows = []
    for _, row in reviews_df.iterrows():
        aspects = extract_aspect_sentences(row["review_text"])

        for item in aspects:
            score = score_sentence(item["sentence"])
            rows.append({
                "product_id": row["product_id"],
                "review_id":row.get("review_id"),
                "aspect": item["aspect"],
                "sentence":item["sentence"],
                "sentiment_score": score
            })
        return pd.DataFrame(rows)

def aggregate_aspects(absa_df):
    return (
        absa_df
        .groupby(["product_id"],"aspect")
        .agg(
            avg_sentiment = ("sentiment_score", "mean"),
            mentions=("sentiment_score", "count")

        )
        .reset_index()
        .sort_values("avg_sentiment")
    )

def clean_review_for_cluster(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "",text)
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()

#sentence transformers
def cluster(reviews_df):
 model = SentenceTransformer("all-MiniLM-L6-v2")
 reviews_df["cluster_text"] = reviews_df["review_text"].apply(clean_review_for_cluster)
 embeddings = model.encode(
    reviews_df["cluster_text"].tolist(),
     show_progress_bar=True
)

 pca = PCA(n_components=20, random_state=42)
 X_reduced = pca.fit_transform(embeddings)
 kmeans = KMeans(n_clusters=5, random_state=42)
 clusters = kmeans.fit_predict(X_reduced)
 reviews_df["cluster"] = clusters


 clusterer_db = hdbscan.HDBSCAN(
     min_cluster_size=30,
     metric="euclidean"
 )
 clusters_db = clusterer_db.fit_predict(X_reduced)
 reviews_df["cluster_db"] = clusters_db
 return reviews_df





