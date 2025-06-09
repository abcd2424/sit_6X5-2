import streamlit as st
import pandas as pd
import random

st.title("🪑 표 형태 교실 자리 배치 프로그램 (6열 × 5행)")

ROWS, COLS = 5, 6
TOTAL_STUDENTS = 32

def generate_seats(students):
    # 6행 자리까지 포함, 빈칸은 빈 문자열
    seats = [["" for _ in range(COLS)] for _ in range(ROWS + 1)]
    idx = 0
    for r in range(ROWS):
        for c in range(COLS):
            seats[r][c] = students[idx]
            idx += 1
    # 6행 3열,4열에 나머지 2명 배치
    seats[ROWS][2] = students[idx]
    seats[ROWS][3] = students[idx + 1]
    return seats

def seats_to_dataframe(seats):
    # 행 번호를 행 인덱스 대신 표시할 수 있도록 행 번호 붙이기
    df = pd.DataFrame(seats, columns=[f"열 {i+1}" for i in range(COLS)])
    df.index = [f"행 {i+1}" for i in range(len(seats))]
    # 빈 문자열 → NaN으로 바꾸면 테이블에서 빈칸으로 표시됨
    df.replace("", pd.NA, inplace=True)
    return df

if "students" not in st.session_state:
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students

seats = generate_seats(st.session_state.students)
df_seats = seats_to_dataframe(seats)

st.markdown("### 📋 칠판 (Board)")
st.write("→ 칠판은 여기에 위치합니다 (교실 앞)")

st.table(df_seats)

if st.button("🔄 자리 초기화"):
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students
    st.experimental_rerun()
