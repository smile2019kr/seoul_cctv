import pandas as pd
import numpy as np
import json
import googlemaps


class DataReader:
    def __init__(self):
        self._context = None
        self._fname = None

    @property
    def context(self)->str:
        return self._context
    @context.setter
    def context(self, context):
        self._context = context

    @property
    def fname(self)->str:
        return self._fname
    @fname.setter
    def fname(self, fname):
        self._fname = fname

    def new_file(self)->str:
        return self._context + self._fname

    def csv_to_dframe(self)->object:
        file = self.new_file()
        return pd.read_csv(file, encoding='UTF-8', thousands=',')
        #한글 읽어들이기 설정 UTF-8, 숫자 천단위로 쉼표 표기 추가

    def xls_to_dframe(self, header,usecols)->object:
        #엑셀파일은 헤더가 있으므로 그냥 불러올때와 다름
        file = self.new_file()
        return pd.read_excel(file, encoding='UTF-8', header=header, usecols=usecols)

    def json_load(self):
        file = self.new_file()
        return json.load(open(file, encoding='UTF-8'))

    def create_gmaps(self):
        return googlemaps.Client(key='...')
    # key값은 개인정보이므로 깃허브 백업시에는 공란으로 둘것
    # (정보기재상태로 백업 후 정보삭제하여 다시 백업한다고 해도 기존에 백업된 정보가 남아있으므로 백업 시 아예 삭제한 상태로 백업하는것이 중요함)




