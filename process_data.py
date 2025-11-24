import pandas as pd
import numpy as np

def replace_to_nan(df):
    df.replace(
        to_replace=[0, False, None], 
        value=np.nan,
        inplace=True)
    

def split_eup_myeon_dong(df, col="법정읍면동명"):
    dong_end_word = ('동', '로', '가')
    eup_myeon_word = ('읍', '면')

    def make_new_col(end_word, new_col, df):
        mask = df[col].str.endswith(end_word, na=False)
        df[new_col] = np.where(
            mask, 
            df[col], 
            np.nan)
        
    make_new_col(dong_end_word, '법정동', df)
    make_new_col(eup_myeon_word, '법정읍면', df)

    return df


def process_data(df):
