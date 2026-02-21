import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime, time

# PDF 클래스 정의 (에러 방지용 텍스트 전용)
class StraumannPDF(FPDF):
    def __init__(self, title_text):
        super().__init__()
        self.title_text = title_text
        if os.path.exists("NanumGothic.ttf"):
            self.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)

    def header(self):
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 18)
        self.cell(0, 15, self.title_text, 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 8)
        self.set_text_color(180, 180, 180)
        self.cell(0, 10, '본 안내서는 상담용 자료이며, 정확한 비용은 수술 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 사이드바: 데이터 및 견적 정보 ---
with st.sidebar:
    st.header("🏆 스트라우만 데이터")
    st.markdown("""
        | 브랜드 | 성공률 | 근거 |
        | :--- | :--- | :--- |
        | **스트라우만** | **99.7%** | **JDR 10년 연구** |
        | 국산 브랜드 | 92~97% | 일반 임상 데이터 |
    """)
    st.info("**🎓 연세대 조규성 교수팀 10년 연구**\n- 1,692건 추적 결과 98.2% 이상의 생존율 입증")
    
    st.divider()
    st.subheader("📄 안내서 정보 입력")
    clinic_name = st.text_input("치과명", value="")
    contact_info = st.text_input("연락처", value="")
    patient_name = st.text_input("환자명", value="")
    
    # 수술 예정 일자 및 시간 분리 입력
    col_d, col_t = st.columns(2)
    with col_d:
        surgery_date = st.date_input("수술 일자", datetime.now())
    with col_t:
        surgery_time = st.time_input("수술 시간", value=time(14, 0)) # 기본값 오후 2시
    
    # 일자와 시간을 합친 문자열 생성
    full_surgery_dt = f"{surgery_date.strftime('%Y-%m-%d')} {surgery_time.strftime('%H:%M')}"
    
    st.divider()
    generate_pdf = st.button("📥 PDF 안내서 생성", use_container_width=True)

# --- 메인 화면: ROI 및 우수성 탭 (기존과 동일) ---
st.title("👨‍⚕️ 스트라우만 가치 계산기")

tab1, tab2 = st.tabs(["💰 장기 가치 분석 (ROI)", "🌟 스트라우만의 우수성"])

with tab1:
    st.subheader("실질 투자 가치 확인")
    c1, c2 = st.columns(2)
    with c1:
        total_p = st.number_input("임플란트 총 비용 (원)", value=1500000, step=10000)
        discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000)
        final_p = total_p - discount
        st.markdown(f"**최종 상담 금액: {final_p:,.0f}원**")
    with c2:
        years = st.slider("예상 사용 기간 (년)", 5, 30, 20)
    
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

# --- PDF 생성 로직 (시간 정보 포함) ---
if generate_pdf:
    if not patient_name or not clinic_name:
        st.sidebar.warning("치과명과 환자명을 입력해주세요.")
    else:
        try:
            dynamic_title = f"{clinic_name} 스트라우만 안내서"
            pdf = StraumannPDF(dynamic_title)
            pdf.add_page()
            if os.path.exists("NanumGothic.ttf"):
                pdf.set_font('NanumGothic', '', 12)
            
            # 1. 정보 출력 (시간 포함)
            pdf.cell(0, 8, f'치과명: {clinic_name} / 연락처: {contact_info}', 0, 1)
            pdf.cell(0, 8, f'환자명: {patient_name} 귀하', 0, 1)
            pdf.cell(0, 8, f'발행일: {datetime.now().strftime("%Y-%m-%d")} / 수술 예정일시: {full_surgery_dt}', 0, 1)
            pdf.ln(5)
            
            # 2. 금액 및 ROI 요약
            pdf.set_font('NanumGothic', '', 14)
            pdf.cell(0, 10, f'■ 상담가: {final_p:,.0f}원 (정상가 {total_p:,.0f}원 대비 {discount:,.0f}원 할인)', 0, 1)
            pdf.set_text_color(0, 90, 171)
            pdf.cell(0, 12, f'하루 평균 투자 비용: {int(daily_roi):,}원 ({years}년 기준)', 1, 1, 'C')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)
            
            pdf.set_font('NanumGothic', '', 10)
            pdf.multi_cell(0, 7, f'환자분께서 {years}년 동안 사용하실 경우, 하루 평균 비용은 약 {int(daily_roi):,}원입니다. 평생 구강 건강을 위한 가장 합리적인 투자입니다.')
            pdf.ln(5)

            # 3. 우수성 이미지 (중앙 배치)
            if os.path.exists("excellence_evidence.jpg"):
                pdf.image("excellence_evidence.jpg", x=25, w=160)
            
            # 4. QR코드 및 각주
            if os.path.exists("qrcode.png"):
                qr_y = pdf.get_y() + 5
                pdf.image("qrcode.png", x=140, y=qr_y, w=25)
                pdf.set_xy(166, qr_y + 10)
                pdf.set_font('NanumGothic', '', 8)
                pdf.set_text_color(180, 180, 180)
                pdf.cell(30, 5, '스트라우만 공식영상', 0, 0, 'L')

            pdf_bytes = pdf.output(dest='S')
            if not isinstance(pdf_bytes, bytes):
                pdf_bytes = pdf_bytes.encode('latin-1', errors='ignore')
            
            st.sidebar.download_button(
                label="📄 PDF 안내서 다운로드",
                data=pdf_bytes,
                file_name=f"{clinic_name}_Estimate_{patient_name}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"PDF 생성 중 오류가 발생했습니다: {e}")
