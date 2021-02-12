from tkinter import *
from PIL import Image, ImageTk

import location_weather_crawling as lwc
import location_gui as lg

def weather_info(root):
	#날씨정보 프레임
	#location_text : loaction_gui의 input을 받는다
	#weather_text & current_temp_text : location_text를 이용한 날씨 api이용
	weather_info_frame = Frame(root)
	weather_info_frame.pack(side = "top", fill = "both", pady=40)
	
	#location_gui에서 위치 정보 받아오기
	#location_text = lg.final_location
	location_text = "서울시 용산구"

	# 받아온 위치정보를 이용해서 날씨 정보값 받아오기
	temp_and_cast = lwc.location_weather(location_text)

	#날씨 api를 통해 날씨 정보값 읽어오기
	current_tmp_text = temp_and_cast[0]
	weather_text = temp_and_cast[1]

	print(current_tmp_text)
	print(weather_text)

	location_label = Label(weather_info_frame, text=location_text)
	location_label.config(font = ("Courier",10,"bold"))
	location_label.pack(anchor="s")

	weather_label = Label(weather_info_frame, text=weather_text)
	weather_label.config(font = ("Courier", 8))
	weather_label.pack(fill="both")

	
	pil_weatherPhoto_image = Image.open("./images/weather_sunny_3.png")
	pil_weatherPhoto_image = pil_weatherPhoto_image.resize((50,50), Image.ANTIALIAS)
	weatherPhoto = ImageTk.PhotoImage(pil_weatherPhoto_image)
	global weatherPhoto_label
	weatherPhoto_label = Label(weather_info_frame, image=weatherPhoto)
	weatherPhoto_label.pack(fill="both")

	current_tmp_label = Label(weather_info_frame, text=current_tmp_text)
	current_tmp_label.config(font = ("Courier", 20, "bold"))
	current_tmp_label.pack(fill="both")

def weather_anime():
	#이미지 바꿀때 사용
	pil_weatherPhoto_image = Image.open("./images/weather_sunny_2.png")
	pil_weatherPhoto_image = pil_weatherPhoto_image.resize((50,50), Image.ANTIALIAS)
	weatherPhoto = ImageTk.PhotoImage(pil_weatherPhoto_image)
	weatherPhoto_label.config(image=weatherPhoto)

