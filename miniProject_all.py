import requests
import pandas as pd
import os

# 1. 통계표 목록 요청
url = "https://www.reb.or.kr/r-one/openapi/SttsApiTbl.do"
params = {
    "Key": "b40b44288b324ea383afc68d9a6be1d7",
    "Type": "json",
    "pIndex": 1,
    "pSize": 1000
}

response = requests.get(url, params=params)
data = response.json()

# 2. 전체 통계표 → DataFrame으로
df = pd.DataFrame(data['SttsApiTbl'][1]['row'])

# 3. "외국인" 포함 통계만 필터링
foreign_df = df[df['STATBL_NM'].str.contains('외국인')]

# 4. STATBL_ID → STATBL_NM 매핑 dict 생성
statbl_name_map = dict(zip(foreign_df["STATBL_ID"], foreign_df["STATBL_NM"]))

# 5. 통계표별 데이터 가져오기
all_data = []

for statbl_id in foreign_df['STATBL_ID']:
    params = {
        "key": "b40b44288b324ea383afc68d9a6be1d7",
        "type": "json",
        "pIndex": 1,
        "pSize": 1000,
        "STATBL_ID": statbl_id,
        "DTACYCLE_CD": "HY"
    }

    response = requests.get("https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do", params=params)
    result = response.json()

    if "SttsApiTblData" in result:
        rows = result["SttsApiTblData"][1]["row"]
        for row in rows:
            row["STATBL_ID"] = statbl_id
            row["STATBL_NM"] = statbl_name_map.get(statbl_id, "알 수 없음")  # 통계표 이름 추가
            all_data.append(row)

# 6. 전체 DataFrame으로 변환
df_all = pd.DataFrame(all_data)

# 7. 현재 스크립트 경로에 저장
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, "foreign_related_stats_all.csv")
df_all.to_csv(save_path, index=False, encoding='utf-8-sig')

print("✅ CSV 파일 저장 완료:", save_path)
