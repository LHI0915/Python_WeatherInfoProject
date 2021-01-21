import requests 
import json 
import pandas as pd

import datetime
from datetime import timedelta

import config

# weather_get_api(장소 넘기기)
def weather_get_api():

	weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?' 
	# 낙뢰 정보 확인을 위해 초단기예보를 사용해야 함 (LGT)
	# weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?'

	service_key = config.weather_api_key

	today = datetime.datetime.today()
	
	# 동네예보
	# - Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
	# - API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10
	today = datetime.datetime.today()
	base_date = today.strftime("%Y%m%d")
	base_time = "0800"
	'''
	if today.hour < 3:
		today = today - timedelta(days=1)

		base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜	
		base_time = "2300"

	if today.strftime("%M") < '30':
		base_time = today.strftime("%I") + "00" # 기준시간
	else:
		base_time = today.strftime("%I") + "30"

	print(base_time)
	'''
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
	res = requests.get(weather_url + payload)

	items = res.json().get('response').get('body').get('items')

	data = dict()
	data['date'] = base_date

	weather_data = dict()

	for item in items['item']:
		# 기온
		if item['category'] == 'T3H':
			weather_data['tmp'] = item['fcstValue']
		
		# 강수형태(PTY) 코드 : 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
		if item['category'] == 'PTY':
			weather_pty_code = item['fcstValue']
			
			if weather_pty_code == '1':
				weather_pty_state = '비'
			elif weather_pty_code == '2':
				weather_pty_state = '비/눈'
			elif weather_pty_code == '3':
				weather_pty_state = '눈'
			elif weather_pty_code == '4':
				weather_pty_state = '소나기'
			else:
				# weather_pty_code == '0'
				weather_pty_state = '없음'

			weather_data['pty_code'] = weather_pty_code
			weather_data['pty_state'] = weather_pty_state

		# 하늘상태(SKY) 코드 : 맑음(1), 구름많음(3), 흐림(4) 
		if item['category'] == 'SKY':
			weather_sky_code = item['fcstValue']
			
			if weather_sky_code >= '0' and weather_sky_code <= '5':
				weather_sky_state = '맑음'
			elif weather_sky_code >= '6' and weather_sky_code <= '8':
				weather_sky_state = '구름많음'
			elif weather_sky_code >= '9' and weather_sky_code <= '10':
				weather_sky_state = '흐림'

			weather_data['sky_code'] = weather_sky_code
			weather_data['sky_state'] = weather_sky_state

	data['weather'] = weather_data
	print(data['weather'])
	# {'pty_code': '0', 'pty_state': '없음', 'sky_code': '4', 'sky_state': '맑음'} # 9도 / 강수 이상 없음 / 하늘맑음
	
	return data

weather_data = weather_get_api()