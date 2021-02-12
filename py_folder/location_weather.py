import requests 
import json 
import pandas as pd

import datetime
from datetime import timedelta

import config
from location_gui import final_location

def location_coordinate(locaion):
	# 여기서 주소를 좌표로 변경
		
	# res/xylist.csv를 이용해 주소를 확인후 nx와 ny를 매치 시켜야한다 
	# 다음 코드를 통해 cvs 파일을 리스트 형식으로 불러온다
	xylist = pd.read_csv('./res/xylist.csv', engine='c', dtype=str, sep=',', encoding='CP949')
	final_location = ["경기도", "고양시 일산서구", "주엽1동"]
	for idx, juso in enumerate(final_location):
		final_location[idx] = juso.replace(" ","")

	# csv값 확인
	#print(xylist)
	
	nx = "20"
	ny = "20"	
	
	for row_index, row in xylist.iterrows():
		if type(row) == float:
			continue
		if row[0] == final_location[0] and row[1]==final_location[1] and row[2]==final_location[2]:
		 	nx = row[3]
		 	ny = row[4]
		#  	print("{0} {1} {2}" .format(row[0],row[1],row[2])
		# print("{0} {1}" .format(row[3], row[4]))
	print(nx, ny)
	
	return nx, ny

def get_vilage_base_time(h, m):
	# API 업로드 기준인 10분 전 후를 체크
	if m < 10 :
		if h <= 5 :	return '0200'
		elif h <= 8 :	return '0500'
		elif h <= 11 :	return '0800'
		elif h <= 14 :	return '1100'
		elif h <= 17 :	return '1400'
		elif h <= 20 :	return '1700'
		elif h <= 23 :	return '2000'
		else : return '2300'
	else:
		if h <= 2 :	return '0200'
		if h <= 5 :	return '0500'
		elif h <= 8 :	return '0800'
		elif h <= 11 :	return '1100'
		elif h <= 14 :	return '1400'
		elif h <= 17 :	return '1700'
		elif h <= 20 :	return '2000'
		else : return '2300'

# get_weather_api(장소 넘기기)
def get_weather_vilage_api(nx, ny):
	'''
	동네예보(VilageFcstInfoService)
	POP - 강수확률
	TMN - 아침 최저기온
	TMX - 낮 최고기온
	'''
	weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?' 

	service_key = config.weather_api_key

	today = datetime.datetime.today()
	
	base_date = '-'
	base_time = '-'

	# 동네예보
	# - Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
	# - API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10
	today = datetime.datetime.today()
	date_flag = True
	
	if today.hour <= 2 and today.minute < 10 :
		today = today - timedelta(days=1)
		base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜	
		base_time = "2300"

		date_flag = False

	if date_flag :
		base_date = today.strftime("%Y%m%d")
		base_time = get_vilage_base_time(today.hour, today.minute)

	print(base_date)
	print(base_time)

	payload = "serviceKey=" + service_key + "&" +\
			"dataType=json" + "&" +\
			"base_date=" + base_date + "&" +\
			"base_time=" + base_time + "&" +\
			"nx=" + nx + "&" +\
			"ny=" + ny

	# 값 요청

	res = requests.get(weather_url + payload)

	try:
		items = res.json().get('response').get('body').get('items')
	except AttributeError:
		# api가 업데이트 될때 00시 부터 02시 10분 까지 에러 발생
		# 기본 값을 넘겨준다
		weather_data = {
			'tmp' : '20',
			'pty_code': '0', 'pty_state': '없음', 
			'sky_code': '1', 'sky_state': '맑음' }
		return weather_data

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
				weather_pty_state = '없음'

			weather_data['pty_code'] = weather_pty_code
			weather_data['pty_state'] = weather_pty_state

		# 하늘상태(SKY) 코드 : 맑음(0~5), 구름많음(6~8), 흐림(9~10) 
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

	# print(weather_data)
	# {'pty_code': '0', 'pty_state': '없음', 'sky_code': '4', 'sky_state': '맑음'} # 9도 / 강수 이상 없음 / 하늘맑음
	
	return weather_data

# get_weather_api(장소 넘기기)
def get_weather_srt_api(nx, ny):
	'''
	초단기예보(UltraSrtFcstInfoService)
	T1H - 기온(℃)
	RN1	- 1시간 강수량(mm)
	REH - 습도(%)
	SKY - 하늘상태(코드값)
		하늘상태(SKY) 코드 : 맑음(0~5), 구름많음(6~8), 흐림(9~10)
	PTY	- 강수형태(코드값)
		강수형태(PTY) 코드 : 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
	LGT	- 낙뢰(코드값)
		낙뢰(LGT) 코드 : 확률없음(0), 낮음(1), 보통(2), 높음(3) 
	'''
	weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?'

	service_key = config.weather_api_key

	today = datetime.datetime.today()
	
	base_date = '-'
	base_time = '-'

	# 초단기예보
	# - Base_time : 매 시간 30분에 생성
	# - API 제공 시간(~이후) : 매 시간 45분 이후
	today = datetime.datetime.today()
	date_flag = True

	if today.hour == 0 and today.minute < 45 :
		today = today - timedelta(days=1)
		base_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜	
		base_time = "2330"

		date_flag = False

	if date_flag :
		base_date = today.strftime("%Y%m%d")
		if today.minute < 45 :
			today = today - timedelta(hour=1)
			base_time = today.strftime("%I%M")
		else:
			base_time = today.strftime("%I%M")

	print(base_date)
	print(base_time)

	payload = "serviceKey=" + service_key + "&" +\
			"dataType=json" + "&" +\
			"base_date=" + base_date + "&" +\
			"base_time=" + base_time + "&" +\
			"nx=" + nx + "&" +\
			"ny=" + ny

	# 값 요청

	res = requests.get(weather_url + payload)

	try:
		items = res.json().get('response').get('body').get('items')
	except AttributeError:
		# api가 업데이트 될때 00시 부터 02시 10분 까지 에러 발생
		# 기본 값을 넘겨준다
		weather_data = {
			'tmp' : '20',
			'pty_code': '0', 'pty_state': '없음', 
			'sky_code': '1', 'sky_state': '맑음' }
		return weather_data

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
				weather_pty_state = '없음'

			weather_data['pty_code'] = weather_pty_code
			weather_data['pty_state'] = weather_pty_state

		# 하늘상태(SKY) 코드 : 맑음(0~5), 구름많음(6~8), 흐림(9~10) 
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

	# print(weather_data)
	# {'pty_code': '0', 'pty_state': '없음', 'sky_code': '4', 'sky_state': '맑음'} # 9도 / 강수 이상 없음 / 하늘맑음
	
	return weather_data


nx, ny = location_coordinate('경기도 고양시 화전동')
api_result = get_weather_vilage_api(nx, ny)
print(api_result)