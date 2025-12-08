import pandas as pd
import sys, os, re
from utils import *

def read_csv(file_path):
    try:
        return pd.read_csv(file_path, encoding='euc-kr')
    except Exception as e:
        print(f"csv파일 읽기 오류({file_path}): {e}")
        sys.exit(1)

def split_address(data, return_type=0):
    pattern = r"(?:[^\s]+(?:개|길|리|로|동|가)\s*"+\
               "(?:\d*[가-힣]*(?:개|길|리|로|동|가))?)"+\
               "(?:\s+)?((지하)*|(산)*)(?:\s+)?(\d+(?:-\d*)?)" 
    match = re.search(pattern, data)

    if match is not None:
        idx = match.span()[-1]
        address = data[:idx].strip()          # 도로명주소
        detailed_address = data[idx:].strip() # 상세주소

        if return_type == 0: return address, detailed_address
        elif return_type == 1: return address
        elif return_type == 2: return detailed_address
    else: return data if return_type == 1 else data, ''


def read_target_data():
    target_path = get_config_data("paths", "target_data")
    target_file_list = os.listdir(target_path)
    taraget_col = get_config_data("target_col", "roadname")

    for filename in target_file_list:
        file_df = read_csv(os.path.join(target_path, filename))

        for col in taraget_col:
            file_df[col]

        break