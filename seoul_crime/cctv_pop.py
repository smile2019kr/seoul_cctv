import pandas as pd
import numpy as np
from seoul_crime.data_reader import DataReader


"""
Index(['기관명', '소계', '2013년도 이전', '2014년', '2015년', '2016년'], dtype='object')
Index(['자치구', '계', '계.1', '계.2', '65세이상고령자'], dtype='object')
"""


class CCTVModel:
    def __init__(self):
        self.dr = DataReader()

    def hook_process(self):
        print('----------------1. cctv 파일 DF 생성--------------------')
        self.get_cctv()


        #cctv정보파일 읽어오기
    def get_cctv(self):
        self.dr.context = './data/'
        self.dr.fname = 'cctv_in_seoul.csv'
        cctv = self.dr.csv_to_dframe()
        # 인덱스 확인을 위한 출력문 print(cctv.columns)
        print(cctv.columns)
        # print(cctv) -> 제대로 df로 불러들였는지 확인용
        self.dr.fname = 'pop_in_seoul.xls'
        pop = self.dr.xls_to_dframe(2, 'B,D,G,J,N')
        # B, D, G, J, N 에 있는 것만 불러오기
        # print(pop) -> 제대로 df로 불러들였는지 확인용
        # 인덱스 확인을 위한 출력문 print(pop.columns)
        print(pop.columns)

