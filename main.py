import streamlit as st
import pandas as pd
import random

st.title("🪑 표 형태 교실 자리 배치 프로그램 (6열 × 5행)")

ROWS, COLS = 5, 6
TOTAL_STUDENTS = 32

def generate_seats(students):
    seats = [["" for _ in range(COLS)] for _ in range(ROWS + 1)]
    idx = 0
    for r in range(ROWS):
        for c in range(COLS):
            seats[r][c] = students[idx]
            idx += 1
    seats[ROWS][2] = students[idx]
    seats[ROWS][3] = students[idx + 1]
    return seats

def seats_to_dataframe(seats):
    df = pd.DataFrame(seats, columns=[f"열 {i+1}" for i in range(COLS)])
    df.index = [f"행 {i+1}" for i in range(len(seats))]
    df.replace("", pd.NA, inplace=True)
    return df

if "students" not in st.session_state:
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students

# 초기화 버튼
if st.button("🔄 자리 초기화"):
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students
    # st.experimental_rerun() 삭제했으니 따로 호출 안 해도 됨

seats = generate_seats(st.session_state.students)
df_seats = seats_to_dataframe(seats)

st.markdown("### 📋 칠판 (Board)")
st.write("→ 칠판은 여기에 위치합니다 (교실 앞)")

st.table(df_seats)
