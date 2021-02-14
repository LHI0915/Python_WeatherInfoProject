# tkinter 모듈안에 있는 모든 것을 가져가 쓰겠다.
from tkinter import * 
import requests
import json
import xmltodict
import search_location as sl
import weather_gui as wg

final_location = []

# search 버튼 클릭 시 동작
def searchBtn_cmd(entry_insert_location,get_location_label,location_listbox,api_key):
    

    # 버튼 누르면 입력한 주소 위치를 가져옴 
    entry_location_info = entry_insert_location.get()
    get_location_label.configure(text = entry_location_info)

    # entry와 리스트 삭제
    entry_insert_location.delete(0,END) # entry에 있는 내용 삭제
    location_listbox.delete(0,END)

    global juso_list 
    juso_list = sl.get_location(entry_location_info,api_key)
    #print(juso_list)

    if len(juso_list):
        for juso in juso_list:
            location_listbox.insert(END,juso)
    else:
        message = "검색된 주소가 없습니다."
        location_listbox.insert(0,message)

# 리스트 항목 클릭 시 동작
def weather_search_cmd(root,first_frame,location_listbox):
    # curselection은 인덱스로 가져옴
    if len(location_listbox.curselection())== 0:
        return

    select_location_index = location_listbox.curselection()[0] # 선택한 항목의 인덱스 번호를 알려줌
    select_location = location_listbox.get(select_location_index) #선택한 항목

    #!!! select_location이 리스트에서 선택한 항목 !!!
    for juso_key in juso_list.keys():
        if juso_key == select_location:
            final_location = juso_list[juso_key]
            print(final_location)
            first_frame.destroy()
            wg.weather_info(root,final_location)
            break

def first_start_page(root):
    # api_key 가져오기
    api_key = sl.get_api_key()
    
    first_frame = Frame(root)
    first_frame.pack(side = "top", fill = "both", expand=True)

    # information about this funtion
    info_label = Label(first_frame, text="주소 또는 장소를 입력해주세요", relief="solid", bd =1)
    info_label.config(font = ("Courier",13,"bold"))
    info_label.pack(side = "top", fill="both", padx=3, pady=3)

    # 지역 입력 entry와 검색 버튼을 담을 frame
    searchBtn_insertEntry_frame = Frame(first_frame, relief = "solid", bd = 1)
    searchBtn_insertEntry_frame.pack(fill = "both", padx=3, pady=3)

    # search button
    search_btn = Button(searchBtn_insertEntry_frame, text="검색", command = lambda: searchBtn_cmd(entry_insert_location,get_location_label,location_listbox,api_key))
    search_btn.pack(side = "right")

    # insert location
    # text와 entry의 차이는 text는 여러줄 입력 가능, entry는 한 줄만 입력 가능
    entry_insert_location = Entry(searchBtn_insertEntry_frame)
    entry_insert_location.pack(side="left", fill="x", expand=True, ipady=4)

    # get entry location info for test
    get_location_label = Label(first_frame, text = "주소 정보 확인", relief="solid", bd=1)
    get_location_label.config(font=("Courier",10,"bold"))

    # listbox and Scrollbar frame
    listbox_scrollbar_frame = Frame(first_frame)
    listbox_scrollbar_frame.pack(fill = "both", padx=3, pady=3)

    # listbox Scrollbar
    listbox_scrollbar = Scrollbar(listbox_scrollbar_frame)
    listbox_scrollbar.pack(side = "right",fill="y")

    # searched location list
    # selectmode : 선택할 개수(extended : 여러개, single : 한 개), height : 리스트에 보여질 항목의 개수 ex. 3이면 3개만
    # yscrollcommand를 통한 set을 해주지 않으면 스크롤 기능을 못함 
    
    location_listbox = Listbox(listbox_scrollbar_frame, selectmode = "single", height=10, yscrollcommand=listbox_scrollbar.set) 
    location_listbox.pack(side="left", fill="both", expand=True)

    weather_search_btn = Button(first_frame, relief="solid", bd=1, text="날씨 정보 검색",command = lambda: weather_search_cmd(root,first_frame,location_listbox))
    weather_search_btn.config(font=("Courier",10,"bold"))
    weather_search_btn.pack(side="bottom", fill="both", padx=3, pady=3)


    # Scrollbar 기능을 사용하기 위해 두 가지를 해주어야 함. 1. listbox에 yscrollcommand set하기. 2. scrollbar command에 yview
    listbox_scrollbar.config(command = location_listbox.yview)