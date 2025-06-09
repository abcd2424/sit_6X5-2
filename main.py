import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(page_title="자리 배치", layout="centered")

st.title("🪑 교실 자리 배치 프로그램")
st.write("총 32명의 학생을 6행 5열로 배치하고, 나머지 2명은 마지막 줄 중앙에 위치합니다.")

# 초기화 버튼
if "students" not in st.session_state or st.button("🔄 자리 초기화"):
    students = list(range(1, 33))
    random.shuffle(students)
    st.session_state.students = students

# 자리 배치 계산
def get_seat_df(students):
    rows, cols = 6, 5
    data = []
    idx = 0

    for i in range(rows):
        for j in range(cols):
            if i == rows - 1 and j in [2, 3]:
                continue
            data.append({
                "번호": students[idx],
                "행": rows - i,
                "열": j + 1
            })
            idx += 1

    # 마지막 2명 중앙 배치 (2.5열, 3.5열)
    data.append({"번호": students[idx], "행": 1, "열": 2.5})
    data.append({"번호": students[idx + 1], "행": 1, "열": 3.5})

    return pd.DataFrame(data)

df = get_seat_df(st.session_state.students)

# 좌석 시각화
fig = go.Figure()
for _, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["열"]],
        y=[row["행"]],
        text=str(row["번호"]),
        mode="markers+text",
        marker=dict(size=40, color="lightblue"),
        textposition="middle center",
        hoverinfo="text"
    ))

fig.update_layout(
    title="자리 배치도",
    xaxis=dict(title="열", tickmode='linear', dtick=1, range=[0.5, 5.5]),
    yaxis=dict(title="행", tickmode='linear', dtick=1, range=[0.5, 6.5]),
    showlegend=False,
    width=700,
    height=600,
    margin=dict(t=40, l=10, r=10, b=10)
)

st.plotly_chart(fig, use_container_width=True)
