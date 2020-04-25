from src.params import *
from src.config import *


def get_script_data():
    df_script = pd.DataFrame()
    return df_script


def clean_script_data(df):
    return df


if __name__ == '__main__':
    df = get_script_data()
    print(df)
    df_clean = clean_script_data(df)
    print(df)
