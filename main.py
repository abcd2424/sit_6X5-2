import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(page_title="자리 배치", layout="centered")

st.title("🪑 교실 책상 자리 배치 프로그램")

if "students" not in st.session_state:
    students = list(range(1, 33))
    random.shuffle(students)
    st.session_state.students = students

def get_seat_df(students):
    rows, cols = 6, 5
    data = []
    idx = 0
    for i in range(rows):
        for j in range(cols):
            # 마지막 행 (i==5) 3열,4열 비움
            if i == rows - 1 and j in [2, 3]:
                continue
            data.append({
                "번호": int(students[idx]),
                "행": i + 1,  # 세로 1부터 6까지 순서로 바꿈
                "열": j + 1
            })
            idx += 1

    # 비운 자리(6행 3,4열) 대신 1행 3,4열에 31,32번 배치(원하는 위치 변경 가능)
    data.append({"번호": int(students[idx]), "행": 1, "열": 3})
    data.append({"번호": int(students[idx + 1]), "행": 1, "열": 4})
    return pd.DataFrame(data)

df = get_seat_df(st.session_state.students)

fig = go.Figure()

desk_width = 0.8
desk_height = 0.8
desk_color = "#ADD8E6"  # 연한 하늘색

for _, row in df.iterrows():
    x = row["열"]
    y = row["행"]
    번호 = row["번호"]
    fig.add_shape(
        type="rect",
        x0=x - desk_width / 2, x1=x + desk_width / 2,
        y0=y - desk_height / 2, y1=y + desk_height / 2,
        line=dict(color="black"),
        fillcolor=desk_color
    )
    fig.add_annotation(
        x=x, y=y,
        text=f"<b>{int(번호)}</b>",
        showarrow=False,
        font=dict(size=18, color="black"),
        xanchor="center",
        yanchor="middle"
    )

# 칠판을 맨 위로 올림 (행 0 ~ 0.4)
fig.add_shape(
    type="rect",
    x0=0.5, x1=5.5,
    y0=6.6, y1=7.0,
    line=dict(color="black", width=3),
    fillcolor="#444444"
)
fig.add_annotation(
    x=3,
    y=6.8,
    text="<b>칠판 (Board)</b>",
    showarrow=False,
    font=dict(size=20, color="white"),
    xanchor="center",
    yanchor="middle"
)

fig.update_layout(
    xaxis=dict(range=[0.5, 5.5], title="열", showgrid=False, zeroline=False),
    yaxis=dict(range=[0, 7.2], title="행", showgrid=False, zeroline=False),
    width=700,
    height=700,
    margin=dict(t=40, l=10, r=10, b=10),
    plot_bgcolor="white",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

if st.button("🔄 자리 초기화"):
    students = list(range(1, 33))
    random.shuffle(students)
    st.session_state.students = students
    st.experimental_rerun()
