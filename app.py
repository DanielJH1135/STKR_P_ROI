import streamlit as st
import os
from fpdf import FPDF
from datetime import datetime, time, timedelta

# CSS 주입: 슬라이더(config.toml 처리), 액티브 툴팁 및 링크 스타일링
st.markdown("""
<style>
    /* --- 액티브 툴팁(마우스 오버) 및 하이퍼링크 커스텀 --- */
    .active-tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
        font-weight: bold;
        border-bottom: 2px dashed #46B98C; /* 민트 그린 점선 */
    }
    .active-tooltip a {
        text-decoration: none;
        color: #46B98C !important; /* 민트 그린 색상 */
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
        pointer-events: none; /* 툴팁이 클릭을 방해하지 않도록 설정 */
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
    
    /* 메인 페이지 하단 고정 주의문구 */
    .footer-disclaimer {
        color: #A9A9A9;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 50px;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# PDF 클래스 정의 (에러 방지용 텍스트 전용)
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
        self.set_y(-25)
        if os.path.exists("NanumGothic.ttf"):
            self.set_font('NanumGothic', '', 8)
        self.set_text_color(180, 180, 180)
        self.cell(0, 5, '※ 임플란트는 관리 여하에 따라 사용기간은 상이합니다.', 0, 1, 'C')
        self.cell(0, 5, '본 자료는 환자 상담용 참고자료이며, 무단 전재 및 온라인 게시를 금지합니다.', 0, 1, 'C')
        self.cell(0, 5, '본 안내서는 상담용 자료이며, 정확한 비용은 수술 계획에 따라 변경될 수 있습니다.', 0, 0, 'C')

# --- 사이드바: 데이터 및 견적 정보 ---
with st.sidebar:
    st.header("🏆 스트라우만 임상 데이터")
    
    # 임상 데이터 표 수정: 민트그린 적용, 하이퍼링크 및 각주 추가
    st.markdown("""
        <table style="width:100%; border-collapse: collapse; font-size: 0.9rem;">
            <tr style="border-bottom: 1px solid #ddd; text-align: left;">
                <th style="padding: 8px;">브랜드</th>
                <th style="padding: 8px;">장기생존률</th>
                <th style="padding: 8px;">근거</th>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 8px;"><b>스트라우만</b></td>
                <td style="padding: 8px;"><b>99.7%</b></td>
                <td style="padding: 8px;">
                    <span class="active-tooltip">
                        <a href="https://pubmed.ncbi.nlm.nih.gov/25370914/" target="_blank">10년이상의 연구논문</a>
                        <span class="tooltip-content">van Velzen FJ, et al. J Clin Periodontal. 2015; 374 implants, 177 patients, 10-year follow-up</span>
                    </span>
                </td>
            </tr>
            <tr>
                <td style="padding: 8px;">임플란트 평균</td>
                <td style="padding: 8px;">약 93~96%</td>
                <td style="padding: 8px;">
                    <span class="active-tooltip">
                        <a href="https://www.sciencedirect.com/science/article/abs/pii/S0300571219300491" target="_blank">메타분석 데이터</a>
                        <span class="tooltip-content">Howe MS, Keys W, Richards D. J Dent. 2019;84:9-21.</span>
                    </span>
                </td>
            </tr>
        </table>
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
        validity_date = st.date_input("견적 유효기간", datetime.now() + timedelta(days=30))
    with col_t:
        surgery_time = st.time_input("상담 시간", value=time(14, 0))
    
    full_validity_dt = f"{validity_date.strftime('%Y-%m-%d')} 까지 유효"
    
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
        discount = st.number_input("조정 금액 (원)", value=0, step=10000)
        final_p = total_p - discount
        # 의료법 준수 표현으로 수정
        st.markdown(f"**상담 가격 : {final_p:,.0f}원**")
        st.caption(f"(원내 공식 비급여 고찰가격 : {total_p:,.0f}원)")
    with c2:
        years = st.slider("예상 사용 기간 (년)", 5, 50, 20)
        st.markdown(f"**견적 유효기간:** {full_validity_dt}")
        
        st.markdown("""
            <div style="color: #A9A9A9; font-size: 0.85rem; margin-top: 10px; line-height: 1.4;">
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

    # 1. 메인페이지 하단 보안 주의 문구
    st.markdown("""
        <div class="footer-disclaimer">
            본 상담툴은 의료진의 상담 참고용이며, 외부(SNS, 블로그 등)으로 유출을 금지합니다.
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("신뢰의 브랜드, 스트라우만. 그 이유는?")
    # 깃허브에 올릴 새로운 상세페이지 이미지들로 교체
    new_images = ["상세페이지 1.png", "상세페이지 2.png", "상세페이지 3.png"]
    for img in new_images:
        if os.path.exists(img):
            st.image(img, use_container_width=True)
        else:
            st.error(f"이미지 파일({img})을 찾을 수 없습니다. 깃허브에 해당 파일이 있는지 확인해주세요.")
    
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
            # 수술예정일 -> 견적 유효기간으로 변경
            pdf.cell(0, 6, f'발행일: {datetime.now().strftime("%Y-%m-%d")} / 견적 유효기간: {full_validity_dt}', 0, 1)
            pdf.ln(3)
            
            pdf.set_font('NanumGothic', '', 14)
            # 가격 표현 수정 (의료법 준수)
            pdf.cell(0, 8, f'■ 상담 가격: {final_p:,.0f}원 (원내 공식 비급여 고찰가격 : {total_p:,.0f}원)', 0, 1)
            
            # 4. PDF 가격 아래 시뮬레이션 주의 문구 추가
            pdf.set_font('NanumGothic', '', 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 6, '본 계산 결과는 단순 시뮬레이션이며, 실제 진료비와 치료 결과는 환자의 상태에 따라 다를 수 있음.', 0, 1)
            pdf.ln(2)

            pdf.set_font('NanumGothic', '', 14)
            pdf.set_text_color(0, 90, 171)
            pdf.cell(0, 12, f'하루 평균 투자 비용: {int(daily_roi):,}원 ({years}년 기준)', 1, 1, 'C')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
            
            pdf.set_font('NanumGothic', '', 10)
            pdf.multi_cell(0, 6, f'환자분께서 {years}년 동안 사용하실 경우, 하루 평균 비용은 약 {int(daily_roi):,}원입니다. 평생 구강 건강을 위한 가장 합리적인 투자입니다.')
            pdf.ln(5)

            # 상세페이지1을 PDF 대표 이미지로 사용 (공간 확보를 위해 w 축소)
            if os.path.exists("상세페이지1.png"):
                pdf.image("상세페이지1.png", x=35, w=140)
            
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
