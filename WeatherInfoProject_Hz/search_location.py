import csv

'''
import config

def get_api_key():
    api_key = config.location_api_key
    
    return api_key
'''
def read_csv():
    juso_list = []
    open_csv = open('../res/xylist.csv', 'r', encoding='CP949')
    read_csv = csv.reader(open_csv)
    for line in read_csv:
        line_list = []

        juso_text = line[0] + ' ' + line[1] + ' ' + line[2]
        line_list.append(juso_text)

        # nx == line[3] and ny == line[4]
 
        # print(line_list)

        juso_list.append(line_list)

    open_csv.close()

    return juso_list

def get_location(juso_list, entry_location_info):
    search_juso_list = []

    for juso in juso_list:
        if entry_location_info in juso[0]: 
            search_juso_list.append(juso)

    return search_juso_list