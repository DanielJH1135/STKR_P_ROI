import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime

# PDF 생성 클래스
class StraumannPDF(FPDF):
    def header(self):
        if os.path.exists("NanumGothic.ttf"):
            self.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)
            self.set_font('NanumGothic', '', 18)
        else:
            self.set_font('Arial', 'B', 16)
        # 헤더 제목 변경: 의사 이모지 + 스트라우만 상담가치분석
        self.cell(0, 15, '👨‍⚕️ 스트라우만 상담가치분석', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('NanumGothic', '', 8) if os.path.exists("NanumGothic.ttf") else self.set_font('Arial', '', 8)
        self.cell(0, 10, '본 견적은 상담용 자료이며, 정확한 비용은 수술 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 사이드바 및 ROI 로직 (기존과 동일) ---
with st.sidebar:
    st.header("🏆 스트라우만 임상 데이터")
    st.info("연세대 조규성 교수팀 10년 연구: 생존율 98.2%")
    st.divider()
    st.subheader("📄 견적서 정보 입력")
    clinic_name = st.text_input("치과명", value="")
    contact_info = st.text_input("연락처", value="")
    patient_name = st.text_input("환자명", value="")
    surgery_date = st.date_input("수술 예정 일자", datetime.now())
    pdf_button = st.button("📥 PDF 견적서 생성 및 출력", use_container_width=True)

# ROI 계산 섹션
total_price = st.number_input("임플란트 정상가 (원)", value=1500000, step=10000)
discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000)
final_price = total_price - discount
years = st.slider("기대 사용 기간 (년)", 5, 30, 20)
daily_cost = final_price / (years * 365)

# --- PDF 생성 로직: 레이아웃 수정 버전 ---
if pdf_button:
    if not patient_name or not clinic_name:
        st.sidebar.error("치과명과 환자명을 입력해주세요.")
    else:
        pdf = StraumannPDF()
        pdf.add_page()
        pdf.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)
        pdf.set_font('NanumGothic', '', 12)
        
        # 기본 정보 출력
        pdf.cell(0, 10, f'치과명: {clinic_name}', 0, 1)
        pdf.cell(0, 10, f'연락처: {contact_info}', 0, 1)
        pdf.cell(0, 10, f'환자명: {patient_name} 귀하', 0, 1)
        pdf.cell(0, 10, f'발행일: {datetime.now().strftime("%Y-%m-%d")} / 수술예정일: {surgery_date}', 0, 1)
        pdf.ln(5)
        
        # 금액 및 ROI 요약
        pdf.set_font('NanumGothic', '', 16)
        pdf.set_text_color(0, 90, 171) # Straumann Blue
        pdf.cell(0, 15, f'최종 상담가: {final_price:,.0f}원', 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        pdf.set_font('NanumGothic', '', 12)
        pdf.multi_cell(0, 10, f'환자분께서 {years}년 동안 사용하실 경우, 하루 평균 비용은 약 {int(daily_cost):,}원입니다. 평생 건강을 위한 가장 합리적인 투자입니다.')
        pdf.ln(10)
        
        # 1. 우수성 이미지 (중앙 배치 및 잘림 방지)
        if os.path.exists("excellence_evidence.jpg"):
            # 현재 Y 위치 확인 후 페이지 하단이면 다음 페이지로
            if pdf.get_y() > 180:
                pdf.add_page()
            
            # 가로 190으로 중앙 배치 (마진 10)
            pdf.image("excellence_evidence.jpg", x=10, w=190)
            pdf.ln(100) # 이미지 높이만큼 아래로 이동 (파일 비율에 맞춰 조정)

        # 2. QR코드 및 각주 (이미지 아래에 배치)
        if os.path.exists("qrcode.png"):
            current_y = pdf.get_y()
            pdf.image("qrcode.png", x=10, y=current_y, w=25) # QR코드 크기 조절
            
            # QR코드 옆 각주 추가 (라이트 그레이 색상)
            pdf.set_xy(37, current_y + 8)
            pdf.set_text_color(180, 180, 180) # Light Gray RGB
            pdf.set_font('NanumGothic', '', 10)
            pdf.cell(0, 10, '스트라우만 공식영상', 0, 1)
            pdf.set_text_color(0, 0, 0) # 색상 복구

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.sidebar.download_button(label="📄 PDF 다운로드 받기", data=pdf_output, file_name=f"Estimate_{patient_name}.pdf", mime="application/pdf")
