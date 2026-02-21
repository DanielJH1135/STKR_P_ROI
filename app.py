import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime

# PDF 클래스 정의 (에러 방지용 한글 설정)
class StraumannPDF(FPDF):
    def __init__(self):
        super().__init__()
        # 나눔고딕 폰트 등록 (NanumGothic.ttf 필수)
        if os.path.exists("NanumGothic.ttf"):
            self.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)

    def header(self):
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 20)
        # 요청하신 제목 반영
        self.cell(0, 20, '👨‍⚕️ 스트라우만 가치 계산기', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 8)
        self.set_text_color(180, 180, 180)
        self.cell(0, 10, '본 견적은 상담용이며, 실제 치료 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 사이드바: 임상 데이터 및 견적 정보 ---
with st.sidebar:
    st.header("🏆 스트라우만 임상 데이터")
    st.markdown("""
        | 구분 | 수치 | 근거 |
        | :--- | :--- | :--- |
        | **성공률** | **99.7%** | **JDR(Derks) 10년 연구** |
        | **생존율** | **98.2%** | **연세대 조규성 교수팀** |
    """)
    st.info("**🎓 연세대 조규성 교수팀 10년 연구**\n- 1,692건 추적 결과 98.2% 이상의 생존율 입증")
    
    st.divider()
    st.subheader("📄 견적서 정보 입력")
    # 비운 상태로 제공
    clinic_name = st.text_input("치과명", value="")
    contact_info = st.text_input("연락처", value="")
    patient_name = st.text_input("환자명", value="")
    surgery_date = st.date_input("수술 예정 일자", datetime.now())
    
    st.divider()
    generate_pdf = st.button("📥 PDF 견적서 생성", use_container_width=True)

# --- 메인 화면: ROI 및 우수성 탭 ---
# 제목 이모지 반영
st.title("👨‍⚕️ 스트라우만 가치 계산기")

tab1, tab2 = st.tabs(["💰 장기 가치 분석 (ROI)", "🌟 스트라우만의 우수성"])

with tab1:
    st.subheader("실질 투자 가치 확인")
    c1, c2 = st.columns(2)
    with c1:
        total_p = st.number_input("임플란트 총 비용 (원)", value=1500000, step=10000)
        discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000)
        final_p = total_p - discount
        # 콤마 표시
        st.markdown(f"**최종 상담 금액: {final_p:,.0f}원**")
    with c2:
        years = st.slider("예상 사용 기간 (년)", 5, 30, 20)
    
    # ROI 수식: 실시간 숫자 연동
    daily_roi = final_p / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:40px; border-radius:15px; border-left: 10px solid #005aab; text-align:center;'>
            <p style='font-size:1.2rem; color:#555;'>환자분의 하루 평균 투자 비용은</p>
            <h2 style='margin:0; color:#005aab; font-size:4.5rem;'>{int(daily_roi):,}원</h2>
            <p style='font-size:1.1rem; color:#333; margin-top:10px;'>
                <b>하루 {int(daily_roi):,}원으로 {years}년 동안 건강한 미소를 유지하세요.</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("스트라우만이 신뢰받는 이유")
    images = ["excellence_tech.png", "excellence_history.png", "excellence_evidence.jpg"]
    for img in images:
        if os.path.exists(img):
            st.image(img, use_container_width=True)

# --- PDF 생성 및 오류 방지 로직 ---
if generate_pdf:
    if not patient_name or not clinic_name:
        st.sidebar.warning("치과명과 환자명을 입력해주세요.")
    else:
        try:
            pdf = StraumannPDF()
            pdf.add_page()
            if os.path.exists("NanumGothic.ttf"):
                pdf.set_font('NanumGothic', '', 12)
            
            # 1. 환자 및 치과 정보
            pdf.cell(0, 10, f'치과명: {clinic_name} / 연락처: {contact_info}', 0, 1)
            pdf.cell(0, 10, f'환자명: {patient_name} 귀하', 0, 1)
            pdf.cell(0, 10, f'발행일: {datetime.now().strftime("%Y-%m-%d")} / 수술 예정일: {surgery_date}', 0, 1)
            pdf.ln(10)
            
            # 2. 금액 상세
            pdf.set_font('NanumGothic', '', 14) if os.path.exists("NanumGothic.ttf") else pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, f'■ 정상가: {total_p:,.0f}원', 0, 1)
            pdf.cell(0, 10, f'■ 상담 할인: -{discount:,.0f}원', 0, 1)
            pdf.set_text_color(0, 90, 171) # Straumann Blue
            pdf.cell(0, 15, f'최종 상담가: {final_p:,.0f}원', 1, 1, 'C')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)
            
            # ROI 문구 실시간 연동
            pdf.set_font('NanumGothic', '', 12) if os.path.exists("NanumGothic.ttf") else pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 10, f'환자분께서 {years}년 동안 사용하실 경우, 하루 평균 비용은 약 {int(daily_roi):,}원입니다. 평생 구강 건강을 위한 가장 합리적인 투자입니다.')
            pdf.ln(10)

            # 3. 우수성 이미지 (중앙 배치)
            if os.path.exists("excellence_evidence.jpg"):
                # 중앙 배치 로직: A4(210mm) - 이미지폭(160mm) / 2 = 25mm
                pdf.image("excellence_evidence.jpg", x=25, w=160)
            
            # 4. QR코드 및 각주 (우측 하단)
            if os.path.exists("qrcode.png"):
                pdf.image("qrcode.png", x=165, y=240, w=30)
                pdf.set_xy(150, 272)
                pdf.set_font('NanumGothic', '', 9) if os.path.exists("NanumGothic.ttf") else pdf.set_font('Arial', '', 9)
                pdf.set_text_color(180, 180, 180) # 라이트 그레이
                pdf.cell(45, 5, '스트라우만 공식영상', 0, 0, 'R')

            # PDF 출력 및 인코딩 처리 (오류 방지)
            pdf_bytes = pdf.output(dest='S')
            if not isinstance(pdf_bytes, bytes):
                pdf_bytes = pdf_bytes.encode('latin-1', errors='ignore')
            
            st.sidebar.download_button(
                label="📄 PDF 견적서 다운로드",
                data=pdf_bytes,
                file_name=f"Straumann_Estimate_{patient_name}.pdf",
                mime="application/pdf"
            )
            st.sidebar.success("성공적으로 생성되었습니다!")
        except Exception as e:
            st.error(f"PDF 생성 중 오류가 발생했습니다: {e}")
