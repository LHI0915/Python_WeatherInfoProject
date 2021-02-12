import requests
from bs4 import BeautifulSoup

def location_weather(final_location):
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={0} 날씨" .format(final_location)

    response = requests.get(url)

    soup = BeautifulSoup(response.text,"lxml")
    
    weather = soup.find("div",attrs={"class":"info_data"})
    temperture = weather.find("p", attrs={"class" : "info_temperature"}).text.replace("도씨","")
    cast = weather.find("p", attrs={"class" : "cast_txt"}).text.split(",")[0]
    
    temp_and_cast = []
    temp_and_cast.append(temperture)
    temp_and_cast.append(cast)

    print(temp_and_cast)

    return temp_and_cast

if __name__=="__main__":
    location_weather("울산광역시 남구 신정동")

    
    


