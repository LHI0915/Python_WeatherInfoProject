from tkinter import *
from PIL import Image, ImageTk

import location_weather as lw

def weather_info(root, location):
	#날씨정보 프레임
	#location_text : loaction_gui의 input을 받는다
	#weather_text & current_temp_text : location_text를 이용한 날씨 api이용

	weather_info_frame = Frame(root)
	weather_info_frame.pack(side = "top", fill="both", pady=0)
	
	#location_gui에서 위치 정보 받아오기
	location_text = "경기도 고양시 화전동"

	#날씨 api를 통해 날씨 정보값 읽어오기
	weather_text = "맑음"
	current_tmp_text = "20" + "℃"

	global location_label
	location_label = Label(weather_info_frame, text=location_text)
	location_label.config(font = ("Courier",12,"bold"))
	location_label.pack(anchor="s")

	global weather_label
	weather_label = Label(weather_info_frame, text=weather_text)
	weather_label.config(font = ("Courier", 10))
	weather_label.pack(fill="both")
	
	global current_tmp_label
	current_tmp_label = Label(weather_info_frame, text=current_tmp_text)
	current_tmp_label.config(font = ("Courier", 20, "bold"))
	current_tmp_label.pack(fill="both")

	weather_text = weather_set(location)

	return weather_text

def weather_set(location):
	weather_data = lw.get_weather_info(location)

	location_label.config(text=location)
	
	weather_kor_text = ''
	weather_eng_text = ''

	if int(weather_data['lgt_code']) >= 3:
		weather_kor_text = '천둥/번개'
		weather_eng_text = 'stormy'
	elif int(weather_data['pty_code']) != 0:
		weather_kor_text = weather_data['pty_state']
		if weather_data['pty_state'] == '비' :
			weather_eng_text = 'rainy'
		elif weather_data['pty_state'] == '눈' :
			weather_eng_text = 'snowy'
	elif float(weather_data['wsd']) >= 9:
		weather_kor_text = '바람'
		weather_eng_text = 'windy'
	else:
		weather_kor_text = weather_data['sky_state']
		if weather_data['sky_state'] == '맑음' :
			weather_eng_text = 'sunny'
		elif weather_data['sky_state'] == '구름많음' :
			weather_eng_text = 'partly_sunny'
		else:
			weather_eng_text = 'cloudy'

	if weather_kor_text: 
		weather_label.config(text=weather_kor_text)
		current_tmp_label.config(text=weather_data['tmp3'])
	else:
		weather_label.config(text='-')
		current_tmp_label.config(text='- ℃')

	return weather_eng_text
