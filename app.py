import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 불러오기
df = pd.read_csv("foreign_stats_filtered.csv")

# 주택 유형 명칭 간소화
df['STATBL_NM'] = df['STATBL_NM'].replace({
    '국적별 외국인주택소유현황_공동주택': '공동주택',
    '국적별 외국인주택소유현황_단독주택': '단독주택'
})

# 🔍 사이드바 필터
statbl_options = st.sidebar.multiselect("🏠 주택 유형 선택", df['STATBL_NM'].unique(), default=df['STATBL_NM'].unique())
df_filtered = df[df['STATBL_NM'].isin(statbl_options)]

wrt_options = st.sidebar.multiselect("📆 기간 선택", sorted(df_filtered['WRTTIME_DESC'].unique()), default=sorted(df_filtered['WRTTIME_DESC'].unique()))
df_filtered = df_filtered[df_filtered['WRTTIME_DESC'].isin(wrt_options)]

itm_option = st.sidebar.selectbox("📌 항목 선택", df_filtered['ITM_FULLNM'].unique())
df_filtered = df_filtered[df_filtered['ITM_FULLNM'] == itm_option]

# 📊 1. 전체 막대그래프 (국적별 소유 현황)
st.subheader("📊 전체 국적별 외국인 주택 소유 현황 (막대그래프)")
bar_data = df_filtered.groupby(['CLS_FULLNM'])['DTA_VAL'].sum().reset_index().sort_values(by='DTA_VAL', ascending=False)

fig_bar = px.bar(
    bar_data,
    x='CLS_FULLNM',
    y='DTA_VAL',
    labels={'CLS_FULLNM': '국적', 'DTA_VAL': '소유 주택 수'},
    title='전체 기간 + 항목 합산 기준'
)
st.plotly_chart(fig_bar, use_container_width=True)


# 🥧 2. 주택유형별 원형차트 (단일 기간일 경우만)
st.subheader("🥧 주택유형별 국적 분포 (원형 차트)")

if len(wrt_options) == 1:
    for statbl in statbl_options:
        st.markdown(f"**{wrt_options[0]} / {statbl}**")
        pie_data = df_filtered[
            (df_filtered['STATBL_NM'] == statbl) &
            (df_filtered['WRTTIME_DESC'] == wrt_options[0])
        ]

        if not pie_data.empty:
            fig_pie = px.pie(
                pie_data,
                names='CLS_FULLNM',
                values='DTA_VAL',
                title=f"{statbl} - {wrt_options[0]} 기준 국적별 분포",
                hole=0.3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info(f"해당 조건의 데이터가 없습니다: {statbl} / {wrt_options[0]}")
else:
    st.warning("⛔ 원형차트는 '기간'을 1개만 선택했을 때만 표시됩니다.")

# 📄 3. 필터링된 데이터 표
st.subheader("📄 필터링된 데이터 보기")
st.dataframe(df_filtered[['WRTTIME_DESC', 'STATBL_NM', 'CLS_FULLNM', 'ITM_FULLNM', 'DTA_VAL']], use_container_width=True)
