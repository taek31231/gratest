import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.title("미세중력렌즈 시뮬레이션")

# --- 설정값 ---
st.sidebar.header("시뮬레이션 설정")
orbital_period = st.sidebar.slider("행성 공전 주기 (프레임 수)", 100, 500, 200, key="period_slider")
planet_mass_ratio = st.sidebar.slider("행성 질량비 (중심별=1)", 0.001, 0.1, 0.01, format="%.3f", key="mass_ratio_slider")
observer_angle_deg = st.sidebar.slider("관찰자 초기 각도 (도)", 0, 360, 90, key="observer_angle_slider")
st.sidebar.markdown("---")
st.sidebar.info("💡 **팁:** 'Play' 버튼을 누르거나 아래 슬라이더를 움직여 애니메이션을 제어하세요.")

# --- 시뮬레이션 상수 ---
R_STAR = 0.5  # 중심별 시각적 반지름 (단위)
R_ORBIT = 5.0  # 행성 궤도 반지름 (단위)
R_OBSERVER_DIST = 10.0 # 관찰자의 중심별로부터의 거리 (시각화용)

# --- 미세중력렌즈 광도 계산 함수 (더 정교하게 구현 필요) ---
def calculate_magnification(planet_pos, observer_pos, star_pos, planet_mass_ratio):
    # 이 함수는 미세중력렌즈의 배율(magnification) 공식을 적용해야 합니다.
    # 여기서는 매우 단순화된 근사를 사용합니다.
    # 실제 microlensing은 광원(source star), 렌즈(lens object, 행성), 관찰자(observer)의 정렬에 따라 결정됩니다.
    # A = (u^2 + 2) / (u * sqrt(u^2 + 4)) where u = impact parameter / Einstein radius

    # 여기서는 중심별(star_pos)이 '광원'이고 행성(planet_pos)이 '렌즈' 역할을 하며,
    # 관찰자(observer_pos)가 이 효과를 보는 상황을 시뮬레이션합니다.

    # 1. 관찰자 시점에서 행성-중심별의 상대적 위치 (선형 근사)
    # 관찰자-중심별 벡터
    obs_to_star_vec = -np.array(observer_pos) # (0,0) - observer_pos
    # 관찰자-행성 벡터
    obs_to_planet_vec = np.array(planet_pos) - np.array(observer_pos)

    # 중심별을 기준으로 한 행성의 상대적 위치 (관찰자 시선에 수직한 거리)
    # 즉, 관찰자-중심별 라인에 대한 행성의 수직 거리
    # 투영된 거리: d_perp = |obs_to_planet_vec X obs_to_star_vec_unit|
    
    # 단순화를 위해, 관찰자 시점에서 행성과 중심별이 얼마나 정렬되어 있는지를 봅니다.
    # 중심별과 행성 사이의 거리가 너무 멀면 렌즈 효과는 무시합니다.
    
    magnification = 1.0 # 기본 광도 (증폭 없음)

    # 행성이 중심별에 가까이 있을 때만 렌즈 효과 고려
    if np.linalg.norm(np.array(planet_pos)) < R_ORBIT * 1.5: # 행성이 궤도 근처에 있을 때
        
        # 중심별과 행성 사이의 거리
        dist_star_planet = np.linalg.norm(np.array(planet_pos) - np.array(star_pos))
        
        # 관찰자, 행성, 중심별의 정렬을 시뮬레이션
        # 관찰자 -> 중심별 시선 벡터
        line_of_sight_vec = np.array(star_pos) - np.array(observer_pos)
        line_of_sight_unit = line_of_sight_vec / np.linalg.norm(line_of_sight_vec)

        # 행성의 위치에서 관찰자->중심별 시선까지의 수직 거리 (아인슈타인 반경의 'u'에 해당)
        # 이 부분이 microlensing의 impact parameter (u)와 관련됩니다.
        # u가 0에 가까울수록 증폭이 커집니다.
        # 여기서는 단순히 행성에서 시선까지의 거리를 사용합니다.
        
        # 행성 위치 (x_p, y_p), 시선 위의 점 (x_s, y_s) (예: 중심별), 시선 벡터 (dx, dy)
        # 점과 직선 사이의 거리 공식 응용
        # line_of_sight_vec = (star_pos[0]-observer_pos[0], star_pos[1]-observer_pos[1])
        # A = observer_pos[1] - star_pos[1]  (dy)
        # B = star_pos[0] - observer_pos[0]  (-dx)
        # C = -A*observer_pos[0] - B*observer_pos[1]
        
        # distance = |A*planet_pos[0] + B*planet_pos[1] + C| / sqrt(A^2 + B^2)

        # Simplified u: distance from planet to observer's line of sight to star
        # We need a point on the line of sight (e.g., star_pos) and direction vector (line_of_sight_vec)
        # Project planet_pos onto line_of_sight_vec and find the perpendicular distance
        
        # Vector from observer to planet
        vec_op = np.array(planet_pos) - np.array(observer_pos)
        
        # Dot product to find the component along the line of sight
        proj_length = np.dot(vec_op, line_of_sight_unit)
        
        # Point on the line of sight closest to the planet
        closest_point_on_los = np.array(observer_pos) + proj_length * line_of_sight_unit
        
        # Perpendicular distance from planet to line of sight
        perpendicular_dist = np.linalg.norm(np.array(planet_pos) - closest_point_on_los)
        
        # Normalize by an "Einstein radius" proxy for visualization
        # The Einstein radius (theta_E) depends on masses and distances.
        # Here, let's use a constant related to the orbital radius for normalization.
        einstein_radius_proxy = R_ORBIT * 0.1 # Example proxy, adjust for visual effect

        u = perpendicular_dist / einstein_radius_proxy
        
        # Micro-lensing magnification formula (point-source point-lens)
        if u <= 0.001: # Avoid division by zero and handle very close alignment
            magnification = 1.0 + planet_mass_ratio * 1000 # Max magnification for very close alignment
        else:
            magnification = (u**2 + 2) / (u * np.sqrt(u**2 + 4))
            # Scale by planet mass ratio to make it more pronounced for larger planets
            magnification = 1.0 + (magnification - 1.0) * (planet_mass_ratio / 0.01) # Normalize to 0.01 mass ratio for scaling

    return max(1.0, magnification) # 광도는 1.0 미만이 될 수 없음

# --- 데이터 준비 ---
frames_data = []
lightcurve_values = []
times = np.arange(orbital_period)

# 관찰자 위치 계산 (고정)
observer_angle_rad = np.radians(observer_angle_deg)
observer_x = R_OBSERVER_DIST * np.cos(observer_angle_rad)
observer_y = R_OBSERVER_DIST * np.sin(observer_angle_rad)
observer_pos = (observer_x, observer_y)
star_pos = (0, 0) # 중심별은 항상 (0,0)에 고정

for t in times:
    # 행성 위치 계산 (원형 궤도)
    angle = 2 * np.pi * t / orbital_period
    planet_x = R_ORBIT * np.cos(angle)
    planet_y = R_ORBIT * np.sin(angle)

    # 광도 계산
    current_magnification = calculate_magnification(
        (planet_x, planet_y), observer_pos, star_pos, planet_mass_ratio
    )
    lightcurve_values.append(current_magnification)

    # 각 프레임에 대한 데이터 저장
    frames_data.append({
        'data': [
            # Trace 0: 중심별 (고정) - 데이터 변경 없음
            go.Scatter(x=[star_pos[0]], y=[star_pos[1]], mode='markers', marker=dict(size=20, color='gold')),
            # Trace 1: 행성 (움직임)
            go.Scatter(x=[planet_x], y=[planet_y], mode='markers', marker=dict(size=8, color='blue')),
            # Trace 2: 광도 그래프 (업데이트)
            go.Scatter(x=times[:t+1], y=lightcurve_values[:t+1], mode='lines', line=dict(color='green'))
        ],
        'name': f'frame_{t}'
    })

# --- 초기 그래프 생성 ---
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("행성 공전 시뮬레이션", "미세중력렌즈 광도 변화"),
                    specs=[[{'type': 'xy'}, {'type': 'xy'}]])

# 1. 공전 시뮬레이션 서브플롯 (왼쪽)
# Trace 0: 중심별 (고정) - 이 인덱스가 중요합니다.
fig.add_trace(go.Scatter(x=[star_pos[0]], y=[star_pos[1]], mode='markers',
                         marker=dict(size=20, color='gold'),
                         name='중심별'), row=1, col=1)
# Trace 1: 행성 (초기 위치)
fig.add_trace(go.Scatter(x=[R_ORBIT * np.cos(0)], y=[R_ORBIT * np.sin(0)], mode='markers',
                         marker=dict(size=8, color='blue'),
                         name='행성'), row=1, col=1)

# 관찰자 위치와 시선 추가 (고정된 선)
fig.add_trace(go.Scatter(x=[observer_x], y=[observer_y], mode='markers',
                         marker=dict(size=10, color='purple', symbol='star'),
                         name='관찰자'), row=1, col=1) # 관찰자 위치
fig.add_trace(go.Scatter(x=[observer_x, star_pos[0]], y=[observer_y, star_pos[1]],
                         mode='lines', line=dict(color='red', dash='dash'),
                         name='관찰자 시선'), row=1, col=1) # 관찰자 시선

fig.update_xaxes(range=[-R_ORBIT * 1.2, R_ORBIT * 1.2], row=1, col=1)
fig.update_yaxes(range=[-R_ORBIT * 1.2, R_ORBIT * 1.2], scaleanchor="x", scaleratio=1, row=1, col=1)
fig.update_layout(showlegend=True, legend=dict(x=0.01, y=0.99)) # 범례 추가 및 위치 조정

# 2. 광도 변화 서브플롯 (오른쪽)
# Trace 2: 광도 그래프 (초기 데이터)
fig.add_trace(go.Scatter(x=[0], y=[lightcurve_values[0]], mode='lines',
                         line=dict(color='green'),
                         name='광도'), row=1, col=2)

fig.update_xaxes(range=[0, orbital_period], title_text="시간 (프레임)", row=1, col=2)
# 광도 Y축 범위 조정: 초기값부터 최대 예상값까지
fig.update_yaxes(range=[min(0.9, min(lightcurve_values) - 0.05), max(1.5, max(lightcurve_values) + 0.05)],
                 title_text="상대 광도", row=1, col=2)

# --- 애니메이션 설정 ---
# frames 리스트에 프레임 데이터 추가
fig.frames = [go.Frame(data=frame['data'], name=frame['name']) for frame in frames_data]

# 애니메이션 재생/일시정지 버튼 설정
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            x=0.01, # 버튼 위치 조정
            y=1.05,
            buttons=[
                dict(label="▶ Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}]),
                dict(label="⏸ Pause",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
            ]
        )
    ]
)

# 타임라인 슬라이더 설정
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
        currentvalue={"font": {"size": 12}, "prefix": "프레임: ", "visible": True},
        len=0.92,
    )
]
fig.update_layout(sliders=sliders)

# --- Streamlit 앱에 Plotly 그래프 표시 ---
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("시뮬레이션 설명:")
st.markdown("""
- **왼쪽 그래프**: 항성(노란색) 주위를 공전하는 행성(파란색)을 보여줍니다. 보라색 별은 관찰자의 위치이며, 붉은 점선은 관찰자로부터 항성으로 향하는 시선 방향을 나타냅니다.
- **오른쪽 그래프**: 시간에 따른 항성의 상대 광도 변화를 나타냅니다. 행성이 관찰자와 항성 사이를 지나가면서 미세중력렌즈 효과에 의해 항성의 광도가 일시적으로 증가하는 것을 시뮬레이션합니다.
- **광도 계산**: 현재 `calculate_magnification` 함수는 미세중력렌즈의 기본 원리(정렬 시 증폭)를 *매우 단순하게 근사*하여 구현되었습니다. 실제 천체 물리에서는 더 복잡한 공식과 파라미터(예: 아인슈타인 반경, 렌즈 및 광원의 질량, 거리 등)를 사용하여 광도를 계산합니다.
""")
