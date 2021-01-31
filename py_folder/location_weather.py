import requests 
import json 
import pandas as pd

import datetime
from datetime import timedelta

import config

def location_coordinate(location):
	# 여기서 주소를 좌표로 변경
		
	# res/xylist.csv를 이용해 주소를 확인후 nx와 ny를 매치 시켜야한다 
	# 다음 코드를 통해 cvs 파일을 리스트 형식으로 불러온다
	xylist = pd.read_csv('../res/xylist.csv', engine='c', dtype=str, sep=',', encoding='CP949')

	# csv값 확인
	print(xylist)
	
	nx = "60"
	ny = "128"	
	
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
		if h < 5 :	return '0200'
		if h < 8 :	return '0500'
		elif h < 11 :	return '0800'
		elif h < 14 :	return '1100'
		elif h < 17 :	return '1400'
		elif h < 20 :	return '1700'
		elif h < 23 :	return '2000'
		else : return '2300'

# get_weather_api(장소 넘기기)
def get_weather_vilage_api(nx, ny):
	'''
	동네예보(VilageFcstInfoService)
	POP - 강수확률(%)
	TMN - 아침 최저기온(℃)
	TMX - 낮 최고기온(℃)
	SKY - 하늘상태(코드값)
		하늘상태(SKY) 코드 : 맑음(0~5), 구름많음(6~8), 흐림(9~10)
	WSD - 풍속(m/s)
		풍속 구간 의미 : 바람이 약하다(0~3), 바람이 약간 강하다(4~8)
										바람이 강하다(9~13), 바람이 매우 강하다(14~)
	'''
	weather_vilage_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?' 

	service_key = config.weather_api_key

	today = datetime.datetime.today()
	
	base_date = '-'
	base_time = '-'

	# 동네예보
	# - Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
	# - API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10
	today = datetime.datetime.today()
	date_vilage_flag = True
	
	if today.hour <= 2 and today.minute < 10 :
		today = today - timedelta(days=1)
		base_vilage_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜	
		base_vilage_time = "2300"

		date_vilage_flag = False

	if date_vilage_flag :
		base_vilage_date = today.strftime("%Y%m%d")
		base_vilage_time = get_vilage_base_time(today.hour, today.minute)

	vilage_payload = "serviceKey=" + service_key + "&" +\
			"dataType=json" + "&" +\
			"base_date=" + base_vilage_date + "&" +\
			"base_time=" + base_vilage_time + "&" +\
			"nx=" + nx + "&" +\
			"ny=" + ny

	# 값 요청

	vilage_res = requests.get(weather_vilage_url + vilage_payload)

	try:
		items = vilage_res.json().get('response').get('body').get('items')
	except AttributeError:
		# api가 업데이트 될때 00시 부터 02시 10분 까지 에러 발생
		# 기본 값을 넘겨준다
		vilage_weather_data = {
			'tmp' : '36.5℃'	,
			'pop' : '0%'	,
			'r06'	:	'0mm'	,
			'reh'	:	'0%'	,
			'tmpn': '36.5℃'	, 
			'tmpx': '36.5℃'	,
			'sky_code'	:	'0'	,
			'sky_state'	:	'맑음'	,
			'vec'	:	'0'	,
			'wsd'	:	'0m/s'	}
		return vilage_weather_data

	vilage_weather_data = dict()

	for item in items['item']:
		# 3시간 기온(℃)
		if item['category'] == 'T3H':
			vilage_weather_data['tmp'] = item['fcstValue'] + '℃'

		# 강수확률(%)
		if item['category'] == 'POP':
			vilage_weather_data['pop'] = item['fcstValue'] + '%'
		
		# 강수량(mm)
		if item['category'] == 'R06':
			vilage_weather_data['r06'] = item['fcstValue'] + 'mm'

		# 습도(%)
		if item['category'] == 'REH':
			vilage_weather_data['reh'] = item['fcstValue'] + '%'

		# 아침 최저기온(℃)
		if item['category'] == 'TMN':
			vilage_weather_data['tmpn'] = item['fcstValue'] + '℃'
		
		# 낮 최고기온(℃)
		if item['category'] == 'TMX':
			vilage_weather_data['tmpx'] = item['fcstValue'] + '℃'

		# 하늘상태(SKY) 코드 : 맑음(0~5), 구름많음(6~8), 흐림(9~10) 
		if item['category'] == 'SKY':
			weather_sky_code = item['fcstValue']
			if weather_sky_code >= '0' and weather_sky_code <= '5':
				weather_sky_state = '맑음'
			elif weather_sky_code >= '6' and weather_sky_code <= '8':
				weather_sky_state = '구름많음'
			elif weather_sky_code >= '9' and weather_sky_code <= '10':
				weather_sky_state = '흐림'

			vilage_weather_data['sky_code'] = weather_sky_code
			vilage_weather_data['sky_state'] = weather_sky_state

		# 풍향
		if item['category'] == 'VEC':
			vilage_weather_data['vec'] = item['fcstValue']

		#	WSD - 풍속(m/s)
		# 풍속 구간 의미 : 바람이 약하다(0~3), 바람이 약간 강하다(4~8)
		#									바람이 강하다(9~13), 바람이 매우 강하다(14~)
		if item['category'] == 'WSD':
			vilage_weather_data['wsd'] = item['fcstValue']
			# vilage_weather_data['wsd'] = item['fcstValue']  + ' m/s'

	return vilage_weather_data

# 초단기예보
def get_weather_srt_api(nx, ny):
	'''
	초단기예보(UltraSrtFcstInfoService)
	PTY	- 강수형태(코드값)
		강수형태(PTY) 코드 : 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
	LGT	- 낙뢰(코드값)
		낙뢰(LGT) 코드 : 확률없음(0), 낮음(1), 보통(2), 높음(3) 
	'''
	weather_srt_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?'

	service_key = config.weather_api_key

	today = datetime.datetime.today()
	
	base_srt_date = '-'
	base_srt_time = '-'

	# 초단기예보
	# - Base_time : 매 시간 30분에 생성
	# - API 제공 시간(~이후) : 매 시간 45분 이후
	today = datetime.datetime.today()
	date_srt_flag = True

	if today.hour == 0 and today.minute < 45 :
		today = today - timedelta(days=1)
		base_srt_date = today.strftime("%Y%m%d") # "20200214" == 기준 날짜	
		base_srt_time = "2330"

		date_srt_flag = False

	if date_srt_flag :
		base_srt_date = today.strftime("%Y%m%d")
		if today.minute < 45 :
			today = today - timedelta(hours=1)
		base_srt_time = today.strftime("%I") + "30"

	srt_payload = "serviceKey=" + service_key + "&" +\
			"dataType=json" + "&" +\
			"base_date=" + base_srt_date + "&" +\
			"base_time=" + base_srt_time + "&" +\
			"nx=" + nx + "&" +\
			"ny=" + ny

	# 값 요청

	srt_res = requests.get(weather_srt_url + srt_payload)

	try:
		items = srt_res.json().get('response').get('body').get('items')
	except AttributeError:
		# api가 업데이트 될때 00시 부터 02시 10분 까지 에러 발생
		# 기본 값을 넘겨준다
		srt_weather_data = {
			'pty_code': '0', 'pty_state': '없음',
			'lgt_code': '0', 'sky_state': '없음' }
		return srt_weather_data

	srt_weather_data = dict()

	for item in items['item']:
		# 강수형태(PTY) 코드 : 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
		if item['category'] == 'PTY':
			weather_pty_code = item['fcstValue']
			if weather_pty_code == '1' or weather_pty_code == '4' or weather_pty_code == '5' :
				weather_pty_state = '비'
			elif weather_pty_code == '2' or weather_pty_code == '3' or weather_pty_code == '6' or weather_pty_code == '7':
				weather_pty_state = '눈'
			else:
				weather_pty_state = '없음'

			srt_weather_data['pty_code'] = weather_pty_code
			srt_weather_data['pty_state'] = weather_pty_state

		# 낙뢰(LGT) 코드 : 확률없음(0), 낮음(1), 보통(2), 높음(3)
		if item['category'] == 'LGT':
			weather_lgt_code = item['fcstValue']
			if weather_lgt_code == '0' :
				weather_lgt_state = '없음'
			elif weather_lgt_code == '1' :
				weather_lgt_state = '낮음'
			elif weather_lgt_code == '2' :
				weather_lgt_state = '보통'
			else :
				weather_lgt_state = '높음'

			srt_weather_data['lgt_code'] = weather_lgt_code
			srt_weather_data['lgt_state'] = weather_lgt_state

	return srt_weather_data

def get_weather_info(location):
	nx, ny = location_coordinate(location)

	api_vilage_result = get_weather_vilage_api(nx, ny)
	api_srt_result = get_weather_srt_api(nx, ny)

	weather_data = dict()
	weather_data.update(api_vilage_result)
	weather_data.update(api_srt_result)

	print(weather_data)

	return(weather_data)