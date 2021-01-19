# https : //www.juso.go.kr/addrlink/addrLinkApi.do
# confmKey String Y - 신청시 발급받은 승인키
# currentPage Integer Y 1 현재 페이지 번호
# countPerPage Integer Y 10 페이지당 출력할 결과 Row 수
# keyword String Y - 주소 검색어
import requests
import json
import xmltodict

with open("./private data/location_apiKey.json", "r") as f:
    token = json.load(f)

print(token["api_key"])
api_key = token["api_key"]

juso_list = []

for page_count in range(1, 3) : 
    url = "https://www.juso.go.kr/addrlink/addrLinkApi.do" 
    data = {
        "confmKey" : api_key,
        "currentPage" : page_count,
        "countPerPage" : "5",
        "keyword" : "인천공항"
    }

    response = requests.post(url, data = data)
    location_json_type = xmltodict.parse(response.text)#사용하기 불편한 list 타입
    location_json_type = json.dumps(location_json_type)#json 형태인데 한글로 쓰여있지 않음
    location_json_type = json.loads(location_json_type)# 최종 한글로 쓰여진 json 타입

    print(location_json_type)
    results_infos = location_json_type["results"]["juso"]

    for results_info in results_infos : 
        if "roadAddr" in results_info : 
            juso_list.append(results_info["roadAddr"])