import streamlit as st
import pandas as pd
from function import prepare_boxes, pack_boxes, plot_pallet, get_data

# 1. 웹 페이지 레이아웃 설정
st.set_page_config(page_title="3D 패킹 시뮬레이터", layout="wide")

st.title("3D 패킹 시뮬레이터")

# 2. 사이드바 설정 (입력 및 실행 버튼)
st.sidebar.header("🚚 파레트 설정")
p_w = st.sidebar.number_input("파레트 가로(W)", value=110)
p_h = st.sidebar.number_input("파레트 세로(H)", value=110)
p_d = st.sidebar.number_input("파레트 높이(D)", value=150)
p_m = st.sidebar.number_input("최대 적재 중량(KG)", value=1000)
p_n = st.sidebar.slider("파레트 개수", 1, 20, 5)

uploaded_file = st.sidebar.file_uploader("박스 규격 CSV 파일을 업로드하세요", type=["csv"])

# --- 사이드바: 시뮬레이션 시작 버튼 ---
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if st.sidebar.button("🚀 시뮬레이션 시작", type="primary", use_container_width=True):
        with st.spinner('계산 중...'):
            items = prepare_boxes(df)
            packer_result = pack_boxes(items, p_w, p_h, p_d, p_m, p_n)
            
            active_bins = [b for b in packer_result.bins if len(b.items) > 0]
            all_figs = [plot_pallet(b, p_w, p_h) for b in active_bins]
            bin_details = [get_data(b, p_w, p_h, p_d) for b in active_bins]
            
            # 세션 상태 저장
            st.session_state['active_bins'] = active_bins
            st.session_state['all_figs'] = all_figs
            st.session_state['bin_idx'] = 0
            st.session_state['bin_details'] = bin_details
            st.session_state['summary'] = {
                "used": len(active_bins),
                "success": sum(len(b.items) for b in active_bins),
                "unfitted": len(packer_result.bins[-1].unfitted_items)
            }
            st.rerun()

# --- 메인 화면 레이아웃 ---
if 'summary' in st.session_state:
    col1, col2 = st.columns([1, 2])
    
    # --- 왼쪽 컬럼: 분석 결과 데이터 ---
    with col1:
        s = st.session_state['summary']
        idx = st.session_state['bin_idx']
        details = st.session_state['bin_details'][idx]

        st.subheader("📊 전체 요약")
        m1, m2, m3 = st.columns(3)
        m1.metric("사용 파레트", f"{s['used']}개")
        m2.metric("적재 박스", f"{s['success']}개")
        m3.metric("미적재 박스", f"{s['unfitted']}개")
        
        st.divider()

        st.subheader(f"📍 Pallet {idx + 1} 상세")
        
        # 아이템별 수량 표
        st.write("**📦 아이템 구성**")
        counts_df = pd.DataFrame([details[0]]).T.rename(columns={0: '수량'})
        st.table(counts_df)
        
        # 부피 통계
        v_col1, v_col2 = st.columns(2)
        v_col1.metric("적재 부피", f"{details[1]:,.0f}")
        v_col2.metric("남은 부피", f"{details[2]:,.0f}")
        
        # 효율성 게이지
        usage_rate = (details[1] / (p_w * p_h * p_d)) * 100
        st.progress(usage_rate / 100, text=f"공간 효율성: {usage_rate:.1f}%")

    # --- 오른쪽 컬럼: 3D 시각화 ---
    with col2:
        st.subheader("🎨 3D 적재 시각화")
        all_figs = st.session_state['all_figs']
        
        b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
        with b_col1:
            if st.button("⬅️ 이전", use_container_width=True) and idx > 0:
                st.session_state['bin_idx'] -= 1
                st.rerun()
        with b_col2:
            st.markdown(f"<h4 style='text-align: center;'>Pallet {idx + 1} / {len(all_figs)}</h4>", unsafe_allow_html=True)
        with b_col3:
            if st.button("다음 ➡️", use_container_width=True) and idx < len(all_figs) - 1:
                st.session_state['bin_idx'] += 1
                st.rerun()

        st.plotly_chart(all_figs[idx], use_container_width=True)
else:
    if not uploaded_file:
        st.info("왼쪽 사이드바에서 CSV 파일을 업로드하고 설정을 확인하세요.")
    else:
        st.success("파일이 업로드되었습니다. '시뮬레이션 시작' 버튼을 눌러주세요!")