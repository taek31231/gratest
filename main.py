import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

st.set_page_config(layout="wide")

st.title("미세중력렌즈 효과 시뮬레이션")

# --- 설정값 ---
st.sidebar.header("시뮬레이션 설정")
orbital_period = st.sidebar.slider("행성 공전 주기 (단위 시간)", 100, 500, 200)
planet_mass_ratio = st.sidebar.slider("행성-중심별 질량비 (중심별=1)", 0.001, 0.1, 0.01, format="%.3f")
observer_angle_deg = st.sidebar.slider("관찰자 초기 각도 (도)", 0, 360, 90)

# --- 시뮬레이션 변수 초기화 ---
R_STAR = 1.0  # 중심별 반지름 (단위)
R_ORBIT = 5.0  # 행성 궤도 반지름 (단위)

# 초기화 함수 (애니메이션 시작 시 호출)
def init_animation(ax_orbit, ax_lightcurve):
    ax_orbit.set_xlim(-R_ORBIT * 1.2, R_ORBIT * 1.2)
    ax_orbit.set_ylim(-R_ORBIT * 1.2, R_ORBIT * 1.2)
    ax_orbit.set_aspect('equal', adjustable='box')
    ax_orbit.grid(True)
    ax_orbit.set_title("행성 공전 시뮬레이션")

    ax_lightcurve.set_xlim(0, orbital_period)
    ax_lightcurve.set_ylim(0.9, 1.5) # 광도 범위 (예상치)
    ax_lightcurve.set_xlabel("시간")
    ax_lightcurve.set_ylabel("상대 광도")
    ax_lightcurve.set_title("미세중력렌즈 광도 변화")
    ax_lightcurve.grid(True)

    return []

# 애니메이션 업데이트 함수
def update_animation(frame, fig, ax_orbit, ax_lightcurve,
                     star_plot, planet_plot, observer_line, lightcurve_line, lightcurve_data):
    # 행성 위치 계산 (간단한 원형 궤도 가정)
    angle = 2 * np.pi * frame / orbital_period
    planet_x = R_ORBIT * np.cos(angle)
    planet_y = R_ORBIT * np.sin(angle)

    # 행성 및 중심별 시각화 업데이트
    planet_plot.set_data(planet_x, planet_y)

    # 관찰자 위치 및 시선 표시 (초기 각도 기준)
    observer_angle_rad = np.radians(observer_angle_deg)
    observer_x = 10 * R_ORBIT * np.cos(observer_angle_rad)
    observer_y = 10 * R_ORBIT * np.sin(observer_angle_rad)
    observer_line.set_data([observer_x, -observer_x], [observer_y, -observer_y]) # 시선을 따라 그려진 선

    # --- 미세중력렌즈 광도 계산 (매우 단순화된 모델, 실제 구현은 복잡) ---
    # 이 부분은 실제 미세중력렌즈 공식을 적용하여야 합니다.
    # 여기서는 행성이 중심별에 가까워질수록 광도가 증가하는 경향만 보여줍니다.
    # 중심별과의 거리 기반으로 광도 계산 (예시)
    distance_to_star = np.sqrt(planet_x**2 + planet_y**2)
    # 관찰자 시선에 행성이 들어왔을 때의 광도 증가를 시뮬레이션
    # 이 값은 미세중력렌즈 배율 공식을 통해 정교하게 계산되어야 합니다.
    # 단순화를 위해 중심별-행성-관찰자 정렬 시 광도가 증가하도록 설정
    
    # 관찰자 시선과 행성-중심별 간의 각도
    angle_to_observer = np.arctan2(planet_y - observer_y, planet_x - observer_x)
    angle_from_star_to_planet = np.arctan2(planet_y, planet_x)

    # 행성이 관찰자 시선과 중심별 사이에 있을 때 광도 증가 가정
    # 이 부분은 실제 미세중력렌즈 공식을 적용하여야 합니다.
    # for simplicity, let's assume maximum magnification when aligned with observer's view and star
    alignment_threshold = 0.1 # Example threshold for alignment
    is_aligned = np.abs(np.cos(angle_to_observer - angle_from_star_to_planet)) > (1 - alignment_threshold) # Check if roughly aligned
    
    # Simplified magnification factor (placeholder)
    magnification = 1.0
    if is_aligned and distance_to_star < R_ORBIT * 0.2: # If aligned and close to star (for simplicity)
         # A more complex calculation involving the Einstein radius would go here
        magnification = 1.0 + planet_mass_ratio * 50 # Example: scale by planet mass ratio
        
    lightcurve_data.append(magnification)
    lightcurve_line.set_data(np.arange(len(lightcurve_data)), lightcurve_data)
    ax_lightcurve.set_xlim(0, max(orbital_period, len(lightcurve_data) + 10)) # Adjust x-axis dynamically
    ax_lightcurve.set_ylim(min(0.9, min(lightcurve_data) - 0.05), max(1.5, max(lightcurve_data) + 0.05)) # Adjust y-axis dynamically

    return [star_plot, planet_plot, observer_line, lightcurve_line]

# --- Streamlit 앱 구성 ---
if st.button("애니메이션 시작/정지"):
    st.session_state.running = not st.session_state.get('running', False)
    if st.session_state.running:
        st.write("애니메이션 실행 중...")
    else:
        st.write("애니메이션 정지됨.")

# Matplotlib figure와 axes 준비
fig, (ax_orbit, ax_lightcurve) = plt.subplots(1, 2, figsize=(15, 6))

# 초기 plot 요소들
star_plot, = ax_orbit.plot(0, 0, 'o', color='gold', markersize=20, label='중심별')
planet_plot, = ax_orbit.plot([], [], 'o', color='blue', markersize=8, label='행성')
observer_line, = ax_orbit.plot([], [], 'r--', label='관찰자 시선')
lightcurve_line, = ax_lightcurve.plot([], [], 'g-', label='광도 변화')

# 전역 변수로 광도 데이터 저장
lightcurve_data = []

# 애니메이션 객체 생성 (초기화 및 업데이트 함수 연결)
# St.pyplot에 애니메이션을 직접 넘겨주기 어려우므로, 프레임을 수동으로 관리하거나 gif로 저장 후 표시하는 방법을 고려할 수 있습니다.
# 여기서는 간단하게 한 프레임씩 업데이트하는 방식으로 구성합니다.
# 실제 애니메이션은 gif로 저장하거나, 더 복잡한 Streamlit 애니메이션 기법을 사용해야 합니다.

# Streamlit에서 FuncAnimation을 직접 실행하고 실시간으로 업데이트하는 것은 까다롭습니다.
# 가장 현실적인 방법은 매 프레임마다 matplotlib plot을 새로 그리고 st.pyplot으로 업데이트하는 것입니다.
# 다만 이는 "애니메이션"처럼 보이지 않고, 각 프레임이 개별적으로 업데이트되는 형태입니다.

# 다른 방법으로는 애니메이션을 GIF로 저장 후 Streamlit에 표시하거나,
# Javascript 기반의 라이브러리 (예: Plotly, Altair)를 사용하는 것이 더 적합할 수 있습니다.

# 여기서는 매 프레임마다 그림을 다시 그리는 방식으로 단순화하여 보여드립니다.
# 이 방식은 실시간 "애니메이션"이라기보다는 "프레임 업데이트"에 가깝습니다.

if st.session_state.get('running', False):
    for frame in range(orbital_period): # 공전 주기만큼 프레임 생성
        update_animation(frame, fig, ax_orbit, ax_lightcurve,
                         star_plot, planet_plot, observer_line, lightcurve_line, lightcurve_data)
        st.pyplot(fig) # 매 프레임마다 그림 업데이트
        plt.clf() # 그림 초기화 (매번 새로 그려야 함)
        st.empty() # 이전 그림 지우기 (반복 업데이트 시 필요)
else:
    init_animation(ax_orbit, ax_lightcurve)
    st.pyplot(fig)

st.info("💡 **참고:** Streamlit에서 `FuncAnimation`을 실시간으로 직접 제어하기는 어렵습니다. 위의 코드는 각 프레임을 별도로 업데이트하는 방식이며, 부드러운 애니메이션을 위해서는 GIF 저장 후 표시 또는 JavaScript 기반 라이브러리(Plotly, Altair) 사용을 고려하는 것이 좋습니다.")
