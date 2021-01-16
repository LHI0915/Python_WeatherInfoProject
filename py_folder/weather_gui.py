from tkinter import *
from PIL import Image, ImageTk

import time

# 시계 기능
def update_clock():
	now = time.strftime("%H:%M:%S")
	clock_label.config(text=str(now))
	root.after(1000, update_clock) 

# 화면 생성
root = Tk()
root.title("날씨 정보 프로그램")
#root.geometry("480x680") # 가로 세로 크기 지정
root.geometry("320x480+300+50") # 480 : 가로, 680 : 세로, 100 : x좌표, 300 : y좌표
root.resizable(False, False) # x, y 너비 변경 불가, 창 크기 변경 불가

# 상태창 프레임
statusBar_frame = Frame(root, bg = "black")
statusBar_frame.pack(side = "top", fill = "both")

pil_signalPhoto_image = Image.open("images/statusbar_signal.png")
pil_signalPhoto_image = pil_signalPhoto_image.resize((10,12), Image.ANTIALIAS)
signalPhoto = ImageTk.PhotoImage(pil_signalPhoto_image)
signalPhoto_label = Label(statusBar_frame, image=signalPhoto, background = "black")
signalPhoto_label.pack(side = "left", padx=3, fill = "both")

pil_wifiPhoto_image = Image.open("images/statusbar_wifi.png")
pil_wifiPhoto_image = pil_wifiPhoto_image.resize((15,12), Image.ANTIALIAS)
wifiPhoto = ImageTk.PhotoImage(pil_wifiPhoto_image)
wifiPhoto_label = Label(statusBar_frame, image=wifiPhoto, background = "black")
wifiPhoto_label.pack(side = "left", padx=1, fill = "both")

pil_batteryPhoto_image = Image.open("images/statusbar_battery.png")
pil_batteryPhoto_image = pil_batteryPhoto_image.resize((20,12), Image.ANTIALIAS)
batteryPhoto = ImageTk.PhotoImage(pil_batteryPhoto_image)
batteryPhoto_label = Label(statusBar_frame, image=batteryPhoto, background = "black")
batteryPhoto_label.pack(side = "right", padx=3, fill = "both")

clock_label = Label(statusBar_frame, text = "11:40", background = "black", foreground="white")
clock_label.config(font = ("Courier",10,"bold"))
clock_label.pack(anchor = "center", fill = "both")

#날씨정보 프레임
#location_text : loaction_gui의 input을 받는다
#weather_text & current_temp_text : location_text를 이용한 날씨 api이용
location_text = "경기도 고양시 화전동"
weather_text = "맑음"
current_tmp_text = "20" + "℃"

location_label = Label(root, text=location_text)
location_label.config(font = ("Courier",10,"bold"))
location_label.pack(anchor="s", ipady = 20)

weather_label = Label(root, text=weather_text)
weather_label.config(font = ("Courier", 8))
weather_label.pack(fill="both")

current_tmp_label = Label(root, text=current_tmp_text)
current_tmp_label.config(font = ("Courier", 20, "bold"))
current_tmp_label.pack(fill="both")

update_clock() 
root.mainloop()