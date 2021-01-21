import requests 
import json 
import datetime
import pandas as pd

import config

vilage_weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?' 

service_key = config.weather_api_key

today = datetime.datetime.today()
base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜
#base_date = "20210120" # "20200214" == 기준 날짜
base_time = "0800" # 날씨 값

nx = "60"
ny = "128"

# res/xylist.csv를 이용해 주소를 확인후 nx와 ny를 매치 시켜야한다 
# 다음 코드를 통해 cvs 파일을 리스트 형식으로 불러온다
xylist = pd.read_csv('../res/xylist.csv', engine='c', dtype=str, sep=',', encoding='CP949')

# csv값 확인
print(xylist)

payload = "serviceKey=" + service_key + "&" +\
    "dataType=json" + "&" +\
    "base_date=" + base_date + "&" +\
    "base_time=" + base_time + "&" +\
    "nx=" + nx + "&" +\
    "ny=" + ny

# 값 요청
res = requests.get(vilage_weather_url + payload)

print(res)

items = res.json().get('response').get('body').get('items')

data = dict()
data['date'] = base_date

weather_data = dict()

for item in items['item']:
	# 기온
	if item['category'] == 'T3H':
		weather_data['tmp'] = item['fcstValue']
	
	# 기상상태
	if item['category'] == 'PTY':
		weather_code = item['fcstValue']
		
		if weather_code == '1':
			weather_state = '비'
		elif weather_code == '2':
			weather_state = '비/눈'
		elif weather_code == '3':
			weather_state = '눈'
		elif weather_code == '4':
			weather_state = '소나기'
		else:
			weather_state = '없음'
		
		weather_data['code'] = weather_code
		weather_data['state'] = weather_state

data['weather'] = weather_data
print(data['weather'])
# {'code': '0', 'state': '없음', 'tmp': '9'} # 9도 / 기상 이상 없음