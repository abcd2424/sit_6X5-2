import streamlit as st
import random

st.title("🪑 텍스트 기반 교실 자리 배치 프로그램 (6열 × 5행)")

ROWS, COLS = 5, 6  # 세로 5행, 가로 6열
TOTAL_STUDENTS = 32

def generate_seats(students):
    seats = [["" for _ in range(COLS)] for _ in range(ROWS + 1)]  # 6행 자리 위해 +1
    idx = 0
    # 기본 5행 6열 자리 배치
    for r in range(ROWS):
        for c in range(COLS):
            seats[r][c] = students[idx]
            idx += 1
    # 6행(인덱스 5) 3열(인덱스 2), 4열(인덱스 3)에 남은 2명 배치
    seats[ROWS][2] = students[idx]
    seats[ROWS][3] = students[idx + 1]
    return seats

if "students" not in st.session_state:
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students

seats = generate_seats(st.session_state.students)

# 칠판 표시
st.markdown("### 📋 칠판 (Board)")

# 자리 텍스트 출력 (세로 5 + 1행)
for r in range(ROWS + 1):
    row_display = ""
    for c in range(COLS):
        seat = seats[r][c]
        if seat == "":
            row_display += "⬜️    "  # 빈 자리 표시
        else:
            row_display += f"**{seat:02d}**  "
    st.markdown(row_display)

st.markdown("---")

if st.button("🔄 자리 초기화"):
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students
    st.experimental_rerun()
