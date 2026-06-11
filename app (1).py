import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ─── 페이지 설정 ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="지진 진원 찾기",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── 전역 CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
  }

  /* 전체 배경 */
  .stApp {
    background: #0d1117;
    color: #e6edf3;
  }

  /* 메인 헤더 */
  .hero-header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #58a6ff, #3fb950, transparent);
  }
  .hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #e6edf3;
    margin: 0;
    letter-spacing: -0.5px;
  }
  .hero-subtitle {
    color: #8b949e;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    font-weight: 300;
  }
  .hero-badge {
    display: inline-block;
    background: rgba(88, 166, 255, 0.1);
    border: 1px solid rgba(88, 166, 255, 0.3);
    color: #58a6ff;
    font-size: 0.75rem;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    margin-right: 0.5rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
  }

  /* 단계 표시 */
  .step-indicator {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }
  .step-pill {
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    border: 1px solid #30363d;
    color: #8b949e;
    background: #161b22;
    transition: all 0.2s;
  }
  .step-pill.active {
    background: rgba(88, 166, 255, 0.15);
    border-color: #58a6ff;
    color: #58a6ff;
  }
  .step-pill.done {
    background: rgba(63, 185, 80, 0.1);
    border-color: #3fb950;
    color: #3fb950;
  }

  /* 카드 */
  .card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
  }
  .card-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #58a6ff;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.8rem;
  }

  /* 관측소 정보 테이블 */
  .obs-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }
  .obs-table th {
    background: #21262d;
    padding: 0.6rem 1rem;
    text-align: center;
    color: #8b949e;
    font-weight: 500;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
  }
  .obs-table td {
    padding: 0.7rem 1rem;
    text-align: center;
    border-bottom: 1px solid #21262d;
    color: #e6edf3;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
  }
  .obs-table tr:last-child td { border-bottom: none; }
  .obs-table tr:hover td { background: rgba(88,166,255,0.05); }
  .badge-a { color: #ff7b72; font-weight: 700; }
  .badge-b { color: #79c0ff; font-weight: 700; }
  .badge-c { color: #56d364; font-weight: 700; }

  /* 안내 박스 */
  .info-box {
    background: rgba(88, 166, 255, 0.07);
    border-left: 3px solid #58a6ff;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    color: #c9d1d9;
    line-height: 1.6;
  }
  .warn-box {
    background: rgba(210, 153, 34, 0.08);
    border-left: 3px solid #d29922;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    color: #c9d1d9;
  }
  .success-box {
    background: rgba(63, 185, 80, 0.08);
    border-left: 3px solid #3fb950;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.88rem;
    color: #c9d1d9;
  }

  /* 버튼 스타일 */
  .stButton > button {
    background: #21262d;
    border: 1px solid #30363d;
    color: #e6edf3;
    border-radius: 6px;
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 500;
    transition: all 0.2s;
  }
  .stButton > button:hover {
    background: #30363d;
    border-color: #58a6ff;
    color: #58a6ff;
  }
  .primary-btn > button {
    background: #238636 !important;
    border-color: #2ea043 !important;
    color: white !important;
  }
  .primary-btn > button:hover {
    background: #2ea043 !important;
    border-color: #3fb950 !important;
  }

  /* 입력 필드 */
  .stNumberInput input, .stTextInput input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
  }
  .stNumberInput input:focus, .stTextInput input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 2px rgba(88,166,255,0.15) !important;
  }

  /* 수식 표시 */
  .formula-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #79c0ff;
    margin: 0.6rem 0;
    line-height: 1.8;
  }

  /* 결과 대비 */
  .result-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #21262d;
  }
  .result-label { color: #8b949e; font-size: 0.85rem; }
  .result-value { font-family: 'Space Mono', monospace; color: #e6edf3; font-size: 0.9rem; }
  .result-correct { color: #3fb950; font-weight: 700; }
  .result-close { color: #d29922; font-weight: 700; }
  .result-wrong { color: #ff7b72; font-weight: 700; }

  /* 데이터프레임 숨기기 */
  [data-testid="stDataFrame"] { display: none; }

  /* 섹션 구분선 */
  .section-divider {
    border: none;
    border-top: 1px solid #21262d;
    margin: 1.5rem 0;
  }

  /* 히든 라디오 버튼 번호 없애기 */
  div[data-baseweb="radio"] label {
    color: #c9d1d9 !important;
  }

  /* 탭 */
  .stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-bottom: 1px solid #21262d;
  }
  .stTabs [data-baseweb="tab"] {
    color: #8b949e;
    font-family: 'Noto Sans KR', sans-serif;
  }
  .stTabs [aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom-color: #58a6ff !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── 지진 데이터 (고정) ──────────────────────────────────────────────────────────
EARTHQUAKE_DATA = {
    "event": "2016년 경주 지진 (M 5.8)",
    "actual_epicenter": {"lat": 35.77, "lon": 129.19, "name": "경주 남남서쪽"},
    "stations": [
        {
            "name": "관측소 A",
            "city": "대구",
            "lat": 35.87,
            "lon": 128.60,
            "P_arrival": "14:32:18.2",
            "S_arrival": "14:32:26.8",
            "PS_time": 8.6,
            "epicenter_dist": 54.2,
            "color": "#ff7b72",
            "badge": "badge-a",
        },
        {
            "name": "관측소 B",
            "city": "울산",
            "lat": 35.54,
            "lon": 129.31,
            "P_arrival": "14:32:20.1",
            "S_arrival": "14:32:30.4",
            "PS_time": 10.3,
            "epicenter_dist": 65.0,
            "color": "#79c0ff",
            "badge": "badge-b",
        },
        {
            "name": "관측소 C",
            "city": "포항",
            "lat": 36.03,
            "lon": 129.37,
            "P_arrival": "14:32:19.8",
            "S_arrival": "14:32:29.7",
            "PS_time": 9.9,
            "epicenter_dist": 62.4,
            "color": "#56d364",
            "badge": "badge-c",
        },
    ]
}

# ─── 세션 상태 초기화 ─────────────────────────────────────────────────────────────
defaults = {
    "step": 1,
    "placed_stations": [],
    "dist_a": 0.0, "dist_b": 0.0, "dist_c": 0.0,
    "eq_a": "", "eq_b": "", "eq_c": "",
    "circles_drawn": False,
    "epicenter_lat": 0.0, "epicenter_lon": 0.0,
    "show_result": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.session_state.stations = EARTHQUAKE_DATA["stations"]

# ─── 헬퍼 함수 ──────────────────────────────────────────────────────────────────

def circle_intersection(cx1, cy1, r1, cx2, cy2, r2):
    """두 원의 교점 계산 (위경도 단위)"""
    d = math.sqrt((cx2-cx1)**2 + (cy2-cy1)**2)
    if d > r1+r2 or d < abs(r1-r2) or d == 0:
        return []
    a = (r1**2 - r2**2 + d**2) / (2*d)
    h = math.sqrt(max(0, r1**2 - a**2))
    mx = cx1 + a*(cx2-cx1)/d
    my = cy1 + a*(cy2-cy1)/d
    px = h*(cy2-cy1)/d
    py = h*(cx2-cx1)/d
    return [(mx+px, my-py), (mx-px, my+py)]

def km_to_deg(km):
    """km를 위경도 도(degree)로 변환 (대략 1도 ≈ 111km)"""
    return km / 111.0

def midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def line_through_two_points(p1, p2):
    """두 점을 지나는 직선의 방정식 계수 반환 (ax + by + c = 0)"""
    if abs(p2[0]-p1[0]) < 1e-10:
        return 1, 0, -p1[0]
    slope = (p2[1]-p1[1]) / (p2[0]-p1[0])
    return slope, -1, p1[1] - slope*p1[0]

def line_intersection(a1,b1,c1, a2,b2,c2):
    """두 직선의 교점"""
    det = a1*b2 - a2*b1
    if abs(det) < 1e-10:
        return None
    x = (b1*c2 - b2*c1) / (b2*a1 - b1*a2) if abs(b2*a1 - b1*a2) > 1e-10 else None
    if x is None:
        return None
    if abs(b1) > 1e-10:
        y = (-c1 - a1*x) / b1
    else:
        y = (-c2 - a2*x) / b2
    return (x, y)

# ─── 헤더 ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div>
    <span class="hero-badge">지구과학 × 수학</span>
    <span class="hero-badge">융합 탐구활동</span>
  </div>
  <h1 class="hero-title">🌏 지진 진원지 찾기</h1>
  <p class="hero-subtitle">세 관측소의 지진파 기록을 분석하여 수학적으로 진원의 위치를 추적합니다</p>
</div>
""", unsafe_allow_html=True)

# 단계 표시
step_labels = ["① 상황 파악", "② 위치 표시", "③ 진원거리 입력", "④ 원 그리기", "⑤ 진원 추적", "⑥ 결과 확인"]
pills_html = '<div class="step-indicator">'
for i, label in enumerate(step_labels, 1):
    cls = "active" if st.session_state.step == i else ("done" if st.session_state.step > i else "step-pill")
    if st.session_state.step == i:
        cls = "step-pill active"
    elif st.session_state.step > i:
        cls = "step-pill done"
    else:
        cls = "step-pill"
    pills_html += f'<span class="{cls}">{label}</span>'
pills_html += '</div>'
st.markdown(pills_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# STEP 1 — 상황 설명
# ═══════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="card"><div class="card-title">🚨 긴급 지진 발생 보고</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="info-box">
오늘 오후 2시 32분경, 한반도 남동부에서 규모 5.8의 지진이 발생하였습니다.<br>
세 곳의 지진 관측소에서 지진파가 관측되었으며, 아래 정보를 바탕으로<br>
<strong>수학적 방법을 이용해 진원의 정확한 위치를 추적</strong>해 봅시다.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<table class="obs-table">
  <thead>
    <tr>
      <th>관측소</th><th>도시</th><th>위도 (°N)</th><th>경도 (°E)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="badge-a">관측소 A</span></td>
      <td>대구</td><td>35.87</td><td>128.60</td>
    </tr>
    <tr>
      <td><span class="badge-b">관측소 B</span></td>
      <td>울산</td><td>35.54</td><td>129.31</td>
    </tr>
    <tr>
      <td><span class="badge-c">관측소 C</span></td>
      <td>포항</td><td>36.03</td><td>129.37</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">📐 활동 순서</div>', unsafe_allow_html=True)
        steps_desc = [
            ("①", "세 관측소 위치를 좌표평면에 표시"),
            ("②", "PS시 정보로 진원거리 확인 및 입력"),
            ("③", "각 관측소 중심, 진원거리 반지름의 원 방정식 입력"),
            ("④", "세 원의 교점을 이어 현을 그리기"),
            ("⑤", "세 현의 교점 = 진원 위치 확인"),
            ("⑥", "실제 진원 위치와 비교"),
        ]
        for num, desc in steps_desc:
            st.markdown(f"""
<div style="display:flex;gap:0.8rem;align-items:flex-start;margin-bottom:0.7rem;">
  <span style="color:#58a6ff;font-family:'Space Mono',monospace;font-weight:700;min-width:1.5rem;">{num}</span>
  <span style="color:#c9d1d9;font-size:0.88rem;line-height:1.5;">{desc}</span>
</div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="card">
  <div class="card-title">🔬 과학 개념</div>
  <div style="font-size:0.85rem;color:#c9d1d9;line-height:1.8;">
    <strong style="color:#79c0ff;">PS시</strong> — P파와 S파의 도달 시간 차이<br>
    <strong style="color:#79c0ff;">진원거리</strong> — 관측소에서 진원까지의 거리<br>
    <strong style="color:#79c0ff;">원의 방정식</strong> — (x-a)²+(y-b)²=r²<br>
    <strong style="color:#79c0ff;">현의 수직이등분선</strong>이 원의 중심을 지남
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    if st.button("다음 단계로 → 관측소 위치 표시하기", key="step1_next"):
        st.session_state.step = 2
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# STEP 2 — 관측소 위치 표시
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown('<div class="card"><div class="card-title">📍 관측소 위치 표시하기</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="info-box">
아래 버튼을 눌러 각 관측소의 위치를 좌표평면에 하나씩 표시해 보세요.<br>
오른쪽 그래프에서 위치가 맞는지 확인하세요.
</div>
""", unsafe_allow_html=True)

        stations = st.session_state.stations
        for i, s in enumerate(stations):
            already = any(p["name"] == s["name"] for p in st.session_state.placed_stations)
            badge_class = s["badge"]
            if already:
                st.markdown(f'<div style="padding:0.5rem 0;color:#3fb950;font-size:0.9rem;">✅ <span class="{badge_class}">{s["name"]}</span> ({s["city"]}) — 표시 완료</div>', unsafe_allow_html=True)
            else:
                if st.button(f"📍 {s['name']} ({s['city']}) 위치 찍기  위도 {s['lat']} / 경도 {s['lon']}", key=f"place_{i}"):
                    st.session_state.placed_stations.append(s)
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        if len(st.session_state.placed_stations) == 3:
            st.markdown('<div class="success-box">✅ 세 관측소 위치가 모두 표시되었습니다! 그래프에서 위치를 확인하고 다음 단계로 이동하세요.</div>', unsafe_allow_html=True)
            if st.button("다음 단계로 → 진원거리 입력하기", key="step2_next"):
                st.session_state.step = 3
                st.rerun()

    with col2:
        # 좌표평면 그리기
        fig = go.Figure()

        # 격자 배경
        fig.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            font_color="#8b949e",
            xaxis=dict(
                title="경도 (°E)", range=[127.8, 130.2],
                gridcolor="#21262d", zerolinecolor="#30363d",
                tickformat=".2f", color="#8b949e",
                showline=True, linecolor="#30363d",
            ),
            yaxis=dict(
                title="위도 (°N)", range=[34.8, 37.2],
                gridcolor="#21262d", zerolinecolor="#30363d",
                tickformat=".2f", color="#8b949e",
                showline=True, linecolor="#30363d",
            ),
            height=500,
            margin=dict(l=60, r=30, t=50, b=60),
            title=dict(text="관측소 위치 좌표평면", font=dict(color="#e6edf3", size=14)),
        )

        # 표시된 관측소 점 찍기
        for s in st.session_state.placed_stations:
            fig.add_trace(go.Scatter(
                x=[s["lon"]], y=[s["lat"]],
                mode="markers+text",
                marker=dict(size=14, color=s["color"], symbol="circle",
                            line=dict(color="white", width=2)),
                text=[f"  {s['name']} ({s['city']})"],
                textposition="middle right",
                textfont=dict(color=s["color"], size=12),
                name=s["name"],
                hovertemplate=(
                    f"<b>{s['name']} ({s['city']})</b><br>"
                    f"위도: {s['lat']}°N<br>"
                    f"경도: {s['lon']}°E<br>"
                    f"<b>P파 도착: {s['P_arrival']}</b><br>"
                    f"<b>S파 도착: {s['S_arrival']}</b><br>"
                    f"<b>PS시: {s['PS_time']}초</b><br>"
                    f"<b>진원거리: {s['epicenter_dist']} km</b><br>"
                    "<i>(마우스를 올려 PS시와 진원거리 확인!)</i>"
                    "<extra></extra>"
                )
            ))

        st.plotly_chart(fig, use_container_width=True)

        if len(st.session_state.placed_stations) > 0:
            st.markdown('<div class="info-box">💡 <strong>점 위에 마우스를 올려보세요!</strong> 각 관측소의 P파·S파 도착 시간과 PS시, 진원거리 정보를 확인할 수 있습니다.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# STEP 3 — 진원거리 입력
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown('<div class="card"><div class="card-title">📊 진원거리 입력</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="info-box">
오른쪽 좌표평면에서 각 관측소 점 위에 마우스를 올리면<br>
<strong>PS시와 진원거리</strong> 정보를 볼 수 있습니다.<br>
확인한 값을 아래 표에 입력하세요.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="formula-box">
진원거리 공식<br>
D = PS시 × (Vp × Vs) / (Vp - Vs)<br>
= PS시 × 8.0 × 4.5 / (8.0 - 4.5)<br>
≈ PS시 × <strong>10.28</strong> (단위: km)
</div>
""", unsafe_allow_html=True)

        stations = st.session_state.stations
        colors = ["#ff7b72", "#79c0ff", "#56d364"]
        keys = ["dist_a", "dist_b", "dist_c"]

        for i, (s, key, color) in enumerate(zip(stations, keys, colors)):
            st.markdown(f'<div style="color:{color};font-weight:700;margin-top:0.8rem;font-size:0.9rem;">{s["name"]} ({s["city"]})</div>', unsafe_allow_html=True)
            val = st.number_input(
                f"진원거리 (km)",
                min_value=0.0, max_value=500.0, step=0.1,
                value=st.session_state[key],
                key=f"input_{key}",
                label_visibility="collapsed"
            )
            st.session_state[key] = val

            # 힌트 체크
            actual = s["epicenter_dist"]
            if val > 0:
                diff = abs(val - actual)
                if diff < 2:
                    st.markdown(f'<div style="color:#3fb950;font-size:0.8rem;margin-top:0.2rem;">✓ 잘 입력했어요!</div>', unsafe_allow_html=True)
                elif diff < 10:
                    st.markdown(f'<div style="color:#d29922;font-size:0.8rem;margin-top:0.2rem;">△ 조금 더 정확하게 입력해보세요</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        all_filled = all(st.session_state[k] > 0 for k in keys)
        if all_filled:
            st.markdown('<div class="success-box">✅ 세 관측소의 진원거리를 모두 입력했습니다!</div>', unsafe_allow_html=True)
            if st.button("다음 단계로 → 원의 방정식 입력하기", key="step3_next"):
                st.session_state.step = 4
                st.rerun()

    with col2:
        # 세 관측소 + 호버 정보 그래프
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
            font_color="#8b949e",
            xaxis=dict(title="경도 (°E)", range=[127.8, 130.2],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e"),
            yaxis=dict(title="위도 (°N)", range=[34.8, 37.2],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e"),
            height=500, margin=dict(l=60, r=30, t=50, b=60),
            title=dict(text="관측소 위치 — 마우스를 올려 PS시·진원거리 확인", font=dict(color="#e6edf3", size=13)),
        )

        for s in st.session_state.stations:
            fig.add_trace(go.Scatter(
                x=[s["lon"]], y=[s["lat"]],
                mode="markers+text",
                marker=dict(size=16, color=s["color"], symbol="circle",
                            line=dict(color="white", width=2)),
                text=[f"  {s['name']}"],
                textposition="middle right",
                textfont=dict(color=s["color"], size=12),
                name=s["name"],
                hovertemplate=(
                    f"<b>━━━ {s['name']} ({s['city']}) ━━━</b><br>"
                    f"📍 위도: {s['lat']}°N  경도: {s['lon']}°E<br>"
                    f"⏱ P파 도착: {s['P_arrival']}<br>"
                    f"⏱ S파 도착: {s['S_arrival']}<br>"
                    f"<b>📐 PS시 (S-P): {s['PS_time']} 초</b><br>"
                    f"<b>🔵 진원거리: {s['epicenter_dist']} km</b>"
                    "<extra></extra>"
                )
            ))

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="info-box">💡 각 관측소 점에 마우스를 올려 <strong>PS시와 진원거리</strong>를 확인한 후 왼쪽에 입력하세요.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# STEP 4 — 원의 방정식 입력 및 그리기
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    col1, col2 = st.columns([2, 3])
    stations = st.session_state.stations
    dists = [st.session_state.dist_a, st.session_state.dist_b, st.session_state.dist_c]
    keys_eq = ["eq_a", "eq_b", "eq_c"]
    colors = ["#ff7b72", "#79c0ff", "#56d364"]

    with col1:
        st.markdown('<div class="card"><div class="card-title">⭕ 원의 방정식 입력</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="info-box">
각 관측소를 <strong>원의 중심</strong>으로 하고,<br>
해당 <strong>진원거리를 반지름</strong>으로 하는<br>
원의 방정식을 직접 입력해보세요.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="formula-box">
원의 방정식:<br>
(위도 − 중심위도)² + (경도 − 중심경도)² = r²<br><br>
※ 여기서 r은 진원거리(km)를 위경도로 환산:<br>
r (도) = 진원거리(km) ÷ 111
</div>
""", unsafe_allow_html=True)

        all_eq_valid = True
        for i, (s, dist, key, color) in enumerate(zip(stations, dists, keys_eq, colors)):
            r_deg = km_to_deg(dist)
            st.markdown(f"""
<div style="margin-top:1rem;">
  <span style="color:{color};font-weight:700;">{s['name']} ({s['city']})</span><br>
  <span style="color:#8b949e;font-size:0.8rem;">중심: ({s['lat']}, {s['lon']}), 반지름 ≈ {r_deg:.4f}°</span>
</div>
""", unsafe_allow_html=True)
            example = f"(위도-{s['lat']})²+(경도-{s['lon']})²={r_deg:.4f}²"
            val = st.text_input(
                f"원의 방정식",
                value=st.session_state[key],
                key=f"input_{key}",
                placeholder=f"예: {example}",
                label_visibility="collapsed"
            )
            st.session_state[key] = val
            if val.strip():
                st.markdown(f'<div style="color:#3fb950;font-size:0.78rem;">✓ 입력됨</div>', unsafe_allow_html=True)
            else:
                all_eq_valid = False

        st.markdown("</div>", unsafe_allow_html=True)

        if all_eq_valid:
            if st.button("🔵 원 그리기!", key="draw_circles"):
                st.session_state.circles_drawn = True
                st.rerun()

        if st.session_state.circles_drawn:
            st.markdown('<div class="success-box">✅ 세 원이 그려졌습니다! 오른쪽에서 원의 교점을 확인해보세요.</div>', unsafe_allow_html=True)
            if st.button("다음 단계로 → 진원 위치 확인하기", key="step4_next"):
                st.session_state.step = 5
                st.rerun()

    with col2:
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
            font_color="#8b949e",
            xaxis=dict(title="경도 (°E)", range=[127.8, 130.4],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e",
                       scaleanchor="y", scaleratio=1),
            yaxis=dict(title="위도 (°N)", range=[34.6, 37.2],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e"),
            height=520, margin=dict(l=60, r=30, t=50, b=60),
            title=dict(text="원의 방정식 그래프", font=dict(color="#e6edf3", size=13)),
        )

        # 관측소 점
        for s in stations:
            fig.add_trace(go.Scatter(
                x=[s["lon"]], y=[s["lat"]],
                mode="markers+text",
                marker=dict(size=12, color=s["color"], line=dict(color="white", width=2)),
                text=[f"  {s['name']}"], textposition="middle right",
                textfont=dict(color=s["color"], size=11),
                name=s["name"],
                hovertemplate=f"<b>{s['name']}</b><br>위도:{s['lat']}, 경도:{s['lon']}<extra></extra>"
            ))

        # 원 그리기
        if st.session_state.circles_drawn:
            theta = np.linspace(0, 2*np.pi, 360)
            for s, dist, color in zip(stations, dists, colors):
                r_deg = km_to_deg(dist)
                cx, cy = s["lat"], s["lon"]
                x_circ = cy + r_deg * np.cos(theta)
                y_circ = cx + r_deg * np.sin(theta)
                fig.add_trace(go.Scatter(
                    x=x_circ, y=y_circ,
                    mode="lines",
                    line=dict(color=color, width=2, dash="dot"),
                    name=f"{s['name']} 원",
                    hoverinfo="skip",
                    opacity=0.7,
                ))

            # 교점 계산 및 표시
            all_ips = []
            pairs = [(0,1),(1,2),(0,2)]
            for ia, ib in pairs:
                sa, sb = stations[ia], stations[ib]
                da, db = km_to_deg(dists[ia]), km_to_deg(dists[ib])
                ips = circle_intersection(sa["lat"], sa["lon"], da, sb["lat"], sb["lon"], db)
                for ip in ips:
                    all_ips.append(ip)
                    fig.add_trace(go.Scatter(
                        x=[ip[1]], y=[ip[0]],
                        mode="markers",
                        marker=dict(size=9, color="white", symbol="x",
                                    line=dict(color="#ffff00", width=2)),
                        name="교점",
                        hovertemplate=f"교점<br>위도:{ip[0]:.3f}, 경도:{ip[1]:.3f}<extra></extra>",
                        showlegend=False
                    ))

        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# STEP 5 — 현 그리기 & 진원 추적
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    col1, col2 = st.columns([2, 3])
    stations = st.session_state.stations
    dists = [st.session_state.dist_a, st.session_state.dist_b, st.session_state.dist_c]
    colors = ["#ff7b72", "#79c0ff", "#56d364"]

    # 교점 계산
    all_intersections = {}
    pairs = [(0,1,"AB"),(1,2,"BC"),(0,2,"AC")]
    for ia, ib, label in pairs:
        sa, sb = stations[ia], stations[ib]
        da, db = km_to_deg(dists[ia]), km_to_deg(dists[ib])
        ips = circle_intersection(sa["lat"], sa["lon"], da, sb["lat"], sb["lon"], db)
        all_intersections[label] = ips

    # 현의 교점 (근사) - 세 원의 공통 교점 영역 찾기
    # 두 교점씩 연결 → 현의 교점 = 진원 근사
    chord_midpoints = []
    chord_lines = []
    for label, ips in all_intersections.items():
        if len(ips) == 2:
            chord_midpoints.append(midpoint(ips[0], ips[1]))
            chord_lines.append((ips[0], ips[1]))

    # 현들의 교점 (실제 진원 근사)
    epicenter_approx = None
    if len(chord_lines) >= 2:
        # 첫 두 현의 교점
        p1, p2 = chord_lines[0]
        p3, p4 = chord_lines[1]
        a1, b1, c1 = line_through_two_points(p1, p2)
        a2, b2, c2 = line_through_two_points(p3, p4)
        pt = line_intersection(a1, b1, c1, a2, b2, c2)
        if pt:
            epicenter_approx = pt

    with col1:
        st.markdown('<div class="card"><div class="card-title">📐 현과 진원 위치</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="info-box">
세 쌍의 원이 만나는 두 교점을 이으면 <strong>현(chord)</strong>이 됩니다.<br>
세 현의 교점이 바로 <strong>진원의 위치</strong>입니다!<br><br>
오른쪽 그래프에서 현의 교점을 확인하고,<br>
진원의 위도와 경도를 아래에 입력하세요.
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="formula-box">
수학적 원리:<br>
두 원의 교점을 이은 선분 = 공통현<br>
세 공통현의 교점 = 세 원의 공통 부분<br>
= 세 관측소에서 같은 거리에 있는 지점<br>
= <strong>진원 위치!</strong>
</div>
""", unsafe_allow_html=True)

        if epicenter_approx:
            st.markdown(f"""
<div class="card" style="margin-top:1rem;">
  <div class="card-title">🎯 계산된 진원 좌표</div>
  <div style="font-family:'Space Mono',monospace;font-size:1.1rem;color:#e6edf3;margin:0.5rem 0;">
    위도: <span style="color:#ffa657;">{epicenter_approx[0]:.3f}°N</span><br>
    경도: <span style="color:#ffa657;">{epicenter_approx[1]:.3f}°E</span>
  </div>
  <div style="color:#8b949e;font-size:0.8rem;">그래프의 ⭐ 표시 위치를 확인하세요</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">✍️ 진원 위치 직접 입력</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#c9d1d9;font-size:0.88rem;margin-bottom:0.8rem;">그래프에서 확인한 진원의 위도와 경도를 입력하세요:</div>', unsafe_allow_html=True)

        epi_lat = st.number_input("진원 위도 (°N)", min_value=33.0, max_value=38.5,
                                   value=st.session_state.epicenter_lat,
                                   step=0.01, format="%.3f", key="input_epi_lat")
        epi_lon = st.number_input("진원 경도 (°E)", min_value=125.0, max_value=132.0,
                                   value=st.session_state.epicenter_lon,
                                   step=0.01, format="%.3f", key="input_epi_lon")
        st.session_state.epicenter_lat = epi_lat
        st.session_state.epicenter_lon = epi_lon

        st.markdown("</div>", unsafe_allow_html=True)

        if epi_lat > 33.0 and epi_lon > 125.0:
            if st.button("🔍 실제 결과 확인하기!", key="show_result"):
                st.session_state.show_result = True
                st.session_state.step = 6
                st.rerun()

    with col2:
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
            font_color="#8b949e",
            xaxis=dict(title="경도 (°E)", range=[127.8, 130.4],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e",
                       scaleanchor="y", scaleratio=1),
            yaxis=dict(title="위도 (°N)", range=[34.6, 37.2],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e"),
            height=560, margin=dict(l=60, r=30, t=50, b=60),
            title=dict(text="원의 교점 — 현 그리기 — 진원 확인", font=dict(color="#e6edf3", size=13)),
        )

        # 원 그리기
        theta = np.linspace(0, 2*np.pi, 360)
        for s, dist, color in zip(stations, dists, colors):
            r_deg = km_to_deg(dist)
            cx, cy = s["lat"], s["lon"]
            x_circ = cy + r_deg * np.cos(theta)
            y_circ = cx + r_deg * np.sin(theta)
            fig.add_trace(go.Scatter(
                x=x_circ, y=y_circ, mode="lines",
                line=dict(color=color, width=1.5, dash="dot"),
                name=f"{s['name']} 원", hoverinfo="skip", opacity=0.5,
            ))

        # 관측소 점
        for s, color in zip(stations, colors):
            fig.add_trace(go.Scatter(
                x=[s["lon"]], y=[s["lat"]], mode="markers+text",
                marker=dict(size=11, color=color, line=dict(color="white", width=2)),
                text=[f"  {s['name']}"], textposition="middle right",
                textfont=dict(color=color, size=11),
                name=s["name"],
                hovertemplate=f"<b>{s['name']}</b><br>위도:{s['lat']}, 경도:{s['lon']}<extra></extra>"
            ))

        # 교점 및 현 그리기
        chord_colors_pair = ["#f0e68c", "#dda0dd", "#87ceeb"]
        for idx, (label, ips) in enumerate(all_intersections.items()):
            cc = chord_colors_pair[idx % len(chord_colors_pair)]
            if len(ips) == 2:
                # 현 (두 교점 연결)
                fig.add_trace(go.Scatter(
                    x=[ips[0][1], ips[1][1]], y=[ips[0][0], ips[1][0]],
                    mode="lines",
                    line=dict(color=cc, width=2.5),
                    name=f"현 ({label})",
                    hoverinfo="skip",
                ))
                # 교점
                for ip in ips:
                    fig.add_trace(go.Scatter(
                        x=[ip[1]], y=[ip[0]], mode="markers",
                        marker=dict(size=8, color="white", symbol="x",
                                    line=dict(color=cc, width=2)),
                        hovertemplate=f"교점<br>위도:{ip[0]:.3f}, 경도:{ip[1]:.3f}<extra></extra>",
                        showlegend=False,
                    ))

        # 진원 (계산된)
        if epicenter_approx:
            fig.add_trace(go.Scatter(
                x=[epicenter_approx[1]], y=[epicenter_approx[0]],
                mode="markers+text",
                marker=dict(size=20, color="#ffa657", symbol="star",
                            line=dict(color="white", width=2)),
                text=["  ⭐ 진원 위치"],
                textposition="middle right",
                textfont=dict(color="#ffa657", size=13, family="Noto Sans KR"),
                name="진원 (계산)",
                hovertemplate=f"<b>⭐ 진원 위치 (계산)</b><br>위도: {epicenter_approx[0]:.3f}°N<br>경도: {epicenter_approx[1]:.3f}°E<extra></extra>"
            ))

        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# STEP 6 — 결과 확인
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    actual = EARTHQUAKE_DATA["actual_epicenter"]
    student_lat = st.session_state.epicenter_lat
    student_lon = st.session_state.epicenter_lon
    stations = st.session_state.stations
    dists = [st.session_state.dist_a, st.session_state.dist_b, st.session_state.dist_c]
    colors = ["#ff7b72", "#79c0ff", "#56d364"]

    # 오차 계산
    error_km = math.sqrt(((student_lat - actual["lat"])*111)**2 + ((student_lon - actual["lon"])*111)**2)

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown('<div class="card"><div class="card-title">🏆 결과 확인</div>', unsafe_allow_html=True)

        if error_km < 10:
            grade = "🎉 정확합니다!"
            grade_class = "result-correct"
            comment = "매우 훌륭해요! 수학적 방법으로 진원 위치를 정확하게 찾았습니다."
        elif error_km < 30:
            grade = "👍 근접합니다!"
            grade_class = "result-close"
            comment = "잘 했어요! 실제 진원에 가까이 추적했습니다."
        else:
            grade = "📚 다시 도전!"
            grade_class = "result-wrong"
            comment = "조금 더 정확하게 계산해봐요. 원의 방정식을 다시 확인해보세요."

        st.markdown(f"""
<div style="text-align:center;margin:1rem 0 1.5rem;">
  <div style="font-size:2rem;margin-bottom:0.5rem;" class="{grade_class}">{grade}</div>
  <div style="color:#8b949e;font-size:0.88rem;">{comment}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""<div class="result-row"><span class="result-label">학생 추정 위도</span>
""", unsafe_allow_html=True)
        st.markdown(f"""
<div class="result-row">
  <span class="result-label">학생 추정 위도</span>
  <span class="result-value">{student_lat:.3f}°N</span>
</div>
<div class="result-row">
  <span class="result-label">학생 추정 경도</span>
  <span class="result-value">{student_lon:.3f}°E</span>
</div>
<div class="result-row">
  <span class="result-label">실제 진원 위도</span>
  <span class="result-value result-correct">{actual['lat']}°N</span>
</div>
<div class="result-row">
  <span class="result-label">실제 진원 경도</span>
  <span class="result-value result-correct">{actual['lon']}°E</span>
</div>
<div class="result-row">
  <span class="result-label">오차 거리</span>
  <span class="result-value {'result-correct' if error_km<10 else 'result-close' if error_km<30 else 'result-wrong'}">{error_km:.1f} km</span>
</div>
<div class="result-row">
  <span class="result-label">실제 진원 지명</span>
  <span class="result-value">{actual['name']}</span>
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">💡 정리</div>', unsafe_allow_html=True)
        st.markdown("""
<div style="font-size:0.87rem;color:#c9d1d9;line-height:1.9;">
  ① 세 관측소에서의 <strong style="color:#79c0ff;">진원거리</strong>를 반지름으로 하는<br>
  &nbsp;&nbsp;&nbsp;원을 그리면 세 원은 한 점에서 만납니다.<br><br>
  ② 두 원의 교점을 이은 선분이 <strong style="color:#79c0ff;">공통현</strong>이며,<br>
  &nbsp;&nbsp;&nbsp;공통현은 두 원의 중심을 잇는 선분과 수직입니다.<br><br>
  ③ 세 공통현의 교점이 <strong style="color:#ffa657;">진원의 위치</strong>가 됩니다.
</div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔄 처음부터 다시하기", key="restart"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()

    with col2:
        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
            font_color="#8b949e",
            xaxis=dict(title="경도 (°E)", range=[127.8, 130.4],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e",
                       scaleanchor="y", scaleratio=1),
            yaxis=dict(title="위도 (°N)", range=[34.6, 37.2],
                       gridcolor="#21262d", zerolinecolor="#30363d",
                       tickformat=".2f", color="#8b949e"),
            height=560, margin=dict(l=60, r=30, t=50, b=60),
            title=dict(text="학생 추정 vs 실제 진원 위치 비교", font=dict(color="#e6edf3", size=13)),
        )

        # 원 그리기
        theta = np.linspace(0, 2*np.pi, 360)
        for s, dist, color in zip(stations, dists, colors):
            r_deg = km_to_deg(dist)
            cx, cy = s["lat"], s["lon"]
            x_circ = cy + r_deg * np.cos(theta)
            y_circ = cx + r_deg * np.sin(theta)
            fig.add_trace(go.Scatter(
                x=x_circ, y=y_circ, mode="lines",
                line=dict(color=color, width=1.5, dash="dot"),
                name=f"{s['name']} 원", hoverinfo="skip", opacity=0.4,
            ))

        # 현
        pairs_label = [(0,1,"AB"),(1,2,"BC"),(0,2,"AC")]
        chord_colors_pair = ["#f0e68c", "#dda0dd", "#87ceeb"]
        for idx, (ia, ib, label) in enumerate(pairs_label):
            sa, sb = stations[ia], stations[ib]
            da, db = km_to_deg(dists[ia]), km_to_deg(dists[ib])
            ips = circle_intersection(sa["lat"], sa["lon"], da, sb["lat"], sb["lon"], db)
            if len(ips) == 2:
                cc = chord_colors_pair[idx]
                fig.add_trace(go.Scatter(
                    x=[ips[0][1], ips[1][1]], y=[ips[0][0], ips[1][0]],
                    mode="lines", line=dict(color=cc, width=2),
                    name=f"현 ({label})", opacity=0.6, hoverinfo="skip",
                ))

        # 관측소 점
        for s, color in zip(stations, colors):
            fig.add_trace(go.Scatter(
                x=[s["lon"]], y=[s["lat"]], mode="markers+text",
                marker=dict(size=11, color=color, line=dict(color="white", width=2)),
                text=[f"  {s['name']}"], textposition="middle right",
                textfont=dict(color=color, size=11), name=s["name"],
                hovertemplate=f"<b>{s['name']}</b><br>위도:{s['lat']}, 경도:{s['lon']}<extra></extra>"
            ))

        # 학생 추정 진원
        fig.add_trace(go.Scatter(
            x=[student_lon], y=[student_lat],
            mode="markers+text",
            marker=dict(size=18, color="#ffa657", symbol="star",
                        line=dict(color="white", width=2)),
            text=["  학생 추정 진원"], textposition="middle right",
            textfont=dict(color="#ffa657", size=12),
            name="학생 추정 진원",
            hovertemplate=f"<b>학생 추정 진원</b><br>위도:{student_lat:.3f}°N<br>경도:{student_lon:.3f}°E<extra></extra>"
        ))

        # 실제 진원
        fig.add_trace(go.Scatter(
            x=[actual["lon"]], y=[actual["lat"]],
            mode="markers+text",
            marker=dict(size=22, color="#3fb950", symbol="star",
                        line=dict(color="white", width=3)),
            text=["  ✅ 실제 진원"], textposition="middle right",
            textfont=dict(color="#3fb950", size=13, family="Noto Sans KR"),
            name="실제 진원",
            hovertemplate=f"<b>✅ 실제 진원 위치</b><br>{actual['name']}<br>위도:{actual['lat']}°N<br>경도:{actual['lon']}°E<extra></extra>"
        ))

        # 학생↔실제 연결선
        fig.add_trace(go.Scatter(
            x=[student_lon, actual["lon"]], y=[student_lat, actual["lat"]],
            mode="lines",
            line=dict(color="#8b949e", width=1.5, dash="dash"),
            name=f"오차 ({error_km:.1f}km)", hoverinfo="skip",
        ))

        st.plotly_chart(fig, use_container_width=True)
