import requests
import pandas as pd

url = "https://www.reb.or.kr/r-one/openapi/SttsApiTbl.do"
params = {
    "Key": "b40b44288b324ea383afc68d9a6be1d7",
    "Type": "json",
    "pIndex": 1,
    "pSize": 1000
}

res = requests.get(url, params=params)
data = res.json()

# 원하는 데이터는 data["SttsApiTbl"][1]["row"] 안에 있음
df = pd.DataFrame(data["SttsApiTbl"][1]["row"])
print(df.head())
