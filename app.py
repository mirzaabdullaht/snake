import streamlit as st
import time
import random

st.set_page_config(page_title="Snake Game", page_icon="🐍", layout="centered")

st.title("🐍 Snake Game")

# --- Game Config ---
GRID_SIZE = 20
SPEED = 0.15  # lower = faster snake

# --- Initialize session state ---
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
if "food" not in st.session_state:
    st.session_state.food = (10, 10)
if "direction" not in st.session_state:
    st.session_state.direction = "RIGHT"
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- Helper Functions ---
def new_food():
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in st.session_state.snake:
            return pos

def move_snake():
    head_x, head_y = st.session_state.snake[0]
    if st.session_state.direction == "UP":
        head_x -= 1
    elif st.session_state.direction == "DOWN":
        head_x += 1
    elif st.session_state.direction == "LEFT":
        head_y -= 1
    elif st.session_state.direction == "RIGHT":
        head_y += 1

    new_head = (head_x % GRID_SIZE, head_y % GRID_SIZE)

    # Collision with self
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    # Check food
    if new_head == st.session_state.food:
        st.session_state.food = new_food()
        st.session_state.score += 1
    else:
        st.session_state.snake.pop()

# --- Game UI ---
col1, col2, col3, col4 = st.columns(4)
if col1.button("⬅️ Left"):
    if st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
if col2.button("⬆️ Up"):
    if st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
if col3.button("⬇️ Down"):
    if st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
if col4.button("➡️ Right"):
    if st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

placeholder = st.empty()

# --- Main Game Loop ---
if not st.session_state.game_over:
    for _ in range(1000):
        board = [["⬛"] * GRID_SIZE for _ in range(GRID_SIZE)]
        for x, y in st.session_state.snake:
            board[x][y] = "🟩"
        fx, fy = st.session_state.food
        board[fx][fy] = "🍎"
        board_display = "\n".join(["".join(row) for row in board])
        placeholder.text(board_display)
        move_snake()
        time.sleep(SPEED)
        if st.session_state.game_over:
            break

# --- Game Over ---
if st.session_state.game_over:
    st.error(f"💀 Game Over! Final Score: {st.session_state.score}")
    if st.button("🔁 Restart"):
        for key in ["snake", "food", "direction", "score", "game_over"]:
            if key == "snake":
                st.session_state[key] = [(5, 5), (5, 4), (5, 3)]
            elif key == "food":
                st.session_state[key] = (10, 10)
            elif key == "direction":
                st.session_state[key] = "RIGHT"
            elif key == "score":
                st.session_state[key] = 0
            elif key == "game_over":
                st.session_state[key] = False
        st.rerun()
