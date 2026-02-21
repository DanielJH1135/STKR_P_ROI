import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Straumann Consultation & Estimate", layout="wide")

# PDF 생성 클래스 (나눔고딕 적용)
class StraumannPDF(FPDF):
    def header(self):
        if os.path.exists("NanumGothic.ttf"):
            self.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)
            self.set_font('NanumGothic', '', 18)
        else:
            self.set_font('Arial', 'B', 16)
        self.cell(0, 15, '임플란트 프리미엄 견적서 (스트라우만)', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('NanumGothic', '', 8) if os.path.exists("NanumGothic.ttf") else self.set_font('Arial', '', 8)
        self.cell(0, 10, '본 견적은 상담용 자료이며, 정확한 비용은 수술 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 1. 사이드바: 임상 데이터 및 견적 정보 입력 ---
with st.sidebar:
    st.header("🏆 스트라우만 임상 데이터")
    st.markdown("""
        | 구분 | 수치 | 근거 |
        | :--- | :--- | :--- |
        | **성공률** | **99.7%** | **JDR(Derks) 10년 연구** |
        | **생존율** | **98.2%** | **연세대 조규성 교수팀** |
    """)
    st.info("연세대 치과병원 10년 추적 관찰 결과, 98% 이상의 압도적 생존율 기록")
    
    st.divider()
    
    st.subheader("📄 견적서 정보 입력")
    clinic_name = st.text_input("치과명", value="")
    contact_info = st.text_input("연락처", value="")
    patient_name = st.text_input("환자명", value="")
    surgery_date = st.date_input("수술 예정 일자", datetime.now())
    
    st.divider()
    
    # PDF 출력 버튼을 사이드바 하단에 배치
    pdf_button = st.button("📥 PDF 견적서 생성 및 출력", use_container_width=True)

# --- 2. 메인 화면: ROI 및 우수성 탭 ---
tab1, tab2 = st.tabs(["💰 장기 가치 분석 (ROI)", "🌟 스트라우만의 우수성"])

with tab1:
    st.subheader("실질 투자 가치 계산기")
    col_a, col_b = st.columns(2)
    
    with col_a:
        total_price = st.number_input("임플란트 정상가 (원)", value=1500000, step=10000, format="%d")
        st.markdown(f"**정상가: {total_price:,.0f}원**")
        discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000, format="%d")
        final_price = total_price - discount
        st.markdown(f"### 최종 상담가: <span style='color:red;'>{final_price:,.0f}원</span>", unsafe_allow_html=True)
        
    with col_b:
        years = st.slider("기대 사용 기간 (년)", 5, 30, 20)
    
    daily_cost = final_price / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:30px; border-radius:15px; border-left: 10px solid #005aab; text-align:center;'>
            <p style='font-size:1.2rem; color:#555;'>환자분의 하루 평균 투자 비용은</p>
            <h2 style='margin:0; color:#005aab; font-size:4rem;'>{int(daily_cost):,}원</h2>
            <p style='font-size:1.1rem; color:#333; margin-top:10px;'>
                <b>하루 {int(daily_cost):,}원으로 {years}년 동안 건강한 미소를 지키세요.</b><br>
                재수술 리스크를 최소화하는 가장 경제적인 선택입니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("전 세계가 신뢰하는 스트라우만")
    # 이미지 3종 세트 배치
    if os.path.exists("excellence_tech.png"):
        st.image("excellence_tech.png", caption="독보적인 기술력 (Roxolid & SLActive)", use_container_width=True)
    if os.path.exists("excellence_history.png"):
        st.image("excellence_history.png", caption="70년 스위스 정밀공학의 역사", use_container_width=True)
    if os.path.exists("excellence_evidence.jpg"):
        st.image("excellence_evidence.jpg", caption="방대한 임상 데이터로 검증된 안정성", use_container_width=True)

# --- 3. PDF 생성 로직 ---
if pdf_button:
    if not patient_name or not clinic_name:
        st.sidebar.error("치과명과 환자명을 입력해주세요.")
    else:
        pdf = StraumannPDF()
        pdf.add_page()
        pdf.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)
        pdf.set_font('NanumGothic', '', 12)
        
        # 기본 정보
        pdf.cell(0, 10, f'치과명: {clinic_name}', 0, 1)
        pdf.cell(0, 10, f'연락처: {contact_info}', 0, 1)
        pdf.cell(0, 10, f'환자명: {patient_name} 귀하', 0, 1)
        pdf.cell(0, 10, f'발행일: {datetime.now().strftime("%Y-%m-%d")} / 수술예정일: {surgery_date}', 0, 1)
        pdf.ln(5)
        
        # 금액 정보
        pdf.set_font('NanumGothic', '', 14)
        pdf.cell(0, 10, f'■ 정상가: {total_price:,.0f}원', 0, 1)
        pdf.cell(0, 10, f'■ 할인금액: -{discount:,.0f}원', 0, 1)
        pdf.set_font('NanumGothic', '', 16)
        pdf.set_text_color(0, 90, 171) # 스트라우만 블루
        pdf.cell(0, 15, f'최종 상담가: {final_price:,.0f}원', 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)
        
        # ROI 요약
        pdf.ln(5)
        pdf.set_font('NanumGothic', '', 12)
        pdf.multi_cell(0, 10, f'환자분께서 {years}년 동안 사용하실 경우, 하루 평균 비용은 약 {int(daily_cost):,}원입니다. 이는 평생의 구강 건강을 위한 가장 합리적인 투자입니다.')
        
        # QR코드 (우측 하단 배치)
        if os.path.exists("qrcode.png"):
            pdf.image("qrcode.png", x=160, y=140, w=35) # 위치 조정 가능
            
        # 우수성 이미지 (최하단 배치)
        if os.path.exists("excellence_evidence.jpg"):
            pdf.image("excellence_evidence.jpg", x=10, y=180, w=190)

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.sidebar.download_button(label="📄 클릭하여 PDF 다운로드", data=pdf_output, file_name=f"Estimate_{patient_name}.pdf", mime="application/pdf")
