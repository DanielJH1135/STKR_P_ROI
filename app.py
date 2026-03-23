import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime, time

# CSS 주입: 슬라이더 색상 고도화 및 액티브 툴팁 애니메이션
st.markdown("""
<style>
    /* --- 슬라이더 커스텀 (빨간색 완전 박멸) --- */
    
    /* 1. 채워지는 바 (왼쪽, 활성화된 부분) - 선택자 구조 강화 */
    .stSlider div[data-baseweb="slider"] > div > div > div:first-child {
        background-color: #2D7662 !important;
    }
    
    /* 혹시 모를 인라인 스타일 빨간색 덮어쓰기 */
    .stSlider div[data-baseweb="slider"] div[style*="rgb(255, 75, 75)"] {
        background-color: #2D7662 !important;
    }
    
    /* 2. 비워진 바 (오른쪽, 비활성화된 부분) */
    .stSlider div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        background-color: #e2e6e6 !important;
    }
    
    /* 3. 슬라이더 동그란 썸(Thumb) */
    .stSlider div[data-baseweb="slider"] div[role="slider"] {
        background-color: #2D7662 !important;
        border-color: #2D7662 !important;
    }
    
    /* 4. 마우스 오버 시 링(그림자) */
    .stSlider div[data-baseweb="slider"] div[role="slider"]:hover,
    .stSlider div[data-baseweb="slider"] div[role="slider"]:focus,
    .stSlider div[data-baseweb="slider"] div[role="slider"]:focus-visible {
        box-shadow: 0 0 0 0.2rem rgba(45, 118, 98, 0.25) !important;
        outline: none !important;
    }

    /* 5. 슬라이더 상단 숫자(말풍선) */
    .stSlider div[data-baseweb="slider"] div[role="slider"] > div {
        color: #2D7662 !important; 
    }
    
    /* 6. 슬라이더 라벨 글씨 색상 고정 */
    .stSlider label p {
        color: #333333 !important;
    }

    /* --- 액티브 툴팁(마우스 오버) 커스텀 --- */
    .active-tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
        color: #005aab; /* 강조할 파란색 */
        font-weight: bold;
        border-bottom: 2px dashed #005aab;
    }
    .active-tooltip .tooltip-content {
        visibility: hidden;
        width: 300px;
        background-color: #36393A; /* 스트라우만 그레이 */
        color: #fff;
        text-align: center;
        border-radius: 8px;
        padding: 12px;
        position: absolute;
        z-index: 999;
        bottom: 150%; 
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        font-size: 0.85rem;
        box-shadow: 0px 10px 15px rgba(0,0,0,0.2);
        line-height: 1.4;
    }
    .active-tooltip .tooltip-content::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: #36393A transparent transparent transparent;
    }
    .active-tooltip:hover .tooltip-content {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
</style>
""", unsafe_allow_html=True)

# PDF 클래스 정의
class StraumannPDF(FPDF):
    def __init__(self, title_text):
        super().__init__()
        self.title_text = title_text
        self.set_auto_page_break(auto=True, margin=20)
        if os.path.exists("NanumGothic.ttf"):
            self.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)

    def header(self):
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 20)
        self.cell(0, 15, self.title_text, 0, 1, 'C') 
        self.ln(3)

    def footer(self):
        self.set_y(-20)
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 8)
        self.set_text_color(180, 180, 180)
        self.cell(0, 5, '※ 임플란트는 관리 여하에 따라 사용기간은 상이합니다.', 0, 1, 'C')
        self.cell(0, 5, '본 안내서는 상담용 자료이며, 정확한 비용은 수술 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 사이드바: 데이터 및 견적 정보 ---
with st.sidebar:
    st.header("🏆 스트라우만 임상 데이터")
    
    st.markdown("""
        | 브랜드 | 장기생존률 | 근거 |
        | :--- | :--- | :--- |
        | **스트라우만** | **99.7%** | **<span class="active-tooltip">10년이상의 임상데이터 연구논문<span class="tooltip-content">van Velzen FJ, et al. J Clin Periodontal. 2015; 374 implants, 177 patients, 10-year follow-up</span></span>** |
        | 국산 브랜드 | 92~97% | 일반 임상 수치 |
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color: #36393A; color: white; padding: 15px; border-radius: 8px; margin-top: 10px;">
            <b>🎓 연세대 조규성 교수팀 10년 연구</b><br>
            <span style="font-size: 0.9em;">- 1,692건 추적 결과 98.2% 이상의 장기생존율 입증</span>
        </div>
    """, unsafe_allow_html=True)
    
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

tab1, tab2 = st.tabs(["💰 장기 가치 분석 (ROI)", "🌟 오래쓰는 스트라우만"])

with tab1:
    st.subheader("실질 투자 가치 확인")
    c1, c2 = st.columns(2)
    with c1:
        total_p = st.number_input("임플란트 총 비용 (원)", value=1500000, step=10000)
        discount = st.number_input("상담 할인 금액 (원)", value=0, step=10000)
        final_p = total_p - discount
        st.markdown(f"**최종 상담 금액: {final_p:,.0f}원**")
    with c2:
        years = st.slider("예상 사용 기간 (년)", 5, 50, 20)
        
        st.markdown("""
            <div style="color: #A9A9A9; font-size: 0.85rem; margin-top: -10px; line-height: 1.4;">
                * 의사 판단하에 측정된 수치입니다.<br>
                * 환자분의 건강상태 / 관리 여하에 따라 상이할 수 있습니다.
            </div>
        """, unsafe_allow_html=True)
    
    daily_roi = final_p / (years * 365)
    
    st.markdown(f"""
        <div style='background-color:#f8f9fa; padding:40px; border-radius:15px; border-left: 10px solid #46B98C; text-align:center; margin-top: 20px;'>
            <p style='font-size:1.2rem; color:#555;'>환자분의 하루 평균 투자 비용은</p>
            <h2 style='margin:0; color:#46B98C; font-size:4.5rem;'>{int(daily_roi):,}원</h2>
            <p style='font-size:1.1rem; color:#333; margin-top:10px;'>
                <b>하루 {int(daily_roi):,}원으로 {years}년 동안 건강한 미소를 유지하세요.</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("신뢰의 브랜드, 스트라우만. 그 이유는?")
    images = ["excellence_tech.png", "excellence_history.png", "excellence_evidence.jpg"]
    for img in images:
        if os.path.exists(img):
            st.image(img, use_container_width=True)
    
    st.divider()
    st.subheader("🎥 스트라우만이 알려드리는 임플란트 빠르게 이해하기!")
    st.write("스트라우만의 기술력과 전통으로, 건강하게 오래쓰는 임플란트. 진짜 나를 위한 선택.")
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
            
            pdf.cell(0, 6, f'치과명: {clinic_name} / 연락처: {contact_info}', 0, 1)
            pdf.cell(0, 6, f'환자명: {patient_name} 귀하', 0, 1)
            pdf.cell(0, 6, f'발행일: {datetime.now().strftime("%Y-%m-%d")} / 수술 예정일시: {full_surgery_dt}', 0, 1)
            pdf.ln(3)
            
            pdf.set_font('NanumGothic', '', 14)
            pdf.cell(0, 8, f'■ 상담 가격: {final_p:,.0f}원 (할인 적용 전 {total_p:,.0f}원)', 0, 1)
            pdf.set_text_color(0, 90, 171)
            pdf.cell(0, 12, f'하루 평균 투자 비용: {int(daily_roi):,}원 ({years}년 기준)', 1, 1, 'C')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
            
            pdf.set_font('NanumGothic', '', 10)
            pdf.multi_cell(0, 6, f'환자분께서 {years}년 동안 사용하실 경우, 하루 평균 비용은 약 {int(daily_roi):,}원입니다. 평생 구강 건강을 위한 가장 합리적인 투자입니다.')
            pdf.ln(5)

            if os.path.exists("excellence_evidence.jpg"):
                pdf.image("excellence_evidence.jpg", x=35, w=140)
            
            if os.path.exists("qrcode.png"):
                pdf.image("qrcode.png", x=165, y=235, w=30)
                pdf.set_xy(140, 267)
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
