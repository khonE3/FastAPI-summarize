"""
Streamlit Frontend for FastAPI Summarize
"""
import streamlit as st
import requests
from typing import Optional
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
API_V1_PREFIX = "/api/v1"

# Page config
st.set_page_config(
    page_title="🌾 AI สรุปข้อความ - ฉบับอีสาน",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Isan Theme (Harmonious Colors)
st.markdown("""
<style>
    /* Import Thai Font */
    @import url('https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;600;700&family=Sarabun:wght@400;600;700&display=swap');
    
    /* Color Palette - อีสานสีสัมพันธ์
       Primary: #8B0000 (แดงเข้ม)
       Secondary: #DC143C (แดงสด)  
       Accent: #FFD700 (ทอง)
       Light: #FFF5E1 (ครีมอ่อน)
       Dark: #3D1F00 (น้ำตาลเข้ม)
    */
    
    * {
        font-family: 'Sarabun', 'Bai Jamjuree', sans-serif;
        font-size: 1.1rem;
    }
    
    /* Main Background - โทนครีมอบอุ่น */
    .stApp {
        background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E1 50%, #FFEFD5 100%);
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 15px, rgba(139,0,0,0.015) 15px, rgba(139,0,0,0.015) 30px);
    }
    
    /* Header - Gradient สีอีสาน */
    .main-header {
        font-size: 5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(120deg, #8B0000, #DC143C, #FF6347, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2rem 0 1rem 0;
        filter: drop-shadow(3px 3px 5px rgba(139,0,0,0.3));
        font-family: 'Bai Jamjuree', sans-serif;
        letter-spacing: 4px;
        line-height: 1.2;
    }
    
    .sub-header {
        font-size: 2rem !important;
        color: #8B0000 !important;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 3px rgba(255,215,0,0.3);
    }
    
    /* Section Headers */
    h1, h2, h3 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #8B0000 !important;
        margin: 1.5rem 0 1rem 0 !important;
        text-shadow: 1px 1px 2px rgba(255,215,0,0.2);
    }
    
    /* Sidebar - แดงเข้มทอง */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5D0000 0%, #8B0000 30%, #A52A2A 100%);
        border-right: 6px solid #FFD700;
        box-shadow: 5px 0 25px rgba(0,0,0,0.4);
    }
    
    section[data-testid="stSidebar"] * {
        color: #FFF5E1 !important;
        font-size: 1.15rem !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFD700 !important;
        font-size: 1.8rem !important;
        border-bottom: 3px solid #FFD700;
        padding-bottom: 0.8rem;
        margin-top: 1.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    section[data-testid="stSidebar"] label {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #FFEAA7 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }
    
    /* Buttons - แดงทองสัมพันธ์ */
    .stButton > button {
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
        color: #FFF5E1 !important;
        border: 4px solid #FFD700;
        border-radius: 20px;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        padding: 1.2rem 3rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(139,0,0,0.4);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #DC143C 0%, #FF4500 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(220,20,60,0.6);
        border-color: #FFDF00;
    }
    
    /* Text Areas - พื้นครีมข้อความน้ำตาล */
    .stTextArea textarea {
        border: 4px solid #8B0000 !important;
        border-radius: 20px !important;
        background: #FFFEF9 !important;
        font-size: 1.2rem !important;
        color: #3D1F00 !important;
        line-height: 1.8 !important;
        padding: 1.5rem !important;
        box-shadow: inset 0 2px 8px rgba(139,0,0,0.1);
    }
    
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 20px rgba(255,215,0,0.5), inset 0 2px 8px rgba(139,0,0,0.1) !important;
        background: #FFFFFF !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #A0826D !important;
        font-size: 1.15rem !important;
    }
    
    /* Labels - น้ำตาลเข้ม */
    label {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #5D3A1A !important;
    }
    
    /* Metrics - สีสัมพันธ์กับธีม */
    div[data-testid="stMetricValue"] {
        color: #8B0000 !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        text-shadow: 2px 2px 4px rgba(255,215,0,0.4);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #5D3A1A !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        background: linear-gradient(135deg, #FFF5E1, #FFE4B5);
        padding: 0.5rem 1rem;
        border-radius: 10px;
    }
    
    /* Success - เขียวกับครีม */
    .stSuccess {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%) !important;
        border: 3px solid #388E3C !important;
        border-left: 8px solid #2E7D32 !important;
        border-radius: 15px;
        padding: 1.5rem !important;
        color: #1B5E20 !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(46,125,50,0.2);
    }
    
    /* Info - ครีมกับน้ำตาล */
    .stInfo {
        background: linear-gradient(135deg, #FFF8DC 0%, #FFEAA7 100%) !important;
        border: 3px solid #D4A017 !important;
        border-left: 8px solid #B8860B !important;
        border-radius: 15px;
        padding: 1.5rem !important;
        color: #5D4E37 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(212,160,23,0.2);
    }
    
    /* Warning - เหลืองกับส้ม */
    .stWarning {
        background: linear-gradient(135deg, #FFF9C4 0%, #FFE082 100%) !important;
        border: 3px solid #F57C00 !important;
        border-left: 8px solid #E65100 !important;
        border-radius: 15px;
        padding: 1.5rem !important;
        color: #E65100 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(245,124,0,0.2);
    }
    
    /* Error - แดงกับชมพู */
    .stError {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%) !important;
        border: 3px solid #D32F2F !important;
        border-left: 8px solid #B71C1C !important;
        border-radius: 15px;
        padding: 1.5rem !important;
        color: #B71C1C !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(211,47,47,0.2);
    }
    
    /* Dividers - ไล่สีอีสาน */
    hr {
        border: none;
        height: 5px;
        background: linear-gradient(90deg, #8B0000, #DC143C, #FFD700, #DC143C, #8B0000);
        margin: 2.5rem 0;
        border-radius: 3px;
        box-shadow: 0 2px 5px rgba(139,0,0,0.3);
    }
    
    /* Sliders - แดงเข้ม */
    .stSlider > div > div > div {
        background: #8B0000 !important;
    }
    
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #5D3A1A !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    
    /* Expander - แดงทองสัมพันธ์ */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #8B0000, #A52A2A) !important;
        color: #FFD700 !important;
        border-radius: 15px 15px 0 0;
        font-weight: 800 !important;
        font-size: 1.4rem !important;
        padding: 1.2rem 1.5rem !important;
        border: 4px solid #FFD700;
        border-bottom: none;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, #FFFEF9, #FFF8E7);
        border: 4px solid #FFD700;
        border-top: 2px solid #D4A017;
        border-radius: 0 0 15px 15px;
        padding: 2rem;
        color: #3D1F00 !important;
        font-size: 1.15rem !important;
        line-height: 1.8;
        box-shadow: inset 0 2px 10px rgba(139,0,0,0.05);
    }
    
    /* Decorative Border Pattern */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 14px;
        background: repeating-linear-gradient(
            90deg,
            #8B0000 0px,
            #8B0000 30px,
            #FFD700 30px,
            #FFD700 60px,
            #DC143C 60px,
            #DC143C 90px
        );
        z-index: 999;
        box-shadow: 0 3px 10px rgba(139,0,0,0.4);
    }
    
    /* Selectbox - พื้นครีมข้อความน้ำตาล */
    .stSelectbox > div > div {
        background: #FFFEF9 !important;
        border: 3px solid #8B0000 !important;
        border-radius: 12px;
        font-size: 1.2rem !important;
        color: #3D1F00 !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(139,0,0,0.15);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #FFD700 !important;
        box-shadow: 0 4px 12px rgba(255,215,0,0.3);
    }
    
    /* Caption Text - น้ำตาลกลาง */
    .caption, [data-testid="stCaptionContainer"] {
        color: #5D3A1A !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        background: linear-gradient(135deg, #FFF5E1, #FFE4B5);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
        border-left: 4px solid #D4A017;
    }
    
    /* Code Blocks - พื้นเข้มข้อความทอง */
    code {
        background: #3D1F00 !important;
        color: #FFD700 !important;
        font-size: 1.1rem !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 8px;
        border: 2px solid #8B0000;
    }
    
    pre {
        background: #2C1810 !important;
        border: 4px solid #8B0000 !important;
        border-radius: 12px;
        padding: 1.5rem !important;
    }
    
    pre code {
        color: #FFD700 !important;
        font-size: 1.1rem !important;
    }
</style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}{API_V1_PREFIX}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def summarize_text(text: str, max_length: int, min_length: int) -> Optional[dict]:
    """Call summarization API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}{API_V1_PREFIX}/summarize/",
            json={
                "text": text,
                "max_length": max_length,
                "min_length": min_length
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout - โมเดลอาจกำลังโหลด กรุณารอสักครู่แล้วลองใหม่")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 ไม่สามารถเชื่อมต่อ API - กรุณาเริ่ม server ก่อน")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


# Header
st.markdown('<p class="main-header">🌾 AI สรุปข้อความ 🌾</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">✨ สรุปเรื่องยาวให้สั้น ด้วยปัญญาประดิษฐ์ ✨</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ การตั้งค่า")
    
    # API Status
    api_status = check_api_health()
    if api_status:
        st.success("✅ ระบบพร้อมใช้งาน")
    else:
        st.error("❌ ระบบยังไม่พร้อม")
        st.info("💡 เปิดเซิร์ฟเวอร์:\n```bash\nuv run uvicorn main:app --reload\n```")
    
    st.divider()
    
    # Settings
    st.subheader("📊 ตั้งค่าการสรุป")
    
    max_length = st.slider(
        "ความยาวสูงสุด (คำ)",
        min_value=30,
        max_value=500,
        value=150,
        step=10,
        help="ข้อความสรุปจะยาวไม่เกินจำนวนนี้"
    )
    
    min_length = st.slider(
        "ความยาวต่ำสุด (คำ)",
        min_value=10,
        max_value=100,
        value=30,
        step=5,
        help="ข้อความสรุปจะยาวไม่ต่ำกว่าจำนวนนี้"
    )
    
    st.divider()
    
    # Examples
    st.subheader("📚 ตัวอย่างข้อความ")
    
    example_texts = {
        "FastAPI": """FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints. The key features are: Fast: Very high performance, on par with NodeJS and Go. Fast to code: Increase the speed to develop features by about 200% to 300%. Fewer bugs: Reduce about 40% of human (developer) induced errors. Intuitive: Great editor support. Completion everywhere. Less time debugging. Easy: Designed to be easy to use and learn. Less time reading docs. Short: Minimize code duplication. Multiple features from each parameter declaration. Robust: Get production-ready code. With automatic interactive documentation. Standards-based: Based on the open standards for APIs: OpenAPI and JSON Schema.""",
        
        "Machine Learning": """Machine Learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine Learning focuses on the development of computer programs that can access data and use it to learn for themselves. The process of learning begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide. The primary aim is to allow the computers learn automatically without human intervention or assistance and adjust actions accordingly.""",
        
        "Climate Change": """Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, such as through variations in the solar cycle. But since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas. Burning fossil fuels generates greenhouse gas emissions that act like a blanket wrapped around the Earth, trapping the sun's heat and raising temperatures. Examples of greenhouse gas emissions that are causing climate change include carbon dioxide and methane. These come from using gasoline for driving a car or coal for heating a building, for example. Clearing land and forests can also release carbon dioxide."""
    }
    
    selected_example = st.selectbox(
        "เลือกตัวอย่าง",
        ["ไม่เลือก"] + list(example_texts.keys())
    )

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 ข้อความเดิม")
    
    # Load example if selected
    default_text = ""
    if selected_example and selected_example != "ไม่เลือก":
        default_text = example_texts[selected_example]
    
    input_text = st.text_area(
        "พิมพ์หรือวางข้อความที่ต้องการสรุป",
        value=default_text,
        height=300,
        placeholder="วางข้อความภาษาอังกฤษที่ต้องการสรุปที่นี่... 🌾",
        help="ข้อความต้องมีความยาวอย่างน้อย 10 ตัวอักษร"
    )
    
    # Character count
    char_count = len(input_text)
    word_count = len(input_text.split())
    st.caption(f"📊 ตัวอักษร: {char_count} | คำ: {word_count}")
    
    # Summarize button
    summarize_btn = st.button(
        "🚀 สรุปข้อความ",
        type="primary",
        use_container_width=True,
        disabled=not api_status or char_count < 10
    )

with col2:
    st.subheader("✨ ข้อความที่สรุปแล้ว")
    
    # Summary result area
    summary_placeholder = st.empty()
    
    if summarize_btn:
        if not input_text or len(input_text) < 10:
            st.warning("⚠️ กรุณากรอกข้อความอย่างน้อย 10 ตัวอักษร")
        else:
            with st.spinner("🤖 กำลังสรุปข้อความ... รอแป๊บเดียว! 🌾"):
                start_time = time.time()
                result = summarize_text(input_text, max_length, min_length)
                elapsed_time = time.time() - start_time
                
                if result:
                    # Display summary
                    with summary_placeholder.container():
                        st.success("✅ สรุปเสร็จแล้ว!")
                        
                        # Summary text
                        st.markdown("### 📝 สรุป:")
                        st.info(result["summary"])
                        
                        # Metrics
                        st.markdown("### 📊 สถิติ:")
                        
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        
                        with metric_col1:
                            st.metric(
                                "ความยาวต้นฉบับ",
                                f"{result['original_length']} ตัวอักษร"
                            )
                        
                        with metric_col2:
                            st.metric(
                                "ความยาวสรุป",
                                f"{result['summary_length']} ตัวอักษร"
                            )
                        
                        with metric_col3:
                            compression = result['compression_ratio'] * 100
                            st.metric(
                                "บีบอัด",
                                f"{compression:.1f}%",
                                delta=f"-{compression:.1f}%"
                            )
                        
                        # Processing time
                        st.caption(f"⏱️ เวลาประมวลผล: {elapsed_time:.2f} วินาที")
                        
                        # Copy button
                        if st.button("📋 คัดลอกข้อความสรุป", use_container_width=True):
                            st.code(result["summary"], language=None)
    else:
        with summary_placeholder.container():
            st.info("👈 กรอกข้อความและกดปุ่ม 'สรุปข้อความ' เพื่อเริ่มต้น")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #8B4513; padding: 1.5rem; background: linear-gradient(135deg, #FFE4B5, #FFDAB9); border-radius: 15px; margin: 1rem 0;'>
    <p style='font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;'>🚀 ขับเคลื่อนด้วยเทคโนโลยี AI ระดับโลก</p>
    <p style='font-size: 1rem;'>📚 โมเดล: facebook/bart-large-cnn | 🔧 เฟรมเวิร์ก: FastAPI + Streamlit</p>
    <p style='font-size: 0.9rem; margin-top: 0.5rem; color: #DC143C;'>🌾 ออกแบบด้วยหัวใจคนอีสาน 🌾</p>
</div>
""", unsafe_allow_html=True)

# Additional info in expander
with st.expander("ℹ️ เกี่ยวกับ AI Text Summarizer"):
    st.markdown("""
    ### 🤖 เทคโนโลยี
    - **Backend**: FastAPI (Python)
    - **Frontend**: Streamlit
    - **AI Model**: BART (facebook/bart-large-cnn)
    - **ML Library**: Hugging Face Transformers
    
    ### ✨ คุณสมบัติ
    - สรุปข้อความภาษาอังกฤษอัตโนมัติ
    - ปรับความยาวสรุปได้ตามต้องการ
    - แสดงสถิติการบีบอัดข้อมูล
    - ใช้งานง่าย รวดเร็ว
    
    ### 📝 วิธีใช้งาน
    รัน uv run python run.py เพื่อเริ่ม server แล้วเปิดเว็บนี้ จากนั้น:
    1. วางข้อความที่ต้องการสรุป
    2. ตั้งค่าความยาวตามต้องการ
    3. กดปุ่ม "สรุปข้อความ"
    
    ### ⚠️ ข้อจำกัด
    - :red[**รองรับข้อความภาษาอังกฤษเท่านั้น**] (Model limitation)
    - การสรุปครั้งแรกอาจใช้เวลานานเพราะต้องโหลดโมเดล
    - คุณภาพของสรุปขึ้นอยู่กับข้อความต้นฉบับ
    """)

# Keyboard shortcut hint
st.markdown("""
<div style='position: fixed; bottom: 10px; right: 10px; 
     background: linear-gradient(135deg, #DC143C, #B22222); 
     padding: 12px 18px; border-radius: 15px; font-size: 0.9rem; 
     color: #FFD700; border: 2px solid #FFD700; box-shadow: 0 4px 15px rgba(220,20,60,0.4);
     font-weight: 700;'>
    💡 เคล็ดลับ: กด R เพื่อรีโหลดหน้าเว็บ
</div>
""", unsafe_allow_html=True)
