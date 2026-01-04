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
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1F77B4;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
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
st.markdown('<p class="main-header">📝 AI Text Summarizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">สรุปข้อความยาวๆ ให้สั้นและกระชับด้วย AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ การตั้งค่า")
    
    # API Status
    api_status = check_api_health()
    if api_status:
        st.success("✅ API พร้อมใช้งาน")
    else:
        st.error("❌ API ไม่พร้อมใช้งาน")
        st.info("💡 รัน API server:\n```bash\nuv run uvicorn main:app --reload\n```")
    
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
    st.subheader("📄 ข้อความต้นฉบับ")
    
    # Load example if selected
    default_text = ""
    if selected_example and selected_example != "ไม่เลือก":
        default_text = example_texts[selected_example]
    
    input_text = st.text_area(
        "พิมพ์หรือวางข้อความที่ต้องการสรุป",
        value=default_text,
        height=300,
        placeholder="วางข้อความภาษาอังกฤษที่ต้องการสรุปที่นี่...",
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
    st.subheader("✨ ข้อความสรุป")
    
    # Summary result area
    summary_placeholder = st.empty()
    
    if summarize_btn:
        if not input_text or len(input_text) < 10:
            st.warning("⚠️ กรุณากรอกข้อความอย่างน้อย 10 ตัวอักษร")
        else:
            with st.spinner("🤖 กำลังสรุปข้อความ... (อาจใช้เวลาสักครู่ในครั้งแรก)"):
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
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🚀 Powered by FastAPI + Hugging Face Transformers (BART Model)</p>
    <p>📚 Model: facebook/bart-large-cnn | 🔧 Framework: Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Additional info in expander
with st.expander("ℹ️ เกี่ยวกับ AI Text Summarizer"):
    st.markdown("""
    ### 🤖 เทคโนโลジี
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
    1. เริ่ม API server: `uv run uvicorn main:app --reload`
    2. เริ่ม Frontend: `uv run streamlit run frontend.py`
    3. วางข้อความที่ต้องการสรุป
    4. ตั้งค่าความยาวตามต้องการ
    5. กดปุ่ม "สรุปข้อความ"
    
    ### ⚠️ ข้อจำกัด
    - รองรับข้อความภาษาอังกฤษเท่านั้น (model limitation)
    - การสรุปครั้งแรกอาจใช้เวลานานเพราะต้องโหลดโมเดล
    - คุณภาพของสรุปขึ้นอยู่กับข้อความต้นฉบับ
    """)

# Keyboard shortcut hint
st.markdown("""
<div style='position: fixed; bottom: 10px; right: 10px; background: rgba(240, 242, 246, 0.9); 
     padding: 10px; border-radius: 5px; font-size: 0.8rem; color: #666;'>
    💡 Tip: กด Ctrl+Enter เพื่อรันโค้ดอีกครั้ง
</div>
""", unsafe_allow_html=True)
