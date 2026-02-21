import streamlit as st
import pandas as pd

st.set_page_config(page_title="Professional Consultation Tool", layout="wide")

# 사이드바: 진짜 임상 데이터로 업데이트
with st.sidebar:
    st.header("🏆 객관적 데이터 비교")
    st.write("---")
    
    st.subheader("임상 성공률 (10년 장기 추적)")
    # 실제 보도자료 및 연구 데이터 반영
    st.markdown("""
        | 브랜드 | 성공률 | 근거 |
        | :--- | :--- | :--- |
        | **스트라우만** | **99.7%** | **JDR(Derks) 연구** |
        | 국산 브랜드 | 95.6% | 국내 학회지(2년) |
    """)
    
    st.write("---")
    st.subheader("🎓 국내 대학 10년 연구")
    # 연세대 조규성 교수팀 연구 결과로 수정
    st.info("""
    **연세대 치과병원 (조규성 교수팀)**
    - 대상: 스트라우만 임플란트 1,692건
    - 기간: 10년 이상 추적 관찰
    - 결과: **98.2%** 누적 생존율 기록
    - 특징: 주변골 소실이 매우 적고 안정적
    """)
    
    st.write("---")
    st.caption("※ 정보는 신뢰할 수 있는 임상 논문 및 공식 보도자료를 기반으로 합니다.")

# 메인 화면
st.title("👨‍⚕️ 프리미엄 임플란트 가치 분석")

tab1, tab2 = st.tabs(["💰 장기 가치 분석 (ROI)", "🔬 맞춤형 솔루션 가이드"])

with tab1:
    st.subheader("실질 투자 가치 계산기")
    
    col1, col2 = st.columns(2)
    with col1:
        # 입력창에서 콤마 체감을 위해 step 설정 및 아래에 포맷팅 표시
        total_price = st.number_input("임플란트 총 비용 (원)", value=1500000, step=10000, format="%d")
        st.markdown(f"**정상가: {total_price:,.0f}원**")
        
        # 할인 금액 입력 칸 추가
        discount = st.number_input("할인 금액 (원)", value=0, step=10000, format="%d")
        final_price = total_price - discount
        
        st.markdown(f"### 최종 상담가: <span style='color:red;'>{final_price:,.0f}원</span>", unsafe_allow_html=True)
        
    with col2:
        years = st.slider("예상 사용 기간 (년)", 5, 30, 20)
    
    # ROI 수식: 할인가 기준, 실시간 숫자 연동
    daily_cost = final_price / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:30px; border-radius:15px; border-left: 10px solid #005aab; text-align:center;'>
            <p style='font-size:1.2rem; color:#555;'>환자분의 하루 평균 투자 비용은</p>
            <h2 style='margin:0; color:#005aab; font-size:4rem;'>{int(daily_cost):,}원</h2>
            <p style='font-size:1.1rem; color:#333; margin-top:10px;'>
                <b>하루 {int(daily_cost):,}원으로 20년의 건강한 미소를 지키세요.</b><br>
                재수술 리스크를 줄이는 가장 경제적인 선택입니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("스트라우만 정밀 라인업")
    
    # 5대 제품군 분리
    product = st.radio("상담 제품 선택", ["BL", "BLT", "BLX", "TL", "TLX"], horizontal=True)
    
    if product in ["TL", "TLX"]:
        st.info(f"### {product}: {product} 레벨의 장기적 안정성")
        # TL/TLX 전용 규격
        sub_type = st.radio("플랫폼", ["S (Narrow)", "SP (Regular)"])
        if sub_type == "S (Narrow)":
            st.success("권장 직경: 2.8mm (S 전용)")
        else:
            st.success("권장 직경: 1.8mm (SP 전용)")
            
    elif product == "BLX":
        st.info("### BLX: 고정력 및 즉시 식립 최적화")
        # BLX 전용 직경 체계
        dia = st.select_slider("직경 선택 (mm)", options=[3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.5])
        st.success(f"BLX {dia}mm: 골질이 약한 경우에도 압도적 고정력 제공")
        
    elif product in ["BL", "BLT"]:
        st.info(f"### {product}: 본 레벨의 정교한 심미성")
        # BL/BLT 전용 직경
        dia = st.selectbox("직경 선택 (mm)", [2.9, 3.3, 4.1, 4.8])
        st.success(f"{product} {dia}mm: 자연치아와 유사한 잇몸 라인 형성")
