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
            self.set_font('NanumGothic', '', 20)
        # PDF 제목
        self.cell(0, 20, self.title_text, 0, 1, 'C') 
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 8)
        self.set_text_color(180, 180, 180)
        self.cell(0, 10, '본 안내서는 상담용 자료이며, 정확한 비용은 수술 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 사이드바: 데이터 및 견적 정보 ---
with st.sidebar:
    st.header("🏆 스트라우만 임상 데이터")
    st.markdown("""
        | 브랜드 | 성공률 | 근거 |
        | :--- | :--- | :--- |
        | **스트라우만** | **99.7%** | **JDR(Derks) 10년 연구** |
        | 국산 브랜드 | 92~97% | 일반 임상 수치 |
    """)
    st.info("**🎓 연세대 조규성 교수팀 10년 연구**\n- 1,692건 추적 결과 98.2% 이상의 생존율 입증")
    
    st.divider()
    st.subheader("📄 안내서 정보 입력")
    clinic_name = st.text_input("치과명", value="")
    contact_info = st.text_input("연락처", value="")
    patient_name = st.text_input("환자명", value="")
    
    col_d, col_t = st.columns(2)
    with col_d:
        surgery_date = st.date_input("수술 일자", datetime.now())
    with col_t:
        surgery_time = st.time_input("수술 시간", value=time(14, 0))
    
    full_surgery_dt = f"{surgery_date.strftime('%Y-%m-%d')} {surgery_time.strftime('%H:%M')}"
    
    st.divider()
    generate_pdf = st.button("📥 PDF 안내서 생성", use_container_width=True)

# --- 메인 화면: ROI 및 우수성 탭 ---
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
        # 젊은 층까지 고려하여 최대 50년 설정
        years = st.slider("예상 사용 기간 (년)", 5, 50, 20)
    
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
    st.subheader("왜 스트라우만인가?")
    # 이미지 3종 세트 출력
    images = ["excellence_tech.png", "excellence_history.png", "excellence_evidence.jpg"]
    for img in images:
        if os.path.exists(img):
            st.image(img, use_container_width=True)
    
    # --- 우수성 탭 하단 유튜브 영상 추가 ---
    st.divider()
    st.subheader("🎥 스트라우만이 알려드리는 임플란트 빠르게 이해하기!")
    st.write("스트라우만의 기술력과 전통으로, '비싼'임플란트가 아닌 '합리적인'임플란트 식립.")
    # 스트라우만 공식 기술 영상 (SLActive)
    st.video("https://www.youtube.com/watch?v=WHcWT5BRTCA")

# --- PDF 생성 로직 ---
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
            
            pdf.cell(0, 8, f'치과명: {clinic_name} / 연락처: {contact_info}', 0, 1)
            pdf.cell(0, 8, f'환자명: {patient_name} 귀하', 0, 1)
            pdf.cell(0, 8, f'발행일: {datetime.now().strftime("%Y-%m-%d")} / 수술 예정일시: {full_surgery_dt}', 0, 1)
            pdf.ln(5)
            
            pdf.set_font('NanumGothic', '', 14)
            pdf.cell(0, 10, f'■ 상담 가격: {final_p:,.0f}원 (할인 적용 전 {total_p:,.0f}원)', 0, 1)
            pdf.set_text_color(0, 90, 171)
            pdf.cell(0, 15, f'하루 평균 투자 비용: {int(daily_roi):,}원 ({years}년 기준)', 1, 1, 'C')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)
            
            pdf.set_font('NanumGothic', '', 10)
            pdf.multi_cell(0, 10, f'환자분께서 {years}년 동안 사용하실 경우, 하루 평균 비용은 약 {int(daily_roi):,}원입니다. 평생 구강 건강을 위한 가장 합리적인 투자입니다.')
            pdf.ln(10)

            if os.path.exists("excellence_evidence.jpg"):
                pdf.image("excellence_evidence.jpg", x=25, w=160)
            
            if os.path.exists("qrcode.png"):
                qr_y = pdf.get_y() + 5
                pdf.image("qrcode.png", x=165, y=240, w=30)
                pdf.set_xy(140, 272)
                pdf.set_font('NanumGothic', '', 9)
                pdf.set_text_color(180, 180, 180)
                pdf.cell(55, 5, '스트라우만 공식영상', 0, 0, 'R')

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



