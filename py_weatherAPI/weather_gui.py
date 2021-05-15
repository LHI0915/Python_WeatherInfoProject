"""
실행 파일 __name__ == __main__: 만들기

"""

from tkinter import *
from PIL import Image, ImageTk

import tkinter.ttk

import location_weather as lw

def weather_info(root, location):
	#날씨정보 프레임
	#location_text : loaction_gui의 input을 받는다
	#weather_text & current_temp_text : location_text를 이용한 날씨 api이용

	weather_info_frame = Frame(root)
	weather_info_frame.pack(side = "top", fill="both", pady=25)
	
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

	global weather_detail_treeview
	weather_detail_treeview = tkinter.ttk.Treeview(root, columns=["one"], show="tree", selectmode="none")
	#weather_detail_treeview = tkinter.ttk.Treeview(root, columns=["one"], selectmode="none")
	weather_detail_treeview.pack()

	weather_detail_treeview.column("one", width= "100",  anchor="center")
	weather_detail_treeview.heading("one", text= " 값 ", anchor="center")

	weather_detail =[(" ", " "),("강수확률", "-"), 
		("낙뢰확률", "-"),	("강수량", "-"),	("습도", "-"), 
		("최저기온", "-"), ("최고기온", "-"), 
		("풍향", "-"),	("풍속", "-")
	]

	for i in range(len(weather_detail)):
		weather_detail_treeview.insert("", "end", text=weather_detail[i][0], values=weather_detail[i][1], iid=weather_detail[i][0], tag="TAG")

	weather_text = weather_set(location)
	weather_detail_treeview.tag_configure('TAG', background='white', font = ("Courier", 9,"bold"))

	return weather_text

def weather_set(location):
	weather_data = lw.get_weather_info(location)

	location_label.config(text=location)
	
	weather_kor_text = ''
	weather_eng_text = ''

	# 날씨정보 프레임(weather_info_frame)
	# 날씨 애니메이션 text인 weather_eng_text 값 적용 
	if weather_data.get('lgt_code') and int(weather_data['lgt_code']) >= 3:
		weather_kor_text = '천둥/번개'
		weather_eng_text = 'stormy'
	elif weather_data.get('pty_code') and int(weather_data['pty_code']) != 0:
		weather_kor_text = weather_data['pty_state']
		if weather_data['pty_state'] == '비' :
			weather_eng_text = 'rainy'
		elif weather_data['pty_state'] == '눈' :
			weather_eng_text = 'snowy'
	elif weather_data.get('wsd') and float(weather_data['wsd']) >= 9:
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
		current_tmp_label.config(text=weather_data['tmp'])
	else:
		weather_label.config(text='-')
		current_tmp_label.config(text='- ℃')

	# 날씨정보 디테일 (weather_detail_treeview)
	if weather_data.get('pop'):
		weather_detail_treeview.item('강수확률',values=weather_data['pop'])
	if weather_data.get('lgt_code'):
		weather_detail_treeview.item('낙뢰확률',values=weather_data['lgt_state'])
	if weather_data.get('r06'):
		weather_detail_treeview.item('강수량',values=weather_data['r06'])
	if weather_data.get('reh'):
		weather_detail_treeview.item('습도',values=weather_data['reh'])
	if weather_data.get('tmpn'):
		weather_detail_treeview.item('최저기온',values=weather_data['tmpn'])
	if weather_data.get('tmpx'):
		weather_detail_treeview.item('최고기온',values=weather_data['tmpx'])
	if weather_data.get('vec'):
		vec_direction = (int(weather_data['vec']) + 22.5 * 0.5) / 22.5
		vec_direction = int(vec_direction)
		vec_direction_text = '-'
		
		if vec_direction == 0:	vec_direction_text = '북'
		elif vec_direction == 1:	vec_direction_text = '북북동'
		elif vec_direction == 2:	vec_direction_text = '북동'
		elif vec_direction == 3:	vec_direction_text = '동북동'
		elif vec_direction == 4:	vec_direction_text = '동'
		elif vec_direction == 5:	vec_direction_text = '동남동'
		elif vec_direction == 6:	vec_direction_text = '남동'
		elif vec_direction == 7:	vec_direction_text = '남남동'
		elif vec_direction == 8:	vec_direction_text = '남'
		elif vec_direction == 9:	vec_direction_text = '남남서'
		elif vec_direction == 10:	vec_direction_text = '남서'
		elif vec_direction == 11:	vec_direction_text = '서남서'
		elif vec_direction == 12:	vec_direction_text = '서'
		elif vec_direction == 13:	vec_direction_text = '서북서'
		elif vec_direction == 14:	vec_direction_text = '북서'
		elif vec_direction == 15:	vec_direction_text = '북북서'
		else:	vec_direction_text = '북'
		
		weather_detail_treeview.item('풍향', values = vec_direction_text)

	if weather_data.get('wsd'):
		weather_detail_treeview.item('풍속',values=weather_data['wsd']+'m/s')


	return weather_eng_text
