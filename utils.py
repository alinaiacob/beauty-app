import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import re
import ast
from problematic_ingredients import PROBLEMATIC_ALCOHOLS, FRAGRANCE_ALLERGENS, CONTROVERSIAL_FILTERS, RISK_WEIGHTS



def load_products_data():
    df = pd.read_csv("./dataset/product_info.csv")
    return df
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
    df, variants_risk = explode_variants(df)
    df["ingredient"] = df["ingredient"].apply(clean_ingredient)
    return df, variants_risk


def clean_ingredient(ing):
    ing = ing.lower().strip()
    ing = re.sub(r"[.:]+$","",ing)
    ing = re.sub(r"\s+","",ing)
    return ing


def explode_variants(df):
    df_variants = df.explode("variants").dropna(subset=["variants"])

    df_variants["variant_name"] = df_variants["variants"].apply(lambda x: x["variant_name"])
    df_variants["ingredient"] = df_variants["variants"].apply(lambda x: x["ingredients"])

    df_variants = df_variants.explode("ingredient").dropna(subset=["ingredient"])

    df_variants["ingredient"] = df_variants["ingredient"].str.lower().str.strip()
    df_variants["ingredient_class"] = df_variants["ingredient"].apply(classify_ingredient)
    df_variants["ingredient_risk"] = df_variants["ingredient_class"].map(RISK_WEIGHTS).fillna(0)

    variant_risk = (
        df_variants
        .groupby(["variant_name", "product_id"])
        .agg(
            total_ingredients=("ingredient", "count"),
            risk_score=("ingredient_risk", "sum"),
            fragrance_count=("ingredient_class", lambda x: (x=="fragrance_allergen").sum()),
            alcohol_count=("ingredient_class", lambda x: (x=="problematic_alcohol").sum()),
            filters_count=("ingredient_class", lambda x: (x=="controversial_filters").sum())
        )
        .reset_index()
    )

    variant_risk["risk_density"] = (
        variant_risk["risk_score"] / variant_risk["total_ingredients"]
    )

    return df_variants, variant_risk



def classify_ingredient(ingredient):
     if ingredient in PROBLEMATIC_ALCOHOLS:
         return "problematic_alcohol"
     if ingredient in FRAGRANCE_ALLERGENS:
         return "fragrance_allergen"
     if ingredient in CONTROVERSIAL_FILTERS:
         return "controversial_filters"

     return "ok"


def getStatisticsForProduct(product_df):
    rating = product_df["rating"]
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





