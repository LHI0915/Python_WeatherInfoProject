# tkinter 모듈안에 있는 모든 것을 가져가 쓰겠다.
from tkinter import * 
import requests
import json
import xmltodict
import search_location as sl

import pandas as pd

# search 버튼 클릭 시 동작
def searchBtn_cmd():
    # api_key = sl.get_api_key()

    # 버튼 누르면 입력한 주소 위치를 가져옴 
    entry_location_info = entry_insert_location.get()
    get_location_label.configure(text = entry_location_info)

    # entry와 리스트 삭제
    entry_insert_location.delete(0,END) # entry에 있는 내용 삭제
    location_listbox.delete(0,END)

    #juso_list가 없는 경우 if문 실행해 cvs를 읽어 리스트를 받아온다
    juso_list = []
    if len(juso_list) == 0:
        juso_list = sl.read_csv()

    global search_juso_list
    search_juso_list = sl.get_location(juso_list, entry_location_info)

    if len(search_juso_list):
        for juso in search_juso_list:
            location_listbox.insert(END,juso[0])
    else:
        message = "검색된 주소가 없습니다."
        location_listbox.insert(0,message)

# 리스트 항목 클릭 시 동작
def select(event):
    # curselection은 인덱스로 가져옴
    if len(location_listbox.curselection())== 0:
        return
    
    select_location_index = location_listbox.curselection()[0] # 선택한 항목의 인덱스 번호를 알려줌
    select_location = location_listbox.get(select_location_index) #선택한 항목
    get_location_label.configure(text=select_location)

    #!!! selection_location이 리스트에서 선택한 항목 !!!

def location_search_list(root):
    # information about this funtion
    # info_label = Label(root, text="주소 또는 장소를 입력해주세요", relief="solid", bd =1)
    info_label = Label(root, text="주소 또는 장소를 입력해주세요")
    info_label.config(font = ("Courier",13,"bold"))
    info_label.pack(side = "top", fill="both", padx=3, ipady=5)

    # 지역 입력 entry와 검색 버튼을 담을 frame
    global searchBtn_insertEntry_frame
    searchBtn_insertEntry_frame = Frame(root)
    searchBtn_insertEntry_frame.pack(fill = "both", padx=3, pady=3)

    # search button
    # photo = PhotoImage(file = "../images/search.png").subsample(50)
    # search_btn = Button(searchBtn_insertEntry_frame, image=photo, command = searchBtn_cmd)
    search_btn = Button(searchBtn_insertEntry_frame, text="검색", command = searchBtn_cmd)
    search_btn.config(font = ("Courier",10,"bold"))
    search_btn.pack(side = "right")

    # insert location
    # text와 entry의 차이는 text는 여러줄 입력 가능, entry는 한 줄만 입력 가능
    global entry_insert_location
    entry_insert_location = Entry(searchBtn_insertEntry_frame)
    entry_insert_location.pack(side="left", fill="x", expand=True, ipady=4)

    # get entry location info for test
    global get_location_label
    get_location_label = Label(root, text = "주소 정보 확인")
    get_location_label.config(font=("Courier",10,"bold"))
    get_location_label.pack(side="bottom", fill="both", padx=3, pady=3)

    # listbox and Scrollbar frame
    listbox_scrollbar_frame = Frame(root)
    listbox_scrollbar_frame.pack(fill = "both", padx=3, pady=3)

    # listbox Scrollbar
    listbox_scrollbar = Scrollbar(listbox_scrollbar_frame)
    listbox_scrollbar.pack(side = "right",fill="y")

    # searched location list
    # selectmode : 선택할 개수(extended : 여러개, single : 한 개), height : 리스트에 보여질 항목의 개수 ex. 3이면 3개만
    # yscrollcommand를 통한 set을 해주지 않으면 스크롤 기능을 못함 
    global location_listbox
    location_listbox = Listbox(listbox_scrollbar_frame, selectmode = "single", height=50, yscrollcommand=listbox_scrollbar.set) 
    root.bind("<Button-1>", select) # root가 아닌 listbox에 bind를 걸면 한 템포 늦음?(두 번 클릭해야 원하는 값이 들어감)
    location_listbox.pack(side="left", fill="both", expand=True)

    # Scrollbar 기능을 사용하기 위해 두 가지를 해주어야 함. 1. listbox에 yscrollcommand set하기. 2. scrollbar command에 yview
    listbox_scrollbar.config(command = location_listbox.yview)