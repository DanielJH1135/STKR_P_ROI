import streamlit as st

st.set_page_config(page_title="Professional Consultation Tool", layout="wide")

# 사이드바: 국산 vs 스트라우만 성공률 비교 (상주형)
with st.sidebar:
    st.header("🏆 왜 스트라우만인가?")
    st.write("---")
    
    # 성공률 비교 표
    st.subheader("임상 성공률 비교")
    st.markdown("""
        | 브랜드 | 성공률 | 비고 |
        | :--- | :--- | :--- |
        | **스트라우만** | **99.7%** | **본사 공식 보도자료** |
        | 국산 브랜드 | 92~97% | 일반적 임상 수치 |
    """)
    
    st.write("---")
    st.subheader("🎓 국내 대학 연구 결과")
    st.info("연세대 조규성 교수팀 임상 결과: **98.x%** 의 압도적 성공률 입증") #
    
    st.write("---")
    st.caption("※ 70년 전통 스위스 정밀공학의 차이가 결과의 차이를 만듭니다.")

# 메인 화면
st.title("👨‍⚕️ 프리미엄 임플란트 상담 솔루션")

tab1, tab2 = st.tabs(["💰 장기 가치 분석 (ROI)", "🔬 원장님 추천 솔루션"])

with tab1:
    st.subheader("임플란트 가치 계산기")
    st.write("환자분, 평생을 사용하는 임플란트의 '진짜 가격'을 확인해 보세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        # 콤마 표시를 위해 value를 정수로 받고, 아래에서 포맷팅하여 표시
        raw_price = st.number_input("임플란트 총 비용 (원)", value=1500000, step=10000)
        st.markdown(f"**입력된 금액: {raw_price:,.0f}원**") # 세자리 콤마 적용 표시
    with col2:
        years = st.slider("기대 사용 기간 (년)", 5, 30, 20)
    
    # ROI 수식
    daily_cost = raw_price / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:30px; border-radius:15px; border-left: 10px solid #005aab; text-align:center;'>
            <p style='font-size:1.2rem; color:#555;'>환자분의 하루 평균 투자 비용은</p>
            <h2 style='margin:0; color:#005aab; font-size:3rem;'>{int(daily_cost):,}원</h2>
            <p style='font-size:1.1rem; color:#333; margin-top:10px;'>
                <b>하루 200원으로 20년의 건강한 미소를 지키세요.</b><br>
                재수술 걱정 없는 선택, 그것이 가장 경제적인 선택입니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("이 치과만의 전문 솔루션")
    st.write("본 치과는 환자분의 잇몸 상태에 최적화된 스트라우만 전용 라인업을 사용합니다.")
    
    # 원장님이 주력으로 쓰는 라인업 하나를 선택하면 그 장점만 노출
    doctor_choice = st.radio("원장님 주력 제품군 선택", ["BLX (고정력 특화)", "TL/TLX (안정성 특화)"], horizontal=True)
    
    if doctor_choice == "BLX (고정력 특화)":
        st.info("### BLX: 뼈가 약해도 안심하세요")
        st.write("""
        - **넓은 직경 체계 (3.5mm~6.5mm):** 환자분의 골질에 딱 맞는 정밀한 선택이 가능합니다.
        - **즉시 식립 최적화:** 수술 횟수를 줄여 환자분의 불편함을 최소화합니다.
        """)
    else:
        st.info("### TL/TLX: 70년 검증된 정밀함")
        st.write("""
        - **플랫폼 최적화:** S 탭(2.8mm)과 SP 탭(1.8mm)의 정밀한 구분으로 잇몸 형태를 완벽하게 보존합니다.
        - **감염 방지:** 연조직 보호 기능이 뛰어나 장기적인 유지 관리에 유리합니다.
        """)
    
    st.divider()
    st.caption("※ 모든 상담 데이터는 환자분의 이해를 돕기 위한 참고 자료이며, 정확한 진단은 원장님과의 상담을 통해 확정됩니다.")
