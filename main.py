import streamlit as st
import random

st.title("🪑 텍스트 기반 교실 자리 배치 프로그램")

ROWS, COLS = 6, 5
TOTAL_STUDENTS = 32

def generate_seats(students):
    seats = [["" for _ in range(COLS)] for _ in range(ROWS)]
    idx = 0
    for r in range(ROWS):
        for c in range(COLS):
            # 6행(인덱스 5) 3열(2),4열(3) 자리 비우기
            if r == ROWS - 1 and c in [2, 3]:
                continue
            seats[r][c] = students[idx]
            idx += 1
    # 비운 자리(6행 가운데) 2명 배치
    seats[ROWS - 1][2] = students[idx]
    seats[ROWS - 1][3] = students[idx + 1]
    return seats

if "students" not in st.session_state:
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students

seats = generate_seats(st.session_state.students)

# 칠판 표시
st.markdown("### 📋 칠판 (Board)")
# 텍스트로 자리 출력
for r in range(ROWS):
    row_display = ""
    for c in range(COLS):
        seat = seats[r][c]
        if seat == "":
            row_display += "⬜️    "  # 빈 자리 표시
        else:
            # 번호 굵게 표시 (마크다운 볼드체)
            row_display += f"**{seat:02d}**  "
    st.markdown(row_display)

st.markdown("---")

if st.button("🔄 자리 초기화"):
    students = list(range(1, TOTAL_STUDENTS + 1))
    random.shuffle(students)
    st.session_state.students = students
    st.experimental_rerun()
