import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.title("Plotly를 활용한 미세중력렌즈 시뮬레이션")

# --- 설정값 ---
st.sidebar.header("시뮬레이션 설정")
orbital_period = st.sidebar.slider("행성 공전 주기 (프레임 수)", 100, 500, 200, key="period_slider")
planet_mass_ratio = st.sidebar.slider("행성-중심별 질량비 (중심별=1)", 0.001, 0.1, 0.01, format="%.3f", key="mass_ratio_slider")
observer_angle_deg = st.sidebar.slider("관찰자 초기 각도 (도)", 0, 360, 90, key="observer_angle_slider")

# --- 시뮬레이션 상수 ---
R_STAR = 1.0  # 중심별 반지름 (단위)
R_ORBIT = 5.0  # 행성 궤도 반지름 (단위)

# --- 미세중력렌즈 광도 계산 함수 (더 정교하게 구현 필요) ---
def calculate_magnification(planet_pos, star_pos, observer_angle_rad, planet_mass_ratio):
    # 이 함수는 실제 미세중력렌즈 배율 공식을 적용해야 합니다.
    # 여기서는 단순화를 위해, 관찰자 시선과 중심별-행성 정렬 시 광도가 증가하도록 설정합니다.

    # planet_pos: (x, y) 튜플
    # star_pos: (0, 0)
    # observer_angle_rad: 관찰자 시선 각도 (라디안)

    # 행성과 중심별 사이의 거리
    distance_to_star = np.sqrt(planet_pos[0]**2 + planet_pos[1]**2)

    # 행성의 중심별 기준 각도
    planet_angle = np.arctan2(planet_pos[1], planet_pos[0])

    # 관찰자 시선과 행성-중심별 정렬을 확인 (단순화된 방식)
    # 관찰자 시선은 (cos(observer_angle_rad), sin(observer_angle_rad)) 방향
    # 행성의 상대적인 위치를 관찰자 시선에 투영
    # 예시: 행성이 관찰자 시선과 중심별 사이에 매우 가깝게 정렬될 때
    
    # 여기서부터 실제 미세중력렌즈 공식을 도입해야 합니다.
    # UDM (Universal Deviation from the Mean) 모델의 단순화된 형태를 사용할 수 있습니다.
    # 예를 들어, 아인슈타인 반경 내에 들어왔을 때 광도가 급증하는 형태

    # Example: Simple alignment check
    # 렌즈 중심(별)과 광원(배경별) 사이의 각 거리 'u'를 계산해야 함
    # 여기서는 행성이 '렌즈' 역할을 하므로, 행성과 관찰자 시선과의 거리가 중요
    
    # 렌즈 (행성)와 광원 (중심별)의 시선 분리 각도
    # (실제로는 배경별이 광원이고, 행성이 렌즈, 관찰자가 그 효과를 보는 것)
    # 여기서는 중심별이 광원이고, 행성이 중심별을 가리키는 시선 주변을 통과할 때 광도 증가 가정.

    magnification = 1.0 # 기본 광도

    # 가정: 행성이 관찰자 시선에 거의 놓일 때 (즉, 행성-중심별-관찰자가 정렬될 때)
    # 렌즈 효과의 정점은 관찰자-렌즈-소스가 완벽하게 정렬될 때 발생합니다.
    # 여기서는 행성이 렌즈 역할을 하므로, 중심별과 관찰자 시선 사이의 '아인슈타인 반경' 영역을
    # 행성이 통과할 때 광도 증가를 시뮬레이션합니다.

    # 렌즈 (행성)가 광원 (중심별)과 관찰자 사이를 통과할 때의 시선 거리를 계산
    # Simplified approach: If the planet is close to the observer's line of sight through the star
    
    # Calculate the angle between the planet's position vector and the observer's line of sight
    planet_angle_from_observer = np.arctan2(planet_pos[1] - R_ORBIT*np.sin(observer_angle_rad)*0, planet_pos[0] - R_ORBIT*np.cos(observer_angle_rad)*0)
    
    # Approximation for alignment:
    # If the planet passes very close to the star *from the observer's perspective*
    # This is a very simplified model for micro-lensing, which requires more complex physics.
    
    # Let's use a simpler heuristic: when planet is 'in front' of the star relative to observer
    # If the observer is at (R_OBS * cos(observer_angle), R_OBS * sin(observer_angle))
    # And the star is at (0,0)
    # The planet (planet_x, planet_y) is 'in front' if its projection on the observer-star line is between them
    
    # For a general microlensing event, magnification A = (u^2 + 2) / (u * sqrt(u^2 + 4))
    # where u is the normalized source-lens separation (normalized by Einstein radius)
    # u = d_proj / R_E (projected distance / Einstein radius)

    # Simplified approach for animation: simulate a peak when the planet passes near the observer's direct line to the star
    # Let's consider the x-axis as the observer's view when observer_angle_deg is 90 or 270 (y-axis view)
    # Or, more generally, align with the observer's chosen direction
    
    # Angle between planet position and the observer's line of sight to the star
    angle_diff = np.abs(planet_angle - observer_angle_rad)
    
    # Normalize to be between 0 and pi
    if angle_diff > np.pi:
        angle_diff = 2 * np.pi - angle_diff

    # Simulate a peak when the angle difference is small and planet is near the star's apparent disk
    threshold_angle = np.radians(10) # Within 10 degrees of alignment
    
    if angle_diff < threshold_angle:
        # Distance from the star center to the point on the observer's line of sight that the planet crosses
        # This is a simplified proxy for 'u' in microlensing, not physically rigorous
        
        # Simulate a bump. The strength of the bump depends on planet_mass_ratio
        magnification = 1.0 + planet_mass_ratio * (1 - (angle_diff / threshold_angle)**2) * 50 # Example scaling
        magnification = max(1.0, magnification) # Ensure it doesn't go below 1

    return magnification

# --- 데이터 준비 ---
frames_data = []
lightcurve_values = []
times = np.arange(orbital_period)

for t in times:
    angle = 2 * np.pi * t / orbital_period
    planet_x = R_ORBIT * np.cos(angle)
    planet_y = R_ORBIT * np.sin(angle)

    observer_angle_rad = np.radians(observer_angle_deg)
    
    # 광도 계산
    current_magnification = calculate_magnification(
        (planet_x, planet_y), (0, 0), observer_angle_rad, planet_mass_ratio
    )
    lightcurve_values.append(current_magnification)

    # 각 프레임에 대한 데이터 저장
    frames_data.append({
        'data': [
            go.Scatter(x=[planet_x], y=[planet_y], mode='markers', marker=dict(size=8, color='blue')),
            go.Scatter(x=times[:t+1], y=lightcurve_values[:t+1], mode='lines', line=dict(color='green'))
        ],
        'name': f'frame_{t}'
    })

# --- 초기 그래프 생성 ---
# 서브플롯 생성: 왼쪽은 공전 애니메이션, 오른쪽은 광도 변화 그래프
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("행성 공전 시뮬레이션", "미세중력렌즈 광도 변화"),
                    specs=[[{'type': 'xy'}, {'type': 'xy'}]])

# 1. 공전 시뮬레이션 서브플롯 (왼쪽)
fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers',
                         marker=dict(size=20, color='gold'),
                         name='중심별'), row=1, col=1)
fig.add_trace(go.Scatter(x=[R_ORBIT * np.cos(0)], y=[R_ORBIT * np.sin(0)], mode='markers',
                         marker=dict(size=8, color='blue'),
                         name='행성'), row=1, col=1)

# 관찰자 시선 추가 (고정된 선)
observer_x_end = R_ORBIT * 6 * np.cos(observer_angle_rad)
observer_y_end = R_ORBIT * 6 * np.sin(observer_angle_rad)
fig.add_trace(go.Scatter(x=[-observer_x_end, observer_x_end], y=[-observer_y_end, observer_y_end],
                         mode='lines', line=dict(color='red', dash='dash'),
                         name='관찰자 시선'), row=1, col=1)

fig.update_xaxes(range=[-R_ORBIT * 1.2, R_ORBIT * 1.2], row=1, col=1)
fig.update_yaxes(range=[-R_ORBIT * 1.2, R_ORBIT * 1.2], scaleanchor="x", scaleratio=1, row=1, col=1) # 비율 고정

# 2. 광도 변화 서브플롯 (오른쪽)
fig.add_trace(go.Scatter(x=[0], y=[lightcurve_values[0]], mode='lines',
                         line=dict(color='green'),
                         name='광도'), row=1, col=2)

fig.update_xaxes(range=[0, orbital_period], title_text="시간", row=1, col=2)
fig.update_yaxes(range=[min(0.9, min(lightcurve_values) - 0.05), max(1.5, max(lightcurve_values) + 0.05)],
                 title_text="상대 광도", row=1, col=2)

# --- 애니메이션 설정 ---
fig.frames = [go.Frame(data=frame['data'], name=frame['name']) for frame in frames_data]

# 애니메이션 재생/일시정지 버튼 설정
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}]),
                dict(label="Pause",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
            ]
        )
    ]
)

# 슬라이더 설정 (선택 사항: 타임라인 슬라이더)
sliders = [
    dict(
        steps=[
            dict(
                method="animate",
                args=[
                    [f"frame_{t}"],
                    {"mode": "immediate", "frame": {"duration": 50, "redraw": True}, "transition": {"duration": 0}}
                ],
                label=str(t)
            ) for t in times
        ],
        transition={"duration": 0},
        x=0.08,
        y=0,
        currentvalue={"font": {"size": 12}, "prefix": "Frame: ", "visible": True},
        len=0.92,
    )
]
fig.update_layout(sliders=sliders)


# --- Streamlit 앱에 Plotly 그래프 표시 ---
st.plotly_chart(fig, use_container_width=True)

st.info("💡 **참고:** Plotly 애니메이션은 웹 기반이므로 훨씬 부드럽게 재생됩니다. 'Play' 버튼을 클릭하여 애니메이션을 시작하세요. 미세중력렌즈의 광도 계산 로직은 이 예시에서 단순화되어 있으며, 실제 물리 공식을 적용하여 더 정확하게 만들 수 있습니다.")
