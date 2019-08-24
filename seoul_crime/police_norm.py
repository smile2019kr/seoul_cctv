from seoul_crime.data_reader import DataReader
import pandas as pd
import numpy as np
from sklearn import preprocessing

class PoliceNormModel:
    def __init__(self):
        self.dr = DataReader()

    def hook_process(self):
        print('----------------1. cctv 파일 DF 생성--------------------')
        self.create_crime_rate()

    def create_crime_rate(self):
        self.dr.context = './saved_data/'
        self.dr.fname = 'crime_police.csv'
        police_crime = self.dr.csv_to_dframe()
        police = pd.pivot_table(police_crime, index='구별', aggfunc=np.sum)
        print(police.columns)
        police['살인검거율'] = (police['살인 검거'] / police['살인 발생']) * 100
        police['강도검거율'] = (police['강도 검거'] / police['강도 발생']) * 100
        police['강간검거율'] = (police['강간 검거'] / police['강간 발생']) * 100
        police['절도검거율'] = (police['절도 검거'] / police['절도 발생']) * 100
        police['폭력검거율'] = (police['폭력 검거'] / police['폭력 발생']) * 100
        police.drop(columns={'살인 검거','강도 검거','강간 검거','절도 검거','폭력 검거'}, axis=1)
        crime_rate_columns = ['살인검거율','강도검거율','강간검거율','절도검거율','폭력검거율']
        for i in crime_rate_columns:
            police.loc[police[i] > 100, 1] = 100 #비율이 100%가 넘는 경우 100으로 치환
        police.rename(columns = {
            '살인 발생' : '살인',
            '강도 발생' : '강도',
            '강간 발생' : '강간',
            '절도 발생' : '절도',
            '폭력 발생' : '폭력'
        }, inplace=True)

        crime_columns = ['살인', '강도', '강간', '절도', '폭력']

        x = police[crime_rate_columns].values

        min_max_scalar = preprocessing.MinMaxScaler()
        #차원이 올라가면 collection이 객체로 전환됨
        #return되는 값의 차원이 올라가면 scalar로 전환
        #결국, 학습결과로 최종적으로 산출되는 것은 scalar(단위값). collection이 아님
        # 스케일링은 선형변환을 적응하여 전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정

        x_scaled = min_max_scalar.fit_transform(x.astype(float))

        # 정규화(normalization)
        # 많은 양의 데이터를 처리함에 있어 여러 이유로 정규화,
        # 즉 데이터의 범위를 일치시키거나 분포를 유사하게 만들어주는 등의 작업
        # 평균값 정규화, 중간값 정규화.....

        police_norm = pd.DataFrame(x_scaled,
                                   columns=crime_columns,
                                   index=police.index)
        police_norm[crime_rate_columns] = police[crime_rate_columns]
        self.dr.context = './saved_data'
        self.dr.fname = '/cctv_pop.csv'
        cctv_pop = pd.read_csv(self.dr.new_file(), encoding='UTF-8', sep=',', index_col='구별')
        police_norm['범죄'] = np.sum(police_norm[crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[crime_columns], axis=1)
        print(police_norm.columns)
        police_norm.to_csv('./saved_data/police_norm.csv')


