import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Straumann Premium Quote", layout="wide")

# PDF 생성 클래스 정의
class StraumannPDF(FPDF):
    def header(self):
        # 나눔고딕 폰트 등록 (파일이 리포지토리에 있어야 함)
        if os.path.exists("NanumGothic.ttf"):
            self.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)
            self.set_font('NanumGothic', '', 16)
        else:
            self.set_font('Arial', 'B', 16)
        
        self.cell(0, 10, 'PREMIUM IMPLANT ESTIMATE', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        if os.path.exists("NanumGothic.txt"):
            self.set_font('NanumGothic', '', 8)
        self.cell(0, 10, '본 견적은 상담용이며 실제 치료 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 사이드바: 입력 및 데이터 ---
with st.sidebar:
    st.header("🏆 글로벌 No.1 데이터")
    st.info("연세대 조규성 교수팀 10년 연구: 생존율 98.2%") #
    st.divider()
    
    st.subheader("📄 견적서 정보 입력")
    clinic_name = st.text_input("치과명", value="서울스트라우만치과")
    contact_info = st.text_input("연락처", value="02-123-4567")
    patient_name = st.text_input("환자명")
    surgery_date = st.date_input("수술 예정 일자", datetime.now()) #
    
    st.divider()
    # QR코드 이미지 확인
    if os.path.exists("qrcode.png"):
        st.image("qrcode.png", caption="스트라우만 공식 영상 QR", width=150)

# --- 메인 화면: 계산 로직 ---
st.title("👨‍⚕️ 프리미엄 가치 분석 및 견적 생성")

col1, col2 = st.columns(2)
with col1:
    total_price = st.number_input("임플란트 정상가 (원)", value=1500000, step=10000)
    discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000)
    final_price = total_price - discount
    st.subheader(f"최종 상담가: {final_price:,.0f}원")
with col2:
    years = st.slider("기대 사용 기간 (년)", 5, 30, 20)

daily_cost = final_price / (years * 365)
st.markdown(f"### 하루 평균 투자 비용: **{int(daily_cost):,}원**") #

# --- PDF 생성 및 다운로드 버튼 ---
if st.button("📥 PDF 견적서 출력"):
    if not patient_name:
        st.error("환자명을 입력해주세요.")
    else:
        pdf = StraumannPDF()
        pdf.add_page()
        
        # 폰트 설정
        pdf.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)
        pdf.set_font('NanumGothic', '', 12)
        
        # 견적서 내용 작성
        pdf.cell(0, 10, f'치과명: {clinic_name}', 0, 1)
        pdf.cell(0, 10, f'연락처: {contact_info}', 0, 1)
        pdf.cell(0, 10, f'환자명: {patient_name} 귀하', 0, 1)
        pdf.cell(0, 10, f'수술 예정일: {surgery_date}', 0, 1)
        pdf.ln(10)
        
        pdf.set_font('NanumGothic', '', 14)
        pdf.cell(0, 10, f'1. 임플란트 총 비용: {total_price:,.0f}원', 0, 1)
        pdf.cell(0, 10, f'2. 상담 할인 금액: -{discount:,.0f}원', 0, 1)
        pdf.set_font('NanumGothic', '', 16)
        pdf.cell(0, 15, f'최종 합계 금액: {final_price:,.0f}원', 1, 1, 'C')
        pdf.ln(10)
        
        pdf.set_font('NanumGothic', '', 12)
        pdf.multi_cell(0, 10, f'본 임플란트의 {years}년 사용 기준 하루 가치는 약 {int(daily_cost):,}원입니다.\n커피 한 잔보다 저렴한 비용으로 평생의 건강을 지키세요.')
        
        # 하단 우수성 이미지 삽입
        if os.path.exists("excellence_evidence.jpg"):
            pdf.ln(10)
            pdf.image("excellence_evidence.jpg", x=10, w=190)
            
        # QR코드 삽입
        if os.path.exists("qrcode.png"):
            pdf.image("qrcode.png", x=160, y=20, w=30)

        # PDF 저장 및 다운로드
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="Click to Download PDF", data=pdf_output, file_name=f"Estimate_{patient_name}.pdf", mime="application/pdf")

# --- 우수성 탭 ---
st.divider()
st.subheader("🌟 스트라우만 우수성 확인")
if os.path.exists("excellence_evidence.jpg"):
    st.image("excellence_evidence.jpg", use_container_width=True)
