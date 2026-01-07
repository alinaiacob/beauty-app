import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import re
import ast

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

def expand_variants(ingredients_list):
    result = []

    i = 0
    while i < len(ingredients_list) - 1:
        name = ingredients_list[i].replace(':', '').strip()
        ing_str = ingredients_list[i + 1]

        ingredients = [
            ing.strip().lower()
            for ing in ing_str.split(',')
            if ing.strip()
        ]

        result.append({
            'variant_name': name,
            'ingredients': ingredients
        })

        i += 2

    return result


def parse_ingredients(row):
    if pd.isna(row):
        return []

    if isinstance(row, list):
        return row

    row = str(row).strip()

    if row.startswith('[') and row.endswith(']'):
        try:
            parsed = ast.literal_eval(row)
            if isinstance(parsed, list):
                return [i.lower().strip() for i in parsed]
        except Exception:
            pass

    val = row.lower()
    val = re.sub(r'\.$', '', val)
    return [i.strip() for i in val.split(',')]

def getIngredients(df):
    df["ingredients_list"] = df["ingredients"].apply(parse_ingredients)
    df["variants"] = df["ingredients_list"].apply(expand_variants)
    df = explode(df)
    df["ingredient"] = df["ingredient"].apply(clean_ingredient)
    return df


def clean_ingredient(ing):
    ing = ing.lower().strip()
    ing = re.sub(r"[.:]+$","",ing)
    ing = re.sub(r"\s+","",ing)
    return ing


def explode(df):
    # 1️⃣ explode variante
    df_variants = df.explode("variants").dropna(subset=["variants"])

    # 2️⃣ scoatem câmpurile din dict
    df_variants["variant_name"] = df_variants["variants"].apply(lambda x: x["variant_name"])
    df_variants["ingredient"] = df_variants["variants"].apply(lambda x: x["ingredients"])

    # 3️⃣ explode ingrediente
    df_variants = df_variants.explode("ingredient").dropna(subset=["ingredient"])

    return df_variants






