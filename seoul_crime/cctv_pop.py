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
        cctv.rename(columns={cctv.columns[0]: '구별'}, inplace=True)
        #inplace -> 원본을 바꾸라는 것
        pop.rename(columns={
            pop.columns[0]: '구별',
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자'
        }, inplace=True)
      #  pop.drop([0], True)  #1행 삭제
#        print(pop['구별'].isnull()) #null값 있는지 확인 -> 26번째에서 True 라고 나옴. 26번째가 null값이라는 뜻 -> 삭제필요
        pop.drop([26], inplace=True) # 27행 삭제
        pop['외국인비율'] = pop['외국인'] / pop['인구수'] * 100
        pop['고령자비율'] = pop['고령자'] / pop['인구수'] * 100

        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], 1, inplace=True) #연도별정보를 삭제하고 현재자료만 사용
        cctv_pop = pd.merge(cctv, pop, on='구별') #cctv와 pop이라는 df를 [구별]이라는 컬럼명에 맞게 병합
        cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
        cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])

        print('고령자비율과 cctv의 상관계수 {}  \n'
              '외국인비율과 cctv의 상관계수 {}'.format(cor1, cor2))

        # 추출한 데이터를 별도의 디렉토리에 저장
        cctv_pop.to_csv('./saved_data/cctv_pop.csv')


"""
[결과]
고령자비율과 cctv의 상관계수 [[ 1.         -0.28078554]
                             [-0.28078554  1.        ]]  
외국인비율과 cctv의 상관계수 [[ 1.         -0.13607433]
                             [-0.13607433  1.        ]]
"""

