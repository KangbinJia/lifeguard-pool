import math
import random

import matplotlib.pyplot as plt
import streamlit as st

# Simulation constants
WIDTH, HEIGHT = 800, 600
POOL_Y_START = 100
POOL_Y_END = 450
LIFEGUARD_START = (WIDTH // 2, HEIGHT - 20)
V_LAND = 300.0  # effective pixels per second on land
V_WATER = 120.0  # effective pixels per second in water


def random_target():
    return (
        random.randint(50, WIDTH - 50),
        random.randint(POOL_Y_START + 20, POOL_Y_END - 20),
    )


def compute_travel_time(entry_x, target):
    land_dist = math.hypot(entry_x - LIFEGUARD_START[0], POOL_Y_END - LIFEGUARD_START[1])
    water_dist = math.hypot(target[0] - entry_x, target[1] - POOL_Y_END)
    return land_dist / V_LAND + water_dist / V_WATER


def find_optimal_entry(target):
    best_x = 0
    best_time = float("inf")
    for x in range(0, WIDTH + 1, 2):
        t = compute_travel_time(x, target)
        if t < best_time:
            best_time = t
            best_x = x
    return best_x, best_time


def draw_simulation(target, entry_x, best_entry_x):
    entry_point = (entry_x, POOL_Y_END)
    best_entry_point = (best_entry_x, POOL_Y_END)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(HEIGHT, 0)
    ax.axis("off")

    ax.add_patch(plt.Rectangle((0, POOL_Y_START), WIDTH, POOL_Y_END - POOL_Y_START, color="#add8e6"))
    ax.add_patch(plt.Rectangle((0, POOL_Y_END), WIDTH, HEIGHT - POOL_Y_END, color="#f4a460"))
    ax.plot([0, WIDTH], [POOL_Y_END, POOL_Y_END], color="black", linewidth=2)

    ax.scatter(*LIFEGUARD_START, c="black", s=80, zorder=5)
    ax.text(LIFEGUARD_START[0] + 10, LIFEGUARD_START[1] + 5, "Lifeguard", color="black", fontsize=10)

    ax.scatter(*target, c="red", s=80, zorder=5)
    ax.text(target[0] + 10, target[1] + 5, "Target", color="red", fontsize=10)

    ax.scatter(*entry_point, c="yellow", edgecolors="black", s=80, zorder=5)
    ax.text(entry_point[0] + 10, entry_point[1] + 5, "Selected entry", color="black", fontsize=10)

    ax.scatter(*best_entry_point, c="green", s=80, zorder=5)
    ax.text(best_entry_point[0] + 10, best_entry_point[1] + 5, "Optimal entry", color="green", fontsize=10)

    ax.plot([LIFEGUARD_START[0], entry_point[0]], [LIFEGUARD_START[1], entry_point[1]], color="black", linewidth=2)
    ax.plot([entry_point[0], target[0]], [entry_point[1], target[1]], color="black", linewidth=2)

    ax.plot([LIFEGUARD_START[0], best_entry_point[0]], [LIFEGUARD_START[1], best_entry_point[1]], color="green", linewidth=2, linestyle="--")
    ax.plot([best_entry_point[0], target[0]], [best_entry_point[1], target[1]], color="green", linewidth=2, linestyle="--")

    return fig


st.set_page_config(page_title="Lifeguard Pool Simulation", page_icon="🌊", layout="wide")
st.title("Lifeguard Pool Simulation")

if "target" not in st.session_state:
    st.session_state.target = random_target()
    st.session_state.entry_x = WIDTH // 2

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Controls")
    if st.button("New random target"):
        st.session_state.target = random_target()
        st.session_state.entry_x = WIDTH // 2

    entry_x = st.slider("Shoreline entry X", min_value=0, max_value=WIDTH, value=st.session_state.entry_x, step=1)
    st.session_state.entry_x = entry_x

    best_entry_x, best_time = find_optimal_entry(st.session_state.target)
    chosen_time = compute_travel_time(entry_x, st.session_state.target)

    st.metric("Your chosen path time", f"{chosen_time:.3f} sec")
    st.metric("Optimal path time", f"{best_time:.3f} sec")
    st.write(f"Optimal entry X: {best_entry_x}")
    st.write("The green dashed path is the computed optimal route.")
    st.write("The black path is your chosen route.")

with col2:
    fig = draw_simulation(st.session_state.target, st.session_state.entry_x, best_entry_x)
    st.pyplot(fig)

st.markdown("---")
st.write(
    "This Streamlit app keeps the same logic as the desktop version: the lifeguard runs faster on land and swims slower in water, "
    "so the fastest rescue route may use a non-straight path through the shoreline."
)
