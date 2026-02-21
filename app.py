import streamlit as st

st.set_page_config(page_title="Straumann Excellence Dashboard", layout="wide")

# 사이드바: 업데이트된 임상 데이터 상주
with st.sidebar:
    st.header("🏆 객관적 데이터 비교")
    st.write("---")
    
    st.subheader("임상 성공률 (10년 추적)")
    # 공식 보도자료 및 JDR 연구 기반 데이터 반영
    st.markdown("""
        | 브랜드 | 성공률 | 근거 |
        | :--- | :--- | :--- |
        | **스트라우만** | **99.7%** | **JDR(Derks) 10년 연구** |
        | 국산 브랜드 | 92~97% | 일반적 임상 수치 |
    """)
    
    st.write("---")
    st.subheader("🎓 국내 대학 10년 연구")
    # 연세대 조규성 교수팀 연구 결과 반영
    st.info("""
    **연세대 치과병원 (조규성 교수팀)**
    - 대상: 스트라우만 임플란트 1,692건
    - 기간: 10년 이상 추적 관찰
    - 결과: **98.2%** 이상의 누적 생존율 입증
    - 특징: 장기적인 주변골 안정성 탁월
    """)
    
    st.write("---")
    st.caption("※ 본 데이터는 공식 보도자료 및 논문을 기반으로 합니다.")

# 메인 화면
st.title("👨‍⚕️ 스트라우만 프리미엄 상담 솔루션")

tab1, tab2 = st.tabs(["💰 실질 가치 분석 (ROI)", "🌟 스트라우만의 우수성"])

with tab1:
    st.subheader("임플란트 가치 계산기")
    st.write("환자분, 할인 혜택을 반영한 하루 평균 투자 비용을 확인해 보세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        # 정상가 입력
        total_price = st.number_input("임플란트 정상가 (원)", value=1500000, step=10000, format="%d")
        st.markdown(f"**정상가: {total_price:,.0f}원**")
        
        # 할인 금액 입력 칸 추가
        discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000, format="%d")
        
        # 할인가 계산
        final_price = total_price - discount
        st.markdown(f"### 최종 상담가: <span style='color:red;'>{final_price:,.0f}원</span>", unsafe_allow_html=True)
        
    with col2:
        years = st.slider("예상 사용 기간 (년)", 5, 30, 20)
    
    # ROI 수식: 할인가 기준 및 실시간 숫자 연동
    daily_cost = final_price / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:30px; border-radius:15px; border-left: 10px solid #005aab; text-align:center;'>
            <p style='font-size:1.2rem; color:#555;'>환자분의 하루 평균 투자 비용은</p>
            <h2 style='margin:0; color:#005aab; font-size:4rem;'>{int(daily_cost):,}원</h2>
            <p style='font-size:1.1rem; color:#333; margin-top:10px;'>
                <b>하루 {int(daily_cost):,}원으로 {years}년 동안 건강한 미소를 지키세요.</b><br>
                재수술 걱정 없는 선택, 가장 경제적인 투자입니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("왜 전 세계 전문가들은 스트라우만을 선택하는가?")
    st.write("원장님, 아래 이미지들은 깃허브에 동일한 파일명으로 업로드하시면 자동으로 송출됩니다.")
    
    # 깃허브 이미지 링크 구성 가이드 (사용자 깃허브 주소로 변경 필요)
    # 이미지 1: 기술력
    st.markdown("#### 1. 독보적인 기술력 (Roxolid & SLActive)")
    st.image("excellence_tech.png", caption="강도가 더 높고 치유가 빠른 스트라우만만의 특허 기술", use_container_width=True)
    
    st.divider()
    
    # 이미지 2: 역사와 전통
    st.markdown("#### 2. 70년의 역사와 전통")
    st.image("excellence_history.png", caption="1954년부터 시작된 스위스 정밀공학의 정수", use_container_width=True)
    
    st.divider()
    
    # 이미지 3: 임상 데이터
    st.markdown("#### 3. 방대한 임상 데이터")
    st.image("excellence_evidence.png", caption="전 세계에서 가장 많은 임상 논문으로 검증된 안정성", use_container_width=True)

    st.divider()
    st.caption("※ 위 시각 자료는 상담 시 환자분의 이해를 돕기 위한 보조 도구입니다.")
