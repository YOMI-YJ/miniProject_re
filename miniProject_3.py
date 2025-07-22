import requests
import pandas as pd

url = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"

params = {
    "key": "b40b44288b324ea383afc68d9a6be1d7",
    "type": "json",
    "pIndex": 1,
    "pSize": 100,
    "STATBL_ID": "A_2024_00201",
    "DTACYCLE_CD": "HY",

}
# API 호출
response = requests.get(url, params=params)
data = response.json()

# DataFrame 변환
df = pd.DataFrame(data['SttsApiTblData'][1]['row'])

# CSV 저장
csv_filename = "foreign_homeowners_stats.csv"
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

print(f"✅ CSV 저장 완료: {csv_filename}")