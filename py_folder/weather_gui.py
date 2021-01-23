from tkinter import *
from PIL import Image, ImageTk

import location_weather as lw

def weather_info(root, location):
	#날씨정보 프레임
	#location_text : loaction_gui의 input을 받는다
	#weather_text & current_temp_text : location_text를 이용한 날씨 api이용
	weather_info_frame = Frame(root)
	weather_info_frame.pack(side = "top", fill = "both", pady=40)
	
	#location_gui에서 위치 정보 받아오기
	location_text = "경기도 고양시 화전동"

	#날씨 api를 통해 날씨 정보값 읽어오기
	weather_text = "맑음"
	current_tmp_text = "20" + "℃"

	global location_label
	location_label = Label(weather_info_frame, text=location_text)
	location_label.config(font = ("Courier",10,"bold"))
	location_label.pack(anchor="s")

	global weather_label
	weather_label = Label(weather_info_frame, text=weather_text)
	weather_label.config(font = ("Courier", 8))
	weather_label.pack(fill="both")

	'''
	pil_weatherPhoto_image = Image.open("../images/weather_sunny_3.png")
	pil_weatherPhoto_image = pil_weatherPhoto_image.resize((50,50), Image.ANTIALIAS)
	weatherPhoto = ImageTk.PhotoImage(pil_weatherPhoto_image)
	global weatherPhoto_label
	weatherPhoto_label = Label(weather_info_frame, image=weatherPhoto)
	weatherPhoto_label.pack(fill="both")
	'''
	
	global current_tmp_label
	current_tmp_label = Label(weather_info_frame, text=current_tmp_text)
	current_tmp_label.config(font = ("Courier", 20, "bold"))
	current_tmp_label.pack(fill="both")

	weather_set(location)

	return 2

def weather_set(location):
	weather_data = lw.get_weather_info(location)

	print(weather_data)

	location_label.config(text=location)
	weather_label.config(text=weather_data['sky_state'])

	if 'tmp1' in weather_data: 
		current_tmp_label.config(text=weather_data['tmp1'])
	else:
		current_tmp_label.config(text=weather_data['tmp3'])

def weather_anime():
	#이미지 바꿀때 사용
	pil_weatherPhoto_image = Image.open("./images/weather_sunny_2.png")
	pil_weatherPhoto_image = pil_weatherPhoto_image.resize((50,50), Image.ANTIALIAS)
	weatherPhoto = ImageTk.PhotoImage(pil_weatherPhoto_image)
	weatherPhoto_label.config(image=weatherPhoto)
