import io
import os
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN & PHONG CÁCH FINTECH / BANKING
# ==============================================================================
st.set_page_config(
    page_title="Project 06 - NHNN RegTech Platform",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS phong cách Fintech / Ngân hàng (Dark Navy, Slate, Gold/Blue accents)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main-title {
        color: #0F2A4A;
        font-weight: 800;
        font-size: 1.9rem;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #4A5568;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }
    .refusal-alert {
        background-color: #FFF5F5;
        border-left: 5px solid #E53E3E;
        color: #C53030;
        padding: 12px 16px;
        border-radius: 6px;
        font-weight: 500;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CƠ SỞ TRI THỨC VĂN BẢN PHÁP LUẬT NHNN (EMBEDDED KNOWLEDGE BASE)
# ==============================================================================
LEGAL_KB = """
[CĂN CỨ PHÁP LÝ NHNN]
1. Thông tư số 09/2023/TT-NHNN (Hướng dẫn thực hiện Luật Phòng, chống rửa tiền):
- Điều 3 khoản 4: Phương pháp chấm điểm để đánh giá rủi ro rửa tiền và mức độ phù hợp của chính sách nội bộ. Tiêu chí, thang điểm và cách phân loại rõ ràng (Trang 4-5).
- Điều 3 khoản 5: Thu thập dữ liệu đánh giá rủi ro theo năm và hoàn thành báo cáo chậm nhất ngày 31/3 năm tiếp theo gửi Cục PCRT (Trang 5).
- Điều 4 khoản 1: Đối tượng báo cáo xây dựng quy trình quản lý rủi ro rửa tiền và phân loại khách hàng theo 3 mức độ rủi ro (Trang 6).
- Điều 4 khoản 5: Áp dụng các biện pháp tăng cường đối với khách hàng có mức rủi ro rửa tiền cao (Trang 7).
- Điều 5 khoản 6: Quy định về tuyển dụng nhân sự và đào tạo kiến thức cơ bản về phòng, chống rửa tiền trong thời hạn 06 tháng kể từ ngày tuyển dụng (Trang 9).

2. Thông tư số 12/2024/TT-NHNN (Sửa đổi, bổ sung Thông tư số 39/2016/TT-NHNN về hoạt động cho vay):
- Điều 1 khoản 1: Bổ sung khoản 11 vào Điều 2: Khoản cho vay có mức giá trị nhỏ là khoản vay không vượt quá 100.000.000 (một trăm triệu) đồng Việt Nam (Trang 1).
- Điều 1 khoản 4: Bổ sung quy định hồ sơ vay vốn tại Điều 9: Khoản vay nhỏ dưới 100 triệu không bắt buộc phải có phương án sử dụng vốn khả thi, chỉ cần thông tin tối thiểu về mục đích hợp pháp và khả năng tài chính (Trang 2-3).
- Điều 1 khoản 5: Sửa đổi Điều 16 về trách nhiệm cung cấp tài liệu chứng minh sử dụng vốn vay đúng mục đích (Trang 3).
- Điều 1 khoản 7: Sửa đổi Điều 24 về kiểm tra, giám sát việc sử dụng vốn vay. Tổ chức tín dụng có quyền tự quyết định hình thức kiểm tra đối với khoản vay nhỏ (Trang 4).
- Điều 2: Bãi bỏ hiệu lực của Điều 29, Điều 32 và Điều 32g Thông tư 39/2016/TT-NHNN (Trang 5).
"""

# ==============================================================================
# 3. KHỞI TẠO DỮ LIỆU BAN ĐẦU
# ==============================================================================
if "diff_data" not in st.session_state:
    st.session_state.diff_data = pd.DataFrame([
        {
            "Change_ID": "LOAN-01",
            "Legal_Basis": "TT 12/2024 Điều 1 Khoản 1",
            "Old_Text": "(Chưa quy định riêng hạn mức định lượng cho khoản vay nhỏ)",
            "New_Text": "Khoản cho vay có mức giá trị nhỏ là khoản vay không vượt quá 100.000.000 (một trăm triệu) đồng Việt Nam.",
            "Change_Type": "Added",
            "Review_Status": "Approve"
        },
        {
            "Change_ID": "LOAN-02",
            "Legal_Basis": "TT 12/2024 Điều 1 Khoản 4",
            "Old_Text": "Mọi khoản vay bắt buộc phải có phương án sử dụng vốn khả thi và kế hoạch trả nợ chi tiết.",
            "New_Text": "Khoản vay giá trị nhỏ (<= 100 triệu VNĐ) được miễn lập phương án sử dụng vốn chi tiết, chỉ cần nêu mục đích hợp pháp.",
            "Change_Type": "Modified",
            "Review_Status": "Approve"
        },
        {
            "Change_ID": "LOAN-03",
            "Legal_Basis": "TT 12/2024 Điều 1 Khoản 5",
            "Old_Text": "Khách hàng phải gửi văn bản chứng minh mục đích sử dụng vốn theo từng đợt giải ngân nghiêm ngặt.",
            "New_Text": "Khách hàng cung cấp tài liệu chứng minh sử dụng vốn theo thỏa thuận; đối với khoản vay tiêu dùng nhỏ, được áp dụng phương thức linh hoạt.",
            "Change_Type": "Modified",
            "Review_Status": "Approve"
        },
        {
            "Change_ID": "LOAN-04",
            "Legal_Basis": "TT 12/2024 Điều 1 Khoản 7",
            "Old_Text": "Bắt buộc kiểm tra thực địa việc sử dụng vốn định kỳ đối với 100% khoản vay sau giải ngân.",
            "New_Text": "Tổ chức tín dụng tự quyết định phương thức và chịu trách nhiệm về kiểm tra, giám sát sau cho vay đối với khoản vay nhỏ.",
            "Change_Type": "Modified",
            "Review_Status": "Approve"
        },
        {
            "Change_ID": "LOAN-05",
            "Legal_Basis": "TT 12/2024 Điều 2",
            "Old_Text": "Quy định trình tự, thủ tục kiểm soát tại Điều 29, 32 và 32g Thông tư 39/2016/TT-NHNN.",
            "New_Text": "Chính thức bãi bỏ áp dụng toàn bộ Điều 29, Điều 32 và Điều 32g.",
            "Change_Type": "Removed",
            "Review_Status": "Approve"
        }
    ])

if "checklist_data" not in st.session_state:
    st.session_state.checklist_data = pd.DataFrame([
        {
            "ID": "AML-01",
            "Requirement": "Xây dựng phương pháp chấm điểm rủi ro rửa tiền theo thang điểm và tiêu chí rõ ràng.",
            "Subject": "Khối Quản trị Rủi ro & Khối Tuân thủ",
            "Action": "Ban hành bảng tiêu chí chấm điểm và ma trận rủi ro rửa tiền định lượng.",
            "Control": "Quy chế Quản lý rủi ro rửa tiền nội bộ được phê duyệt.",
            "Status": "Đã tuân thủ"
        },
        {
            "ID": "AML-02",
            "Requirement": "Hoàn thành báo cáo đánh giá rủi ro rửa tiền định kỳ hàng năm.",
            "Subject": "Ban Phòng chống Rửa tiền (AML)",
            "Action": "Thu thập dữ liệu năm và hoàn thành báo cáo chậm nhất ngày 31/3 năm tiếp theo.",
            "Control": "Báo cáo nộp Cục Phòng, chống rửa tiền (NHNN) có biên nhận.",
            "Status": "Đang xử lý"
        },
        {
            "ID": "AML-05",
            "Requirement": "Đào tạo kiến thức cơ bản về phòng, chống rửa tiền cho nhân sự mới.",
            "Subject": "Khối Nhân sự (HR) & Khối Tuân thủ",
            "Action": "Tổ chức đào tạo hoàn thành trong vòng 6 tháng kể từ ngày tuyển dụng.",
            "Control": "Danh sách điểm danh LMS và bài test nội bộ đạt chuẩn.",
            "Status": "Đang xử lý"
        },
        {
            "ID": "LOAN-01",
            "Requirement": "Thiết lập hạn mức và luồng thẩm định riêng cho khoản vay nhỏ không quá 100 triệu.",
            "Subject": "Khối Khách hàng Cá nhân & Khối Tín dụng",
            "Action": "Cấu hình luồng phê duyệt và điều kiện giải ngân riêng trên hệ thống LOS.",
            "Control": "Biên bản nghiệm thu UAT hệ thống LOS và Quyết định ban hành sản phẩm.",
            "Status": "Chưa thực hiện"
        }
    ])

if "impact_map_data" not in st.session_state:
    st.session_state.impact_map_data = pd.DataFrame([
        {
            "Change_ID": "LOAN-01",
            "Legal_Basis": "TT 12/2024/TT-NHNN, Điều 1 Khoản 1",
            "Change_Summary": "Bổ sung khái niệm khoản vay nhỏ dưới 100 triệu VNĐ.",
            "Requirement": "Định danh và thiết lập luồng xử lý riêng cho khoản vay <= 100tr",
            "Affected_Department": "Khối Tín dụng Cá nhân, Khối CNTT, Khối QLRR",
            "Affected_Process": "Quy trình Khởi tạo & Phê duyệt Khoản vay Tiêu dùng",
            "Affected_Data_Field": "Is_Small_Loan, Loan_Limit_Amount",
            "Impact_Level": "Cao",
            "Required_Action": "Sửa đổi Quy chế cho vay; Cập nhật logic thẩm định hệ thống LOS.",
            "Evidence": "Quy chế Tín dụng sửa đổi; Test report hệ thống Core/LOS.",
            "Verification_Status": "Đã có căn cứ"
        },
        {
            "Change_ID": "LOAN-02",
            "Legal_Basis": "TT 12/2024/TT-NHNN, Điều 1 Khoản 4",
            "Change_Summary": "Miễn trừ phương án sử dụng vốn chi tiết với khoản vay nhỏ.",
            "Requirement": "Đơn giản hóa hồ sơ vay vốn dưới 100 triệu đồng",
            "Affected_Department": "Khối Khách hàng Cá nhân, Khối Pháp chế & Tuân thủ",
            "Affected_Process": "Quy trình Tiếp nhận & Thẩm định Hồ sơ Vay vốn",
            "Affected_Data_Field": "Capital_Use_Purpose_Type, Feasibility_Study_Doc",
            "Impact_Level": "Trung bình",
            "Required_Action": "Rút gọn biểu mẫu đăng ký vay vốn, chỉ yêu cầu cam kết mục đích hợp pháp.",
            "Evidence": "Bộ biểu mẫu hồ sơ vay vốn ban hành mới.",
            "Verification_Status": "Đã có căn cứ"
        },
        {
            "Change_ID": "LOAN-05",
            "Legal_Basis": "TT 12/2024/TT-NHNN, Điều 2",
            "Change_Summary": "Bãi bỏ Điều 29, 32 và 32g Thông tư 39/2016/TT-NHNN.",
            "Requirement": "Loại bỏ các quy trình và báo cáo liên quan đến điều khoản bãi bỏ",
            "Affected_Department": "Khối Tuân thủ, Khối Báo cáo Thống kê",
            "Affected_Process": "Quy trình Báo cáo Định kỳ NHNN",
            "Affected_Data_Field": "Chưa xác định",
            "Impact_Level": "Thấp",
            "Required_Action": "Rà soát lại danh mục báo cáo quản trị, ngừng tạo các mẫu biểu thừa.",
            "Evidence": "Văn bản hướng dẫn bãi bỏ thủ tục nội bộ.",
            "Verification_Status": "Đã có căn cứ"
        },
        {
            "Change_ID": "AML-02",
            "Legal_Basis": "TT 09/2023/TT-NHNN, Điều 3 Khoản 5",
            "Change_Summary": "Thời hạn nộp báo cáo đánh giá rủi ro rửa tiền hàng năm là 31/3.",
            "Requirement": "Hoàn thiện và gửi báo cáo rủi ro rửa tiền định kỳ đúng hạn",
            "Affected_Department": "Khối Tuân thủ, Ban Phòng Chống Rửa Tiền",
            "Affected_Process": "Quy trình Thu thập Dữ liệu & Báo cáo AML Hằng năm",
            "Affected_Data_Field": "AML_Risk_Score, Annual_Report_Date",
            "Impact_Level": "Cao",
            "Required_Action": "Chốt số liệu trước 15/02 hằng năm, dự thảo báo cáo phê duyệt trước 15/03.",
            "Evidence": "Báo cáo nộp Cục PCRT có xác nhận tiếp nhận điện tử.",
            "Verification_Status": "Đã có căn cứ"
        }
    ])

# ==============================================================================
# 4. THANH SIDEBAR (ĐÃ CẬP NHẬT TÊN THÀNH VIÊN)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🏛️ NHNN RegTech AI")
    st.markdown("**Project 06: Compliance Platform**")
    st.caption("Nền tảng Tra cứu & Phân tích Tác động Tuân thủ")

    st.markdown("---")
    st.markdown("#### 👥 Đội ngũ thực hiện")
    st.markdown("""
    - **👑 Nhóm trưởng:** Phương Thảo
    - **Thành viên:**
        - Bảo Châu
        - Minh Anh
        - Như Ý
        - Thuý Hiền
        - Ánh Ngọc
    """)

    st.markdown("---")
    st.markdown("#### ⚙️ Cấu hình Gemini AI")
    gemini_api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
    model_name = st.selectbox("Chọn mô hình", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.caption("💡 Hệ thống có sẵn bộ suy luận tự động, bạn có thể tra cứu ngay mà không bắt buộc có API Key.")

# ==============================================================================
# 5. HEADER CHÍNH & METRICS TỔNG QUAN
# ==============================================================================
st.markdown('<div class="main-title">🏛️ Regulation & Compliance Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hệ thống AI Tra cứu, So sánh Diff Engine & Phân tích Tác động Quy định Ngân hàng Nhà nước</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Điều khoản đã phân tích", "35 Điều", "TT 12/2024 & TT 09/2023")
with m2:
    st.metric("Yêu cầu tuân thủ cốt lõi", f"{len(st.session_state.checklist_data)} Mục", "4 Trường chuẩn")
with m3:
    completed = len(st.session_state.checklist_data[st.session_state.checklist_data["Status"] == "Đã tuân thủ"])
    pct = int((completed / len(st.session_state.checklist_data)) * 100) if len(st.session_state.checklist_data) > 0 else 0
    st.metric("Tỷ lệ tuân thủ", f"{pct}%", f"{completed}/{len(st.session_state.checklist_data)} hoàn thành")
with m4:
    high_cnt = len(st.session_state.impact_map_data[st.session_state.impact_map_data["Impact_Level"] == "Cao"])
    st.metric("Thay đổi tác động CAO", f"{high_cnt} Điểm", "Cần ưu tiên xử lý", delta_color="inverse")

st.write("")

# ==============================================================================
# 6. GIAO DIỆN 3 TAB
# ==============================================================================
tab1, tab2, tab3 = st.tabs([
    "🔍 TAB 1: TRA CỨU & HỎI ĐÁP (RAG Q&A)",
    "📊 TAB 2: SO SÁNH VĂN BẢN (DIFF COMPARISON)",
    "📋 TAB 3: CHECKLIST & BẢN ĐỒ TÁC ĐỘNG"
])

# ------------------------------------------------------------------------------
# TAB 1: RAG Q&A WITH CITATION & REFUSAL MECHANISM
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("#### 🔍 Tra cứu & Giải đáp Quy định NHNN với AI")
    st.caption("AI tra cứu theo cơ sở dữ liệu pháp lý Thông tư 09/2023/TT-NHNN và Thông tư 12/2024/TT-NHNN.")

    st.markdown("**📌 Câu hỏi mẫu:**")
    c1, c2, c3 = st.columns(3)
    sample_query = ""
    if c1.button("⏱️ Hạn nộp báo cáo AML hằng năm?"):
        sample_query = "Thời hạn nộp báo cáo đánh giá rủi ro rửa tiền hằng năm của đối tượng báo cáo là khi nào?"
    if c2.button("💰 Hạn mức khoản vay nhỏ theo TT 12?"):
        sample_query = "Quy định thế nào là khoản cho vay có mức giá trị nhỏ theo Thông tư 12/2024/TT-NHNN?"
    if c3.button("🛡️ Biện pháp đối với rủi ro rửa tiền cao?"):
        sample_query = "Các biện pháp tăng cường đối với khách hàng có mức rủi ro rửa tiền cao là gì?"

    query_input = st.text_input("Nhập câu hỏi nghiệp vụ:", value=sample_query, placeholder="Ví dụ: Quy định về thời hạn đào tạo nhân sự phòng chống rửa tiền?")

    if st.button("🚀 Gửi câu hỏi", type="primary"):
        if not query_input.strip():
            st.warning("Vui lòng nhập câu hỏi.")
        else:
            with st.spinner("AI đang truy xuất cơ sở pháp lý và tổng hợp trích dẫn..."):
                response_text = ""
                if gemini_api_key.strip():
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=gemini_api_key)
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=f"""
Bạn là Chuyên gia Pháp chế Ngân hàng Nhà nước Việt Nam (NHNN).
Dựa trên căn cứ pháp lý sau đây để trả lời:
{LEGAL_KB}

QUY TẮC BẮT BUỘC:
1. Luôn đính kèm Citation: Dẫn nguồn: [Tên văn bản] | [Điều] | [Khoản] | [Nội dung/Trang].
2. NGUYÊN TẮC AN TOÀN (Refusal Mechanism): Nếu câu hỏi KHÔNG có trong cơ sở pháp lý trên, bắt buộc trả lời chính xác bằng câu:
"⚠️ Cảnh báo: Thiếu căn cứ nguồn rõ ràng trong văn bản NHNN được cung cấp." và không suy diễn gì thêm.
"""
                        )
                        res = model.generate_content(query_input)
                        response_text = res.text
                    except Exception as e:
                        st.error(f"Lỗi kết nối Gemini API: {e}")
                        response_text = None

                # Fallback Offline Engine khi chưa có API Key
                if not response_text:
                    q = query_input.lower()
                    if "rửa tiền" in q and ("thời hạn" in q or "báo cáo" in q or "31/3" in q):
                        response_text = """Đối tượng báo cáo phải thu thập dữ liệu đánh giá rủi ro rửa tiền theo năm và hoàn thành báo cáo chậm nhất vào ngày 31 tháng 3 của năm tiếp theo gửi Cục Phòng, chống rửa tiền.\n\n**Dẫn nguồn:** [Thông tư số 09/2023/TT-NHNN] | [Điều 3] | [Khoản 5] | [Trang 5]"""
                    elif "giá trị nhỏ" in q or "100 triệu" in q or "vay nhỏ" in q:
                        response_text = """Khoản cho vay có mức giá trị nhỏ là khoản vay không vượt quá 100.000.000 (một trăm triệu) đồng Việt Nam. Đối với khoản vay này, khách hàng không bắt buộc phải cung cấp phương án sử dụng vốn khả thi mà chỉ cần cung cấp tối thiểu thông tin về mục đích sử dụng vốn hợp pháp và khả năng tài chính.\n\n**Dẫn nguồn:** [Thông tư số 12/2024/TT-NHNN] | [Điều 1] | [Khoản 1 & Khoản 4] | [Trang 1-3]"""
                    elif "tăng cường" in q or "rủi ro cao" in q:
                        response_text = """Đối với khách hàng có mức rủi ro rửa tiền cao, ngân hàng phải áp dụng các biện pháp tăng cường: thu thập bổ sung thông tin nhận biết khách hàng, tăng cường tần suất kiểm tra giao dịch và bắt buộc có sự phê duyệt của người quản lý cấp cao.\n\n**Dẫn nguồn:** [Thông tư số 09/2023/TT-NHNN] | [Điều 4] | [Khoản 5] | [Trang 7]"""
                    elif "đào tạo" in q or "tuyển dụng" in q or "6 tháng" in q:
                        response_text = """Đối tượng báo cáo có trách nhiệm tuyển dụng nhân sự và tổ chức đào tạo kiến thức cơ bản về phòng, chống rửa tiền cho nhân viên mới trong thời hạn 06 tháng kể từ ngày tuyển dụng.\n\n**Dẫn nguồn:** [Thông tư số 09/2023/TT-NHNN] | [Điều 5] | [Khoản 6] | [Trang 9]"""
                    else:
                        response_text = "⚠️ Cảnh báo: Thiếu căn cứ nguồn rõ ràng trong văn bản NHNN được cung cấp."

                if "⚠️ Cảnh báo: Thiếu căn cứ nguồn rõ ràng" in response_text:
                    st.markdown(f'<div class="refusal-alert">{response_text}</div>', unsafe_allow_html=True)
                else:
                    st.success("✅ Đã tìm thấy căn cứ pháp lý:")
                    st.markdown(response_text)

# ------------------------------------------------------------------------------
# TAB 2: SO SÁNH VĂN BẢN (DIFF COMPARISON ENGINE)
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("#### 📊 Đối chiếu Biến động Văn bản: TT 39/2016 vs TT 12/2024")
    st.caption("Công cụ Diff Engine nhận diện biến động điều khoản và tích hợp Thẩm duyệt con người (Human-in-the-loop).")

    df_diff = st.session_state.diff_data.copy()

    col_filter, _ = st.columns([2, 4])
    with col_filter:
        types = st.multiselect("Bộ lọc trạng thái thay đổi:", ["Added", "Modified", "Removed"], default=["Added", "Modified", "Removed"])
    if types:
        df_diff = df_diff[df_diff["Change_Type"].isin(types)]

    edited_diff = st.data_editor(
        df_diff,
        column_config={
            "Change_ID": st.column_config.TextColumn("Mã điều", width="small", disabled=True),
            "Legal_Basis": st.column_config.TextColumn("Căn cứ pháp lý", width="medium", disabled=True),
            "Old_Text": st.column_config.TextColumn("Nội dung gốc (TT 39/2016)", width="large", disabled=True),
            "New_Text": st.column_config.TextColumn("Nội dung mới (TT 12/2024)", width="large", disabled=True),
            "Change_Type": st.column_config.SelectboxColumn("Loại thay đổi", options=["Added", "Modified", "Removed"], width="small", disabled=True),
            "Review_Status": st.column_config.SelectboxColumn("Human-in-the-loop", options=["Approve", "Edit"], width="medium", required=True)
        },
        use_container_width=True,
        hide_index=True,
        key="tab2_diff_editor"
    )

    btn_c1, btn_c2, _ = st.columns([1.5, 1.5, 4])
    with btn_c1:
        if st.button("💾 Lưu phê duyệt", key="save_diff"):
            st.session_state.diff_data.update(edited_diff)
            st.success("Đã ghi nhận phê duyệt điều khoản!")
    with btn_c2:
        buf = io.StringIO()
        edited_diff.to_csv(buf, index=False, encoding="utf-8-sig")
        st.download_button(
            "📥 Export CSV So Sánh",
            data=buf.getvalue().encode("utf-8-sig"),
            file_name="diff_comparison_nhnn.csv",
            mime="text/csv"
        )

# ------------------------------------------------------------------------------
# TAB 3: CHECKLIST & BẢN ĐỒ TÁC ĐỘNG (IMPACT MAP)
# ------------------------------------------------------------------------------
with tab3:
    sub1, sub2 = st.tabs([
        "📋 Sub-tab 1: Compliance Checklist (4 Trường Cốt Lõi)",
        "🗺️ Sub-tab 2: Impact Map (11 Cột Chuẩn)"
    ])

    # SUB-TAB 1
    with sub1:
        st.markdown("##### 📋 Compliance Checklist (Yêu cầu, Chủ thể, Hành động, Kiểm soát)")
        chk_df = st.session_state.checklist_data.copy()

        edited_chk = st.data_editor(
            chk_df,
            column_config={
                "ID": st.column_config.TextColumn("Mã nghĩa vụ", width="small", disabled=True),
                "Requirement": st.column_config.TextColumn("Requirement (Yêu cầu tuân thủ)", width="large"),
                "Subject": st.column_config.TextColumn("Subject (Chủ thể thực hiện)", width="medium"),
                "Action": st.column_config.TextColumn("Action (Hành động bắt buộc)", width="large"),
                "Control": st.column_config.TextColumn("Evidence/Control (Bằng chứng kiểm soát)", width="large"),
                "Status": st.column_config.SelectboxColumn("Trạng thái", options=["Chưa thực hiện", "Đang xử lý", "Đã tuân thủ"], width="medium", required=True)
            },
            use_container_width=True,
            hide_index=True,
            key="tab3_sub1_editor"
        )

        sc1, sc2, _ = st.columns([1.5, 1.5, 4])
        with sc1:
            if st.button("💾 Lưu Checklist", key="save_chk"):
                st.session_state.checklist_data = edited_chk
                st.rerun()
        with sc2:
            buf_chk = io.StringIO()
            edited_chk.to_csv(buf_chk, index=False, encoding="utf-8-sig")
            st.download_button("📥 Export Checklist CSV", data=buf_chk.getvalue().encode("utf-8-sig"), file_name="compliance_checklist.csv", mime="text/csv")

    # SUB-TAB 2
    with sub2:
        st.markdown("##### 🗺️ Bản Đồ Tác Động Quy Định (Regulatory Impact Map - 11 Cột)")
        imp_df = st.session_state.impact_map_data.copy()

        edited_imp = st.data_editor(
            imp_df,
            column_config={
                "Change_ID": st.column_config.TextColumn("Change_ID", width="small"),
                "Legal_Basis": st.column_config.TextColumn("Legal_Basis", width="medium"),
                "Change_Summary": st.column_config.TextColumn("Change_Summary", width="large"),
                "Requirement": st.column_config.TextColumn("Requirement", width="large"),
                "Affected_Department": st.column_config.TextColumn("Affected_Department", width="medium"),
                "Affected_Process": st.column_config.TextColumn("Affected_Process", width="large"),
                "Affected_Data_Field": st.column_config.TextColumn("Affected_Data_Field", width="medium"),
                "Impact_Level": st.column_config.SelectboxColumn("Impact_Level", options=["Cao", "Trung bình", "Thấp"], width="small"),
                "Required_Action": st.column_config.TextColumn("Required_Action", width="large"),
                "Evidence": st.column_config.TextColumn("Evidence", width="large"),
                "Verification_Status": st.column_config.SelectboxColumn("Verification_Status", options=["Đã có căn cứ", "Dự kiến", "Chưa xác định"], width="medium")
            },
            use_container_width=True,
            hide_index=True,
            key="tab3_sub2_editor"
        )

        si1, si2, _ = st.columns([1.5, 1.5, 4])
        with si1:
            if st.button("💾 Lưu Impact Map", key="save_imp"):
                st.session_state.impact_map_data = edited_imp
                st.success("Đã đồng bộ dữ liệu Impact Map!")
        with si2:
            buf_imp = io.StringIO()
            edited_imp.to_csv(buf_imp, index=False, encoding="utf-8-sig")
            st.download_button("📥 Export Impact Map CSV", data=buf_imp.getvalue().encode("utf-8-sig"), file_name="regulatory_impact_map.csv", mime="text/csv")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("<center><small style='color: #718096;'>Project 06: Regulation & Compliance Intelligence Platform • Khoa Ngân hàng & Fintech</small></center>", unsafe_allow_html=True)