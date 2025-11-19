import pandas as pd
from tqdm import tqdm
import os, json
from utils import *

class ReadCorrectData:
    CORRECT_DATA_PATH = "./data/correct_data"  # 202510_도로명주소 한글_전체분 / 2025_상세주소 표시_전체분
    COL_MAPPING_PATH = "./data/col_mapping.json"
    ROADNAME_FILE_NAME = "도로명주소"
    DETAILED_FILE_NAME = "상세주소"
    ROADNAME_DEL_WORD = "jibun"   # 도로명주소 한글- jibun: 지번 주소
    DETAILED_DEL_WORD = "rnspbt"  # 상세주소 표시- rnspbd: 시군구용, rnspbt: 건축물대장

    def __init__(self):
        self._roadname_path = None
        self._detailed_path = None

        self.roadname_col = None
        self.detailed_col = None

    # 컬럼명 찾기
    def _load_column_mappings(self):
        data = load_json(self.CORRECT_DATA_PATH)
        roadname_col, detailed_col = data['roadname'], data['detailed']

        def str_to_int(col):
            col = {int(k):v for k, v in col.items()}
            return col
        
        return str_to_int(roadname_col), str_to_int(detailed_col)

    # 도로명주소 한글. 상세주소 표시. 폴더 이름 찾기
    def fild_folder_name(self):
        for name in os.listdir(self.CORRECT_DATA_PATH):
            if self.ROADNAME_FILE_NAME in name: roadname_folder_name = name
            elif self.DETAILED_FILE_NAME in name: detailed_folder_name = name

        return roadname_folder_name, detailed_folder_name
    
    def _find_folder_path(self):
        roadname_folder, detailed_folder = self.fild_folder_name()
        self._roadname_path = os.path.join(self.CORRECT_DATA_PATH, roadname_folder)
        self._detailed_path = os.path.join(self.CORRECT_DATA_PATH, detailed_folder)

    # 타겟 파일리스트 찾기
    def find_filelist(self, folder_path, word):
        filelist = os.listdir(folder_path)
        filelist = [filename for filename in filelist if word not in filename]
        
        return filelist
    
    # 데이터 파일 읽기
    def read_data(self, folder_path, filelist, col, data):
        df = pd.DataFrame([])

        for filename in tqdm(filelist, desc=f"{data} 데이터 읽는 중"):
            file = os.path.join(folder_path, filename)
            new_df = pd.read_csv(file, encoding="cp949", sep="|", header=None, low_memory=False)
            new_df.rename(columns=col, inplace=True)
            df = pd.concat([df, new_df])

        return df

    # 메인
    def run(self):
        self.roadname_col, self.detailed_col = self._load_column_mappings()
        self._find_folder_path()

        roadname_filelist = self.find_filelist(self._roadname_path, self.ROADNAME_DEL_WORD)
        detailed_filelist = self.find_filelist(self._detailed_path, self.DETAILED_DEL_WORD)

        roadname_df = self.read_data(self._roadname_path, roadname_filelist, self.roadname_col, self.ROADNAME_FILE_NAME)
        detailed_df = self.read_data(self._detailed_path, detailed_filelist, self.detailed_col, self.DETAILED_FILE_NAME)


if __name__ == "__main__":
    test = ReadCorrectData()
    test.run()
