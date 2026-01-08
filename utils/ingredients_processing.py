import pandas as pd
import re
import ast
from problematic_ingredients import RISK_WEIGHTS

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