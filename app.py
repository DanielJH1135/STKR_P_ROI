import streamlit as st
import pandas as pd

st.set_page_config(page_title="Professional Consultation Dashboard", layout="wide")

# 사이드바 주문서 UI (사용성 개선)
with st.sidebar:
    st.title("🛒 주문 관리")
    st.write("---")
    st.write("**담은 품목 리스트**")
    # 예시 품목 (실제 연동 가능)
    st.info("선택된 품목이 없습니다.")
    st.write("---")
    st.button("쇼핑카트 담기", use_container_width=True)
    st.button("본사 주문 전송", type="primary", use_container_width=True)

st.title("👨‍⚕️ 스트라우만 스마트 상담 대시보드")
st.write("원장님의 상담 성공률(Closing Rate)을 높이는 데이터 솔루션")

tab1, tab2 = st.tabs(["💰 ROI 가치 분석", "🔍 맞춤형 제품 가이드"])

with tab1:
    st.subheader("임플란트 장기 가치 계산기")
    st.write("환자에게 '가격'이 아닌 '하루 가치'를 보여주세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("스트라우만 총 비용 (원)", value=1500000, step=100000)
    with col2:
        years = st.slider("기대 사용 기간 (년)", 5, 30, 20)
    
    # ROI 수식
    daily = price / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center;'>
            <h3>환자분, 이 임플란트의 하루 가치는 <span style='color:#005aab; font-size:40px;'>{int(daily):,}원</span>입니다.</h3>
            <p>오늘의 5,000원 아끼기보다, 20년의 편안함을 하루 200원에 구매하세요.</p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("치과별 맞춤형 라인업")
    
    line = st.selectbox("원장님 사용 라인업", ["BL/BLT", "BLX", "TL/TLX"])
    
    if line == "TL/TLX":
        # S는 2.8mm만, SP는 1.8mm만 송출
        tab_type = st.radio("플랫폼", ["S", "SP"])
        if tab_type == "S":
            st.success("권장 직경: 2.8mm 전용 제품군")
        else:
            st.success("권장 직경: 1.8mm 전용 제품군")
            
    elif line == "BLX":
        # BLX는 3.5~6.5mm 체계
        dia = st.select_slider("직경 선택 (mm)", options=[3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.5])
        st.info(f"BLX {dia}mm: 고정력 극대화 모델")
        
    elif line == "BL/BLT":
        # BL/BLT는 2.9/3.3/4.1/4.8 체계
        dia = st.selectbox("직경 선택 (mm)", [2.9, 3.3, 4.1, 4.8])
        st.info(f"BL/BLT {dia}mm: 검증된 스탠다드 모델")