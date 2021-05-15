from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import location_weather_crawling as lwc
import location_gui as lg

def update_weather_animation(wcnt,weather_images,weather_image_label):
	weather_image = weather_images[wcnt]
	weather_image_label.configure(image=weather_image)
	
	wcnt += 1
	if wcnt == 7:
		wcnt = 0

	weather_info_frame.after(400, update_weather_animation, wcnt, weather_images,weather_image_label) 

def weather_info(root,location):
	#날씨정보 프레임
	global weather_info_frame 
	weather_info_frame = Frame(root)
	weather_info_frame.pack(side = "top", fill = "both", pady=40)

	#location_gui에서 위치 정보 받아오기
	location_text = location
	print("location text : ", location_text)

	# 받아온 위치정보를 이용해서 날씨 정보값 받아오기
	weather_infos = lwc.location_weather(location_text)

	current_tmp_text = weather_infos["온도"]
	weather_text = weather_infos["날씨"]

	print(current_tmp_text)
	print(weather_text)
	
	# 날씨 정보 이미지로 받아오기
	weather_dict = {"맑음" : "sunny", "흐림" : "cloudy","구름많음":"cloudy", "구름조금":"partly_sunny", \
		"비":"rainy", "눈":"snowy","천둥번개":"stormy","바람":"windy"}
	print(weather_dict["k"])
	global weather_images
	weatherPhoto_file_name = "./images/weather_" + weather_dict[weather_text] + ".gif"
	
	weather_images = [PhotoImage(file = weatherPhoto_file_name, format="gif -index %i" %(i)) for i in range(7)]
	
	weather_image_label = Label(weather_info_frame)

	update_weather_animation(0, weather_images, weather_image_label)
	weather_image_label.pack()
	
	location_label = Label(weather_info_frame, text=location_text)
	location_label.config(font = ("Courier",12,"bold"))
	location_label.pack(anchor="s")

	weather_label = Label(weather_info_frame, text=weather_text)
	weather_label.config(font = ("Courier", 10))
	weather_label.pack(fill="both")
	
	current_tmp_label = Label(weather_info_frame, text=current_tmp_text)
	current_tmp_label.config(font = ("Courier", 20, "bold"))
	current_tmp_label.pack(fill="both")

	tree = ttk.Treeview(weather_info_frame, columns=["one","two"])
	tree.column("#0",width=120, anchor="center")
	tree.heading("#0",text="날씨 정보",anchor="center")

	tree.column("#1",width=195, anchor="center")
	tree.heading("#1",text="수치",anchor="center")

	for key, value in weather_infos.items():
		tree.insert("","end",text=key,values=value)

	tree.pack(padx=5, pady=5)


