from tkinter import *
from PIL import Image, ImageTk

import time
import location_gui as lg
import weather_gui as wg

location=""

# 시계 기능
def update_clock():
	now_date = time.strftime("%Y %b %d %a, ")
	now_time = time.strftime("%p %I:%M:%S")
	# 초 없앤 코드
	# now = time.strftime("%p %I:%M")

	date_clock_label.config(text=now_date + now_time)
	root.after(1000, update_clock) 

def update_weather_animation(wcnt):
	weatherPhoto_frame = weatherPhoto_frames[wcnt]
	weatherPhoto_label.configure(image=weatherPhoto_frame)
	
	wcnt += 1
	if wcnt == 7:
		wcnt = 0

	root.after(400, update_weather_animation, wcnt) 

# tkinter 화면 생성
root = Tk()
root.title("날씨 정보 프로그램")
root.geometry("320x480+300+50") # 480 : 가로, 680 : 세로, 100 : x좌표, 300 : y좌표
root.resizable(False, False) # x, y 너비 변경 불가, 창 크기 변경 불가

# 상태창 프레임
statusBar_frame = Frame(root, bg = "black")
statusBar_frame.pack(side = "top", fill = "both")

pil_signalPhoto_image = Image.open("../images/statusbar_signal.png")
pil_signalPhoto_image = pil_signalPhoto_image.resize((10,12), Image.ANTIALIAS)
signalPhoto = ImageTk.PhotoImage(pil_signalPhoto_image)
signalPhoto_label = Label(statusBar_frame, image=signalPhoto, background = "black")
signalPhoto_label.pack(side = "left", padx=3, fill = "both")

pil_wifiPhoto_image = Image.open("../images/statusbar_wifi.png")
pil_wifiPhoto_image = pil_wifiPhoto_image.resize((15,12), Image.ANTIALIAS)
wifiPhoto = ImageTk.PhotoImage(pil_wifiPhoto_image)
wifiPhoto_label = Label(statusBar_frame, image=wifiPhoto, background = "black")
wifiPhoto_label.pack(side = "left", padx=1, fill = "both")

pil_batteryPhoto_image = Image.open("../images/statusbar_battery.png")
pil_batteryPhoto_image = pil_batteryPhoto_image.resize((20,12), Image.ANTIALIAS)
batteryPhoto = ImageTk.PhotoImage(pil_batteryPhoto_image)
batteryPhoto_label = Label(statusBar_frame, image=batteryPhoto, background = "black")
batteryPhoto_label.pack(side = "right", padx=3, fill = "both")

date_clock_label = Label(statusBar_frame, text = "2020 Nov 4, Sun 11:40", background = "black", foreground="white")
date_clock_label.config(font = ("Courier",8,"bold"))
date_clock_label.pack(anchor = "center", fill = "both")

#날씨 gui 연결
lg.location_search_list(root)
if lg.get_location_label["text"] == "주소 정보 확인":
	"""
	해야할일
	프레임 이동하는거 공부해오기
	https://www.delftstack.com/ko/howto/python-tkinter/how-to-switch-frames-in-tkinter/
	"""
	check_location()
else:
	# 넘어온 sky_state를 이용한 image 매칭
	weather_top_space_label = Label(root, pady=4)
	weather_top_space_label.pack(fill="both")

	weatherPhoto_label = Label(root, image = "")
	weatherPhoto_label.pack(fill= "both")

	weather_text = wg.weather_info(root, location)

	if weather_text:
		weatherPhoto_file_name =  "../images/weather_" + weather_text + ".gif"
		weatherPhoto_frames = [PhotoImage(file = weatherPhoto_file_name, format = 'gif -index %i' %(i)) for i in range(7)]

		update_weather_animation(0)

#1초 마다 시간 업데이트
update_clock()

# tkinter 화면
root.mainloop()