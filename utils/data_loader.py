import pandas as pd

def load_products_data():
    df = pd.read_csv("./dataset/product_info.csv")
    return df