import requests
import pandas as pd
import os

# 가져올 STATBL_ID 2개
target_ids = {
    "A_2024_00206": "국적별 외국인주택소유현황_공동주택",
    "A_2024_00207": "국적별 외국인주택소유현황_단독주택"
}

all_data = []

for statbl_id, statbl_name in target_ids.items():
    params = {
        "key": "b40b44288b324ea383afc68d9a6be1d7",
        "type": "json",
        "pIndex": 1,
        "pSize": 1000,
        "STATBL_ID": statbl_id,
        "DTACYCLE_CD": "HY"  # 반기 데이터
    }

    response = requests.get("https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do", params=params)
    result = response.json()

    if "SttsApiTblData" in result:
        rows = result["SttsApiTblData"][1]["row"]
        for row in rows:
            row["STATBL_ID"] = statbl_id
            row["STATBL_NM"] = statbl_name  # 이름도 추가
            all_data.append(row)

# DataFrame 생성 및 저장
df = pd.DataFrame(all_data)

# 현재 경로 기준 저장
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "foreign_stats_filtered.csv")
df.to_csv(save_path, index=False, encoding='utf-8-sig')

print("✅ 필요한 2개 통계표만 저장 완료!")
