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
    page_title="� AI สรุปข้อความ - หนองบัวลำภู",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Nong Bua Lamphu Theme (ธีมหนองบัวลำภู)
st.markdown("""
<style>
    /* Import Thai Font */
    @import url('https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;600;700&family=Sarabun:wght@400;600;700&display=swap');
    
    /* Color Palette - หนองบัวลำภู
       Primary: #9C27B0 (ม่วงบัวหลวง)
       Secondary: #E91E63 (ชมพูบัว)  
       Accent: #4CAF50 (เขียวธรรมชาติ)
       Water: #2196F3 (น้ำเงินทะเลบัว)
       Sky: #87CEEB (ฟ้าสดใส)
       Gold: #FFD700 (ทองพระธาตุ)
       Light: #F3E5F5 (ม่วงอ่อน)
       Dark: #4A148C (ม่วงเข้ม)
    */
    
    * {
        font-family: 'Sarabun', 'Bai Jamjuree', sans-serif;
        font-size: 1rem;
    }
    
    /* Main Background - โทนฟ้าน้ำทะเลบัว */
    .stApp {
        background: linear-gradient(135deg, #E1F5FE 0%, #F3E5F5 50%, #E8EAF6 100%);
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 15px, rgba(156,39,176,0.02) 15px, rgba(156,39,176,0.02) 30px);
    }
    
    /* Header - Gradient สีบัวหลวง */
    .main-header {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(120deg, #9C27B0, #E91E63, #2196F3, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2rem 0 1rem 0;
        filter: drop-shadow(3px 3px 5px rgba(156,39,176,0.3));
        font-family: 'Bai Jamjuree', sans-serif;
        letter-spacing: 4px;
        line-height: 1.2;
    }
    
    .sub-header {
        font-size: 1.5rem !important;
        color: #6A1B9A !important;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 3px rgba(233,30,99,0.3);
    }
    
    /* Section Headers */
    h1, h2, h3 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #7B1FA2 !important;
        margin: 1.5rem 0 1rem 0 !important;
        text-shadow: 1px 1px 2px rgba(156,39,176,0.2);
    }
    
    /* Sidebar - ม่วงบัวน้ำเงินทะเล */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A148C 0%, #7B1FA2 30%, #9C27B0 100%);
        border-right: 6px solid #E91E63;
        box-shadow: 5px 0 25px rgba(156,39,176,0.4);
    }
    
    section[data-testid="stSidebar"] * {
        color: #F3E5F5 !important;
        font-size: 1rem !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFD700 !important;
        font-size: 1.4rem !important;
        border-bottom: 3px solid #E91E63;
        padding-bottom: 0.8rem;
        margin-top: 1.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    section[data-testid="stSidebar"] label {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #FCE4EC !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }
    
    /* Buttons - ม่วงชมพูบัว */
    .stButton > button {
        background: linear-gradient(135deg, #9C27B0 0%, #E91E63 100%);
        color: #FFFFFF !important;
        border: 4px solid #FFD700;
        border-radius: 20px;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(156,39,176,0.4);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #E91E63 0%, #FF4081 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(233,30,99,0.6);
        border-color: #4CAF50;
    }
    
    /* Text Areas - พื้นขาวม่วงอ่อน */
    .stTextArea textarea {
        border: 4px solid #9C27B0 !important;
        border-radius: 20px !important;
        background: #FEFEFE !important;
        font-size: 1rem !important;
        color: #4A148C !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
        box-shadow: inset 0 2px 8px rgba(156,39,176,0.1);
    }
    
    .stTextArea textarea:focus {
        border-color: #E91E63 !important;
        box-shadow: 0 0 20px rgba(233,30,99,0.5), inset 0 2px 8px rgba(156,39,176,0.1) !important;
        background: #FFFFFF !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #9C27B0 !important;
        opacity: 0.6;
        font-size: 0.95rem !important;
    }
    
    /* Labels - ม่วงเข้ม */
    label {
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #6A1B9A !important;
    }
    
    /* Metrics - สีบัวชมพู */
    div[data-testid="stMetricValue"] {
        color: #9C27B0 !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        text-shadow: 2px 2px 4px rgba(233,30,99,0.3);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #6A1B9A !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, #F3E5F5, #FCE4EC);
        padding: 0.5rem 1rem;
        border-radius: 10px;
    }
    
    /* Success - เขียวธรรมชาติ */
    .stSuccess {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%) !important;
        border: 3px solid #4CAF50 !important;
        border-left: 8px solid #388E3C !important;
        border-radius: 15px;
        padding: 1rem !important;
        color: #1B5E20 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(76,175,80,0.2);
    }
    
    /* Info - ฟ้าน้ำเงินทะเลบัว */
    .stInfo {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%) !important;
        border: 3px solid #2196F3 !important;
        border-left: 8px solid #1976D2 !important;
        border-radius: 15px;
        padding: 1rem !important;
        color: #0D47A1 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(33,150,243,0.2);
    }
    
    /* Warning - ทองพระธาตุ */
    .stWarning {
        background: linear-gradient(135deg, #FFF9C4 0%, #FFE082 100%) !important;
        border: 3px solid #FFD700 !important;
        border-left: 8px solid #FFA000 !important;
        border-radius: 15px;
        padding: 1rem !important;
        color: #E65100 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(255,215,0,0.2);
    }
    
    /* Error - ชมพูแดงบัว */
    .stError {
        background: linear-gradient(135deg, #FCE4EC 0%, #F8BBD0 100%) !important;
        border: 3px solid #E91E63 !important;
        border-left: 8px solid #C2185B !important;
        border-radius: 15px;
        padding: 1rem !important;
        color: #880E4F !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(233,30,99,0.2);
    }
    
    /* Dividers - ไล่สีบัวทะเลฟ้า */
    hr {
        border: none;
        height: 5px;
        background: linear-gradient(90deg, #9C27B0, #E91E63, #2196F3, #4CAF50, #FFD700);
        margin: 2.5rem 0;
        border-radius: 3px;
        box-shadow: 0 2px 5px rgba(156,39,176,0.3);
    }
    
    /* Sliders - ม่วงบัว */
    .stSlider > div > div > div {
        background: #9C27B0 !important;
    }
    
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #6A1B9A !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
    }
    
    /* Expander - ม่วงชมพูบัว */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #7B1FA2, #9C27B0) !important;
        color: #FFD700 !important;
        border-radius: 15px 15px 0 0;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 1rem !important;
        border: 4px solid #E91E63;
        border-bottom: none;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, #FEFEFE, #F3E5F5);
        border: 4px solid #E91E63;
        border-top: 2px solid #BA68C8;
        border-radius: 0 0 15px 15px;
        padding: 1.2rem;
        color: #4A148C !important;
        font-size: 1rem !important;
        line-height: 1.8;
        box-shadow: inset 0 2px 10px rgba(156,39,176,0.05);
    }
    
    /* Decorative Border Pattern - ลายบัว */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 14px;
        background: repeating-linear-gradient(
            90deg,
            #9C27B0 0px,
            #9C27B0 30px,
            #E91E63 30px,
            #E91E63 60px,
            #2196F3 60px,
            #2196F3 90px,
            #4CAF50 90px,
            #4CAF50 120px
        );
        z-index: 999;
        box-shadow: 0 3px 10px rgba(156,39,176,0.4);
    }
    
    /* Selectbox  */
    .stSelectbox > div > div {
        background: #0F000F !important;
        border: 4px solid #2196F3 !important;
        border-radius: 15px;
        font-size: 1.1rem !important;
        color: #0D47A1 !important;
        font-weight: 800 !important;
        box-shadow: 0 3px 12px rgba(33,150,243,0.3);
        padding: 0.75rem 1.2rem !important;
        min-height: 3.5rem !important;
        line-height: normal !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .stSelectbox > div > div > div {
        color: #0D47A1 !important;
        font-weight: 800 !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #E91E63 !important;
        background: linear-gradient(135deg, #000, #FCE4EC) !important;
        box-shadow: 0 5px 18px rgba(233,30,99,0.5);
        transform: scale(1.02);
        transition: all 0.3s ease;
    }
    
    /* Caption Text */
    .caption, [data-testid="stCaptionContainer"] {
        color: #FFFFFF !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, #E91E63, #9C27B0) !important;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        display: inline-block;
        border: 3px solid #E91E63;
        box-shadow: 0 4px 12px rgba(233,30,99,0.5);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    
    /* Code Blocks - พื้นม่วงเข้มข้อความทอง */
    code {
        background: #4A148C !important;
        color: #FFD700 !important;
        font-size: 0.95rem !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 8px;
        border: 2px solid #E91E63;
    }
    
    pre {
        background: #4A148C !important;
        border: 4px solid #9C27B0 !important;
        border-radius: 12px;
        padding: 1rem !important;
    }
    
    pre code {
        color: #FFD700 !important;
        font-size: 0.95rem !important;
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
st.markdown('<p class="main-header">🌸 AI สรุปข้อความ 🌸</p>', unsafe_allow_html=True)
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
        "🌸 Red Lotus Sea": """The Red Lotus Sea, or Talay Bua Daeng, is a stunning natural phenomenon in Nong Han Lake, Udon Thani province near Nong Bua Lamphu. Every year from December to February, millions of pink lotus flowers bloom across the lake, creating a breathtaking carpet of color that stretches as far as the eye can see. This spectacular sight has become one of Thailand's most photographed natural wonders, attracting tourists from around the world. Visitors can take boat rides through the lotus fields in the early morning when the flowers are in full bloom. The best time to visit is between 6-11 AM when the lotus flowers are open and the light is perfect for photography. This unique ecosystem also supports diverse wildlife and local fishing communities who have lived in harmony with nature for generations.""",
        
        "🍖 Bak Wave E3": """Bak Wave is a traditional Isaan person from Nong Bua Lamphu who represents the authentic culinary culture of northeastern Thailand. In traditional Isaan communities, dog meat consumption has been part of local cuisine for generations, though this practice has become increasingly controversial in modern times. Bak Wave's story reflects the complex relationship between cultural traditions and changing social values. The dish, known locally as 'neua maa', was historically consumed during special occasions and festivals in rural Isaan villages. However, contemporary Thai society has largely moved away from this practice due to animal welfare concerns and changing attitudes. Modern Isaan cuisine focuses on other beloved dishes like som tam papaya salad, larb minced meat salad, and sticky rice. Bak Wave's narrative illustrates how cultural practices evolve over time, as younger generations from Nong Bua Lamphu and across Isaan embrace new values while maintaining pride in other aspects of their rich cultural heritage.""",
        
        "🏞️ Nong Bua Lamphu Province": """Nong Bua Lamphu is a northeastern Thai province known for its rich cultural heritage and natural beauty. The province is famous for the spectacular red lotus sea in nearby Nong Han Lake, which blooms magnificently from December to February. Local people, known for their warm hospitality and strong Isaan traditions, maintain deep connections to their agricultural roots and cultural practices. The province is home to talented artists, musicians, and craftspeople who preserve and innovate traditional Isaan culture. Wave Isaan music has become a signature cultural export, with local musicians gaining national fame while staying true to their northeastern Thai identity. The people of Nong Bua Lamphu take pride in their unique dialect, traditional silk weaving, delicious cuisine, and vibrant festivals. The province represents the heart of Isaan culture, where ancient traditions blend seamlessly with modern aspirations, creating a dynamic community that celebrates both heritage and progress.""",
        
        "🤖 Artificial Intelligence": """Artificial Intelligence has revolutionized modern technology by enabling machines to perform tasks that typically require human intelligence. AI systems can now recognize patterns, make decisions, understand natural language, and even create art and music. Machine learning, a subset of AI, allows computers to learn from data without explicit programming. Deep learning neural networks have achieved remarkable breakthroughs in image recognition, speech processing, and autonomous vehicles. AI applications are transforming industries including healthcare, finance, education, and entertainment. Natural Language Processing enables chatbots and virtual assistants to understand and respond to human queries. Computer vision allows machines to interpret visual information from the world. Despite its incredible potential, AI also raises important ethical questions about privacy, job displacement, and decision-making accountability that society must address.""",
        
        "🌍 Space Exploration": """Space exploration represents humanity's greatest adventure into the unknown cosmos. Since the first satellite Sputnik launched in 1957, we have sent humans to the Moon, robots to Mars, and probes beyond our solar system. The International Space Station orbits Earth as a testament to international cooperation, hosting astronauts conducting vital research in microgravity. Modern space missions aim to establish permanent lunar bases, send humans to Mars, and search for signs of extraterrestrial life. Private companies like SpaceX and Blue Origin are revolutionizing space travel with reusable rockets, making access to space more affordable. The James Webb Space Telescope peers back to the universe's earliest galaxies, revealing cosmic mysteries. Future missions plan to mine asteroids for resources, build space habitats, and perhaps one day make humanity a multi-planetary species.""",
        
        "💡 Quantum Computing": """Quantum computing harnesses the bizarre principles of quantum mechanics to process information in fundamentally new ways. Unlike classical computers that use bits representing 0 or 1, quantum computers use qubits that can exist in multiple states simultaneously through superposition. This enables them to solve certain problems exponentially faster than traditional computers. Quantum entanglement allows qubits to be correlated in ways impossible for classical bits, creating powerful computational advantages. Applications include breaking current encryption methods, simulating molecular structures for drug discovery, optimizing complex logistics, and advancing artificial intelligence. Major tech companies and research institutions are racing to build practical quantum computers, though significant technical challenges remain. Maintaining quantum states requires extreme cold temperatures near absolute zero. Error correction is difficult because quantum states are fragile and easily disrupted. Despite these obstacles, quantum computing promises to revolutionize fields from cryptography to materials science."""
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
        placeholder="วางข้อความเพื่อสรุปเป็นภาษาอังกฤษที่นี่ ข้อความต้องมีความยาวอย่างน้อย 10 ตัวอักษร",
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
            with st.spinner("🤖 กำลังสรุปข้อความ... รอแป๊บเดียวเด้อ!"):
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
<div style='text-align: center; color: #6A1B9A; padding: 1.5rem; background: linear-gradient(135deg, #F3E5F5, #E1BEE7); border-radius: 15px; margin: 1rem 0; border: 3px solid #9C27B0;'>
    <p style='font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;'>🚀 ขับเคลื่อนด้วยเทคโนโลยี AI ระดับโลก</p>
    <p style='font-size: 1rem;'>📚 โมเดล: facebook/bart-large-cnn | 🔧 เฟรมเวิร์ก: FastAPI + Streamlit</p>
    <p style='font-size: 0.9rem; margin-top: 0.5rem; color: #E91E63;'>🌸 ออกแบบด้วยหัวใจคนหนองบัวลำภู - เมืองบัวหลวง 🌸</p>
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
     background: linear-gradient(135deg, #9C27B0, #7B1FA2); 
     padding: 12px 18px; border-radius: 15px; font-size: 0.9rem; 
     color: #FFD700; border: 2px solid #E91E63; box-shadow: 0 4px 15px rgba(156,39,176,0.4);
     font-weight: 700;'>
    💡 เคล็ดลับ: กด R เพื่อรีโหลดหน้าเว็บ
</div>
""", unsafe_allow_html=True)
