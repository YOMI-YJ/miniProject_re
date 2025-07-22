import requests
import pandas as pd

url = "https://www.reb.or.kr/r-one/openapi/SttsApiTblItm.do"

params = {
    "key": "b40b44288b324ea383afc68d9a6be1d7",
    "type": "json",
    "pIndex": 1,
    "pSize": 100,
    "STATBL_ID": "A_2024_00200"  # 여전히 사용자가 관심 있는 외국인 주택소유 통계
}

res = requests.get(url, params=params)
print(res.status_code)
print(res.text)
