from seoul_crime.data_reader import DataReader
import numpy as np
import folium # 지도그리는 라이브러리

class CrimeMap:
    def __init__(self):
        self.dr = DataReader()
    def hook(self):
        self.create_seoul_crime_map()

    def create_seoul_crime_map(self):
        self.dr.context='./saved_data/'
        self.dr.fname = 'police_norm.csv'
        police_norm = self.dr.csv_to_dframe()
      #  print(pn) #dataframe으로 제대로 불러들였는지 확인하기 위함
        self.dr.context='./data/'
        self.dr.fname = 'geo_simple.json'
        seoul_geo = self.dr.json_load()
        #폴리움 코딩은 템플릿화되어있으므로 가져와서 붙이고 데이터만 한국지도에 맞게 수정하면 됨

        self.dr.context='./data/'
        self.dr.fname = 'crime_in_seoul.csv'
        crime = self.dr.csv_to_dframe()

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
    #        print(name + '--------> '+t[0].get('formatted_address')) # 구글키가 작동하는지 확인

       # 기존 코드
        self.dr.context='./data/'
        self.dr.fname = 'police_position.csv'
        police_pos = self.dr.csv_to_dframe()
        police_pos['lat'] = station_lats
        police_pos['lng'] = station_lngs
   #     print(police_pos) # 제대로 불러읽어들였는지 확인
        col = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
        tmp = police_pos[col] / police_pos[col].max
        police_pos['검거'] = np.sum(tmp, axis=1)
        self.dr.fname = 'geo_simple.json'

        m = folium.Map(location=[37.5502, 126.982], zoom_start=12, title='stamen Toner') # 한국 위도, 경도 설정 및 지도 스타일 설정
        m.choropleth(
            geo_data=seoul_geo,
            name='choropleth',
            # json에서의 id와 police_norm에 있는 스키마(변수명, 컬럼)의 내용 값을 일치시켜야 하므로 pn안에서 [구별] [범죄]를 체크해야함
            # 폴리움 데이터에서 state, unemployment를 컬럼으로 가지도록 한 것과 같은 패턴
            data=tuple(zip(police_norm['구별'], police_norm['범죄'])),
            key_on='feature.id',
            fill_color='PuRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Crime Rate (%)'
        )
        # 괄호안의 파라메터들에 관해 파고들어갈 필요까지는 없음

        # 기존 지도에 검거율 추가
        for i in police_pos.index:
            folium.CircleMarker([police_pos['lat'][i], police_pos['lng'][i]],
                                radius=police_pos['검거'][i] * 10,
                                fill_color = '#0a0a32').add_to(m)

        m.save('./saved_data/Seoul_Crime.html')
        # csv파일 다운로드 또는 웹크롤링으로 바로 읽어들여서 html화면에 변화되는 데이터들의 내용이 반영될 수 있도록 저장하는 구문
        # 실행 후 saved_data폴더에 저장된 Seoul_Crime.html 파일을 클릭해서 크롬으로 출력된 화면 확인
        # 데이터에서 양천구가 누락된 것으로 보임
        # 현업에서도 필요한 부분만 긁어와서 편집/코딩
