from seoul_crime.data_reader import DataReader

class CrimeModel:
    def __init__(self):
        self.dr = DataReader()

    def hook_process(self):
        print('----------------1. 범죄율 파일 DF 생성--------------------')
        self.get_crime()

    def get_crime(self):
        self.dr.context = './data/'
        self.dr.fname = 'crime_in_seoul.csv'
        crime = self.dr.csv_to_dframe()
      #  print(crime)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울'+str(name[:-1]+'경찰서'))
        station_addrs = []
        station_lats = [] #위도
        station_lngs = [] #경도
        gmaps = self.dr.create_gmaps()
        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            station_addrs.append(t[0].get('formatted_address'))
            t_loc = t[0].get('geometry')
            station_lats.append(t_loc['location']['lat']) #formatted_address, lat, lng, location 구글맵 내부에 기재되어있는 정보들이므로 그대로 사용해야함
            station_lngs.append(t_loc['location']['lng'])
            print(name + '--------> '+t[0].get('formatted_address'))
        gu_names = []
        for name in station_addrs:
            t = name.split()
            gu_name = [gu for gu in t if gu[-1] == '구'][0] # [:-1]은 모든글자 [-1]은 끝의 한글자
            gu_names.append(gu_name)
        crime['구별'] = gu_names

        # 구 와 경찰서 위치가 다른 경우 수작업

        crime.loc[crime['관서명'] == '혜화서', ['구별']] == '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] == '은평구'
        crime.loc[crime['관서명'] == '강서서', ['구별']] == '양천구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] == '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] == '강남구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] == '강남구'

        print(crime)

        crime.to_csv('./saved_data/crime_police.csv')

