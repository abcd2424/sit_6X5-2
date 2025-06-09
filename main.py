import streamlit as st
import pandas as pd
import random

st.title("🪑 표 형태 교실 자리 배치 프로그램 (6열 × 5행)")

ROWS, COLS = 5, 6
TOTAL_STUDENTS = 32

def generate_seats(front_students, other_students):
    seats = [["" for _ in range(COLS)] for _ in range(ROWS + 1)]

    # 앞줄 학생 무작위 섞기
    front_row_seats = front_students[:COLS]
    random.shuffle(front_row_seats)
    remaining_front = front_students[COLS:]

    # 뒤에 앉는 학생들 + 앞줄 초과 인원 합치기
    remaining_students = remaining_front + other_students
    random.shuffle(remaining_students)

    idx_remaining = 0

    # 앞줄 6자리 전부 채움 (앞줄 학생 + 부족한 자리 뒤 학생으로 채움)
    for c in range(COLS):
        if c < len(front_row_seats):
            seats[0][c] = front_row_seats[c]
        else:
            if idx_remaining < len(remaining_students):
                seats[0][c] = remaining_students[idx_remaining]
                idx_remaining += 1
            else:
                seats[0][c] = ""

    # 2~5행 자리 배치
    for r in range(1, ROWS):
        for c in range(COLS):
            if idx_remaining < len(remaining_students):
                seats[r][c] = remaining_students[idx_remaining]
                idx_remaining += 1
            else:
                seats[r][c] = ""

    # 6행 3,4열 자리 배치
    for pos in [2, 3]:
        if idx_remaining < len(remaining_students):
            seats[ROWS][pos] = remaining_students[idx_remaining]
            idx_remaining += 1
        else:
            seats[ROWS][pos] = ""
    # 6행 나머지는 빈칸
    for pos in [0, 1, 4, 5]:
        seats[ROWS][pos] = ""

    return seats

def seats_to_dataframe(seats):
    df = pd.DataFrame(seats, columns=[f"열 {i+1}" for i in range(COLS)])
    df.index = [f"행 {i+1}" for i in range(len(seats))]
    df.replace("", pd.NA, inplace=True)
    return df

if "students" not in st.session_state:
    st.session_state.students = list(range(1, TOTAL_STUDENTS + 1))

st.write("앞에 앉고 싶은 친구들의 번호를 쉼표(,)로 구분해 입력하세요. 예: 1,3,5")
front_input = st.text_input("앞줄 배치할 학생 번호 입력")

front_students = []
if front_input.strip():
    try:
        front_students = [int(x.strip()) for x in front_input.split(",") if x.strip().isdigit()]
    except Exception:
        st.error("번호를 정확히 숫자로 쉼표 구분해서 입력해주세요.")

other_students = [s for s in st.session_state.students if s not in front_students]

seats = generate_seats(front_students, other_students)
df_seats = seats_to_dataframe(seats)

st.markdown("### 📋 칠판 (Board)")
st.write("→ 칠판은 여기에 위치합니다 (교실 앞)")

st.table(df_seats)

if st.button("🔄 자리 초기화"):
    st.session_state.students = list(range(1, TOTAL_STUDENTS + 1))
