import pandas as pd
import numpy as np

def replace_to_empty(df):
    df.replace(
        to_replace=[0, False, None, np.nan], 
        value='',
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

def concat_adddress(df):
    def concat_str(col):
        return np.where(
            df[col].str.strip() != '', 
            ' '+df[col], 
            ''
        )

    address_series = df['시도명'].copy()
    address_series += concat_str('시군구명')
    address_series += concat_str('법정읍면')

    address_series += ' ' + df['도로명'] + ' ' + df['건물본번']

    address_series += np.where(
        df['건물부번'].str.strip() != '', 
        '-' + df['건물부번'], 
        ''
    )

    return address_series

def process_data(df):
    replace_to_empty(roadname_df)
    roadname_df = roadname_df.astype(str)

    # 법정읍면동명-> 법정동, 법정읍면으로 분리
    roadname_df = split_eup_myeon_dong(roadname_df)
    roadname_df = roadname_df.drop(columns=['법정읍면동명'])

    # 도로명주소 
    roadname_df['도로명주소'] = concat_adddress(roadname_df)