import pandas as pd
import numpy as np
import streamlit as st
from utils.data_loader import load_reviews
from utils.text_analysis import cluster

st.title("Cluster analysis for reviews")
all_reviews_df = load_reviews()
all_reviews_df = cluster(all_reviews_df)
print(all_reviews_df["cluster"])
st.write("Reviews grouped in clusters ", all_reviews_df["reviews_text"],all_reviews_df["cluster"])
