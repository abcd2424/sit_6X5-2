
import random
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Output, Input

# Dash 앱 초기화
app = Dash(__name__)
server = app.server  # 배포용

# 좌석 위치 계산 함수
def get_seat_positions(student_numbers):
    rows, cols = 6, 5
    data = []
    idx = 0

    for i in range(rows):
        for j in range(cols):
            # 6행 3열, 4열은 제외
            if i == rows - 1 and j in [2, 3]:
                continue
            data.append({
                "번호": student_numbers[idx],
                "행": rows - i,
                "열": j + 1
            })
            idx += 1

    # 마지막 2명 중앙 배치
    extra_positions = [(rows, 2.5), (rows, 3.5)]
    for pos in extra_positions:
        data.append({
            "번호": student_numbers[idx],
            "행": pos[0],
            "열": pos[1]
        })
        idx += 1

    return pd.DataFrame(data)

# 좌석 시각화 함수
def create_figure(df):
    fig = go.Figure()

    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["열"]],
            y=[row["행"]],
            text=str(row["번호"]),
            mode="markers+text",
            marker=dict(size=40, color='lightgreen'),
            textposition="middle center",
            hoverinfo="text"
        ))

    fig.update_layout(
        title="자리 배치도",
        xaxis=dict(title="열", tickmode='linear', dtick=1, range=[0.5, 5.5]),
        yaxis=dict(title="행", tickmode='linear', dtick=1, range=[0.5, 6.5]),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        width=700,
        height=600
    )

    return fig

# Dash 레이아웃 구성
app.layout = html.Div([
    html.H2("교실 자리배치 프로그램"),
    dcc.Graph(id='seat-graph'),
    html.Button('자리 초기화', id='reset-button', n_clicks=0)
])

# 콜백: 버튼 클릭 시 자리 무작위 재배치
@app.callback(
    Output('seat-graph', 'figure'),
    Input('reset-button', 'n_clicks')
)
def update_seats(n_clicks):
    students = list(range(1, 33))  # 번호 1~32
    random.shuffle(students)
    df = get_seat_positions(students)
    return create_figure(df)

# 앱 실행
if __name__ == '__main__':
    app.run_server(debug=True)
