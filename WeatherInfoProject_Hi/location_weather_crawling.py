import requests
import re
from bs4 import BeautifulSoup

def location_weather(final_location):
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={0} 날씨" .format(final_location)

    response = requests.get(url)
    #print(response.text)
    soup = BeautifulSoup(response.text,"lxml")
    
    # return temp_and_cast
    weather = soup.find("div",attrs={"class":"weather_box"})
    temperture = weather.find("p", attrs={"class" : "info_temperature"}).text.replace("도씨","")
    cast = weather.find("p", attrs={"class" : "cast_txt"}).text.split(",")[0]
    
    weather_infos = {}
    weather_infos["온도"]=temperture
    weather_infos["날씨"]=cast

    dust_and_ozone = weather.findAll("dd",attrs={"class":re.compile("^lv")})
    
    weather_infos["미세먼지"]= dust_and_ozone[0].text
    weather_infos["초미세먼지"]=dust_and_ozone[1].text
    weather_infos["오존"]=dust_and_ozone[2].text

    probabilities = weather.findAll("li", attrs={"class":re.compile("on now merge1|on now")})
    probability = [i.find("dd",attrs={"class":"weather_item _dotWrapper"}).text.replace(" ","") for i in probabilities]
    
    weather_infos["강수확률"]=probability[1]
    weather_infos["바람"]=probability[2]
    weather_infos["습도"]=probability[3]

    return weather_infos
    
if __name__=="__main__":
    location_weather("일산서구 주엽동")

    
    


