import requests
import json
import xmltodict
import config


def get_api_key():
    api_key = config.location_api_key
    return api_key

def get_location(entry_location_info, api_key):
    juso_list = {}
    try:
        for page_count in range(1,3):
            url = "https://www.juso.go.kr/addrlink/addrLinkApi.do" 
                
            data = {
                "confmKey" : api_key,
                "currentPage" : page_count,
                "countPerPage" : "5",
                "keyword" : entry_location_info
            }

            response = requests.post(url, data = data)
            location_json_type = xmltodict.parse(response.text)#사용하기 불편한 list 타입
            location_json_type = json.dumps(location_json_type)#json 형태인데 한글로 쓰여있지 않음
            location_json_type = json.loads(location_json_type)# 최종 한글로 쓰여진 json 타입
                    
            results_infos = location_json_type["results"]["juso"]
        
            for results_info in results_infos:
                if len(results_infos) < 6:
                    for dict_info in results_info:
                        if dict_info =="roadAddr" :
                            juso_list[results_info["roadAddr"]] = results_info['siNm']+ " " +results_info['sggNm']+ " "+results_info['emdNm']
                elif len(results_infos) >= 6 and results_info == "roadAddr": 
                    juso_list[results_infos["roadAddr"]] = results_infos['siNm']+" "+results_infos['sggNm']+" "+results_infos['emdNm']
                                
        return juso_list
    except:
        return juso_list

if __name__ == "__main__":
    # search_location.py에서 프로그램 실행시 동작
    pass
    
