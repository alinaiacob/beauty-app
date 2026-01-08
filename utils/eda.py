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

def addOtherValueCol(df, col):
    top10 = df[col].value_counts().head(10).index

    new_col = col + "_featured"
    df[new_col] = df[col].where(df[col].isin(top10), "other")

    return df

def pieChartVariable(df, col):
    df = addOtherValueCol(df, col)
    plt.figure(figsize=(16,10))
    fig, ax= plt.subplots()
    ax.set_title(f"Pie chart for {col}")
    ax.legend()
    col_renamed = col+"_featured"
    ax.pie(df[col_renamed].value_counts(), labels=df[col_renamed].value_counts().index)
    st.pyplot(fig)

def barChartVariable(df, col):
     plt.figure(figsize=(16,10))
     fig, ax = plt.subplots()
     ax.set_title(f"Bar chart for {col}")
     ax.legend()
     ax.bar(df[col].value_counts(),df[col].value_counts().index, width=0.6)
     plt.xticks(rotation=45, ha="right")
     st.pyplot(fig)