import pandas as pd

def load_products_data():
    df = pd.read_csv("./dataset/product_info.csv")
    return df

def load_reviews():
    first_df = pd.read_csv("./dataset/reviews_0-250.csv")
    second_df = pd.read_csv("./dataset/reviews_250-500.csv", engine="python", on_bad_lines="skip")
    third_df = pd.read_csv("./dataset/reviews_500-750.csv")
    fourth_df = pd.read_csv("./dataset/reviews_1250-end.csv")
    fifth_df = pd.read_csv("./dataset/reviews_750-1250.csv",  engine="python", on_bad_lines="skip")
    all_dfs = [first_df, second_df, third_df, fourth_df, fifth_df]
    return all_dfs