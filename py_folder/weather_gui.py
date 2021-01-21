from tkinter import *
from PIL import Image, ImageTk

import location_weather as lw

def weather_info(root):
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

	location_label = Label(weather_info_frame, text=location_text)
	location_label.config(font = ("Courier",10,"bold"))
	location_label.pack(anchor="s")

	weather_label = Label(weather_info_frame, text=weather_text)
	weather_label.config(font = ("Courier", 8))
	weather_label.pack(fill="both")

	
	pil_weatherPhoto_image = Image.open("../images/weather_sunny_3.png")
	pil_weatherPhoto_image = pil_weatherPhoto_image.resize((50,50), Image.ANTIALIAS)
	weatherPhoto = ImageTk.PhotoImage(pil_weatherPhoto_image)
	global weatherPhoto_label
	weatherPhoto_label = Label(weather_info_frame, image=weatherPhoto)
	weatherPhoto_label.pack(fill="both")

	current_tmp_label = Label(weather_info_frame, text=current_tmp_text)
	current_tmp_label.config(font = ("Courier", 20, "bold"))
	current_tmp_label.pack(fill="both")

def weather_set():
	weather_data = lw.weather_get_api()
	print(weather_data)

def weather_anime():
	#이미지 바꿀때 사용
	pil_weatherPhoto_image = Image.open("./images/weather_sunny_2.png")
	pil_weatherPhoto_image = pil_weatherPhoto_image.resize((50,50), Image.ANTIALIAS)
	weatherPhoto = ImageTk.PhotoImage(pil_weatherPhoto_image)
	weatherPhoto_label.config(image=weatherPhoto)

'''
# 화면 생성
# base_gui로 연결시 주석처리
root = Tk()
root.title("날씨 정보 프로그램")
root.geometry("320x480+300+50") # 480 : 가로, 680 : 세로, 100 : x좌표, 300 : y좌표
root.resizable(False, False) # x, y 너비 변경 불가, 창 크기 변경 불가

weather_info(root)

#base_gui로 연결시 주석처리
root.mainloop()
'''