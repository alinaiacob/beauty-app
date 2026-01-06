import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def sum_nan_values(df):
    return df.isna().sum()

def histogramVariable(df, col):
    plt.figure(figsize=(12, 6))
    fig, ax = plt.subplots()
    ax.set_title(f"Histogram for {col}")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Value")
    ax.hist(df[col].values, bins=30)
    st.pyplot(fig)

def pieChartVariable(df, col):
    plt.figure(figsize=(12,6))
    fig, ax= plt.subplots()
    ax.set_title(f"Pie chart for {col}")
    ax.legend()
    ax.pie(df[col].value_counts(), labels=df[col].value_counts().index )
    st.pyplot(fig)

def addOtherValueCol(df, col):
    elem = df[col].value_counts().tolist()
    print(elem)