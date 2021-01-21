import pandas as pd
# 엑셀파일 읽은 후 csv파일로 저장하기
df = pd.ExcelFile("xylist.xlsx").parse(sheet_name=0, dtype=object, engine='xlrd', verbose=True)

# 구분자가 데이터에 존재할 수도 있기 때문에 미리 공백으로 치환한다.
# df = df.apply(lambda x: x.str.replace(',',' ')) # 모든 컬럼에 하기 보다는
# df['my_column'] = df['my_column'].str.replace(',',' ') # str형 컬럼에만 하길 권장한다.
# str형으로 변환이 불가능한 경우 오류가 발생하거나 데이터가 유실되므로 주의하자

df.to_csv(path_or_buf='xylist.csv', sep=',', header=True, index=False, mode='w', encoding='CP949')

# csv파일 읽기

xylist = pd.read_csv('xylist.csv', engine='c', dtype=str, sep=',', encoding='CP949')

uniq_xylist = xylist[['1단계', '2단계', '3단계','격자 X', '격자 Y']].drop_duplicates()

uniq_xylist.to_csv(path_or_buf='uniq_xylist.csv', sep=',', header=True, index=False, mode='w', encoding='CP949')


print(uniq_xylist)