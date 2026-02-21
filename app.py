import streamlit as st
import os

st.set_page_config(page_title="Straumann Consultation Tool", layout="wide")

# 사이드바: 팩트 기반 임상 데이터 고정
with st.sidebar:
    st.header("🏆 글로벌 No.1의 증거")
    st.write("---")
    st.subheader("임상 성공률 (10년)")
    st.markdown("""
        | 브랜드 | 성공률 | 근거 |
        | :--- | :--- | :--- |
        | **스트라우만** | **99.7%** | **JDR(Derks) 10년 연구** |
        | 국산 브랜드 | 92~97% | 일반 임상 데이터 |
    """)
    st.write("---")
    st.subheader("🎓 국내 10년 연구 결과")
    st.info("""
    **연세대 치과병원 (조규성 교수팀)**
    - 1,692건의 스트라우만 임상 분석
    - 10년 누적 생존율: **98.2% 이상**
    - 잇몸 뼈 유지력이 국산 대비 압도적
    """)
    st.write("---")
    st.caption("※ 데이터 출처: JDR 임상 논문 및 보도자료")

# 메인 화면
st.title("👨‍⚕️ 프리미엄 임플란트 가치 분석")

tab1, tab2 = st.tabs(["💰 실질 가치 분석 (ROI)", "🌟 스트라우만의 우수성"])

with tab1:
    st.subheader("임플란트 가치 계산기")
    
    col1, col2 = st.columns(2)
    with col1:
        # 입력창 바로 아래에 콤마가 찍힌 큰 숫자를 보여주어 가독성 해결
        total_price = st.number_input("정상 가격 (원)", value=1500000, step=10000, format="%d")
        st.markdown(f"<h3 style='margin-top:-15px;'>입력 금액: {total_price:,.0f}원</h3>", unsafe_allow_html=True)
        
        # 할인 금액 입력 칸 추가
        discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000, format="%d")
        final_price = total_price - discount
        
        st.markdown(f"#### 할인가 적용 최종 금액: <span style='color:red;'>{final_price:,.0f}원</span>", unsafe_allow_html=True)
        
    with col2:
        years = st.slider("예상 사용 기간 (년)", 5, 30, 15)
    
    # ROI 수식: 할인가 기준, 실시간 숫자 연동
    daily_cost = final_price / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:30px; border-radius:15px; border-left: 10px solid #005aab; text-align:center;'>
            <p style='font-size:1.2rem; color:#555;'>환자분의 하루 평균 투자 비용은</p>
            <h2 style='margin:0; color:#005aab; font-size:4rem;'>{int(daily_cost):,}원</h2>
            <p style='font-size:1.1rem; color:#333; margin-top:10px;'>
                <b>하루 {int(daily_cost):,}원으로 {years}년 동안 건강한 미소를 지키세요.</b><br>
                재수술 걱정 없는 선택, 그것이 가장 경제적인 선택입니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("왜 스트라우만인가?")
    
    # 5대 라인업 정보 (원장님 참고용)
    st.write("---")
    product = st.selectbox("상세 제품군 확인", ["BL", "BLT", "BLX", "TL", "TLX"])
    st.write(f"**{product} 라인업**의 임상적 우수성을 환자분께 설명해 드리고 있습니다.")
    
    st.divider()
    
    # 이미지 에러 방지 로직: 파일이 있을 때만 표시
    image_files = {
        "1. 독보적 기술력": "excellence_tech.png",
        "2. 70년 역사와 전통": "excellence_history.png",
        "3. 방대한 임상 데이터": "excellence_evidence.png"
    }
    
    for title, file in image_files.items():
        st.markdown(f"#### {title}")
        if os.path.exists(file):
            st.image(file, use_container_width=True)
        else:
            # 파일이 없을 경우 에러 대신 안내 문구 출력
            st.warning(f"⚠️ '{file}' 파일이 리포지토리에 없습니다. 파일명을 확인해 주세요.")
