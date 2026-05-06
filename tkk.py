import streamlit as st
from datetime import datetime
import os

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="NextStep", layout="centered", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Prompt', sans-serif; }
    
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

    /* Glassmorphism Card */
    .main-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }

    .bubble-me {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 12px 20px; border-radius: 20px 20px 5px 20px;
        margin-left: auto; margin-bottom: 10px; max-width: 80%;
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.3);
    }

    .bubble-friend {
        background: rgba(255, 255, 255, 0.9);
        color: #2d3436; padding: 12px 20px; border-radius: 20px 20px 20px 5px;
        margin-right: auto; margin-bottom: 10px; max-width: 80%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA (8 หมวดคณะ) ---
major_categories = {
    "1. วิทยาศาสตร์ทั่วไป": ["คณะวิทยาศาสตร์"],
    "2. วิทยาศาสตร์เทคโนโลยี": ["คณะวิศวกรรมศาสตร์", "คณะเกษตรศาสตร์", "คณะสัตวแพทย์", "คณะจิตวิทยา", "คณะแอนิเมชั่น"],
    "3. วิทยาศาสตร์สุขภาพ": ["คณะแพทยศาสตร์", "คณะทันตแพทย์", "คณะเภสัชศาสตร์", "คณะพยาบาลศาสตร์", "คณะสหเวชศาสตร์", "คณะสาธารณสุข"],
    "4. บริหาร": ["คณะบัญชี/บริหาร", "คณะเศรษฐศาสตร์", "คณะโลจิสติกส์"],
    "5. ภาษาศาสตร์": ["คณะศิลปศาสตร์/อักษรศาสตร์"],
    "6. สังคม": ["คณะนิติศาสตร์", "คณะรัฐศาสตร์", "คณะโบราณคดี", "คณะนิเทศศาสตร์"],
    "7. การศึกษา": ["คณะครุศาสตร์/ศึกษาศาสตร์"],
    "8. ศิลปะ": ["คณะสถาปัตยกรรม", "คณะจิตรกรรม", "คณะมัณฑณศิลป์", "คณะศิลปกรรมศาสตร์"]
}

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'chat' not in st.session_state: st.session_state.chat = [{"n": "NextStep AI", "t": "ยินดีต้อนรับ! เข้าสู่ระบบด้วยอีเมลสำเร็จแล้ว", "me": False}]

# --- 4. APP PAGES ---

def login_page():
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=250)
    st.markdown("<h1>🚀 NextStep</h1><p>ก้าวสำคัญสู่มหาวิทยาลัยในฝัน</p></div>", unsafe_allow_html=True)
    
    with st.container():
        tab1, tab2 = st.tabs(["📧 เข้าสู่ระบบ", "📝 ลงทะเบียนใหม่"])
        
        with tab1:
            email = st.text_input("อีเมล")
            password = st.text_input("รหัสผ่าน", type="password")
            if st.button("เข้าสู่ระบบ", use_container_width=True):
                if email and password:
                    # จำลองการตรวจสอบ (ในอนาคตเชื่อม Database)
                    st.session_state.user = {"name": email.split('@')[0], "major": "วิศวกรรมศาสตร์", "cat": "2. วิทยาศาสตร์เทคโนโลยี"}
                    st.session_state.logged_in = True
                    st.rerun()
        
        with tab2:
            st.info("🛡️ ข้อมูลของคุณจะถูกเก็บเป็นความลับตามนโยบาย PDPA")
            new_email = st.text_input("อีเมลสำหรับลงทะเบียน")
            new_pass = st.text_input("ตั้งรหัสผ่าน", type="password")
            confirm_pass = st.text_input("ยืนยันรหัสผ่าน", type="password")
            
            st.divider()
            name = st.text_input("ชื่อเล่นที่ใช้ในแอป")
            cat = st.selectbox("เลือกหมวดหมู่คณะ", list(major_categories.keys()))
            major = st.selectbox("เลือกคณะเป้าหมาย", major_categories[cat])
            
            if st.button("สร้างบัญชีและเริ่มต้นใช้งาน", use_container_width=True):
                if new_email and new_pass == confirm_pass and name:
                    st.session_state.user = {"name": name, "major": major, "cat": cat}
                    st.session_state.logged_in = True
                    st.success("ลงทะเบียนสำเร็จ!")
                    st.rerun()
                elif new_pass != confirm_pass:
                    st.error("รหัสผ่านไม่ตรงกัน!")

def main_app():
    u = st.session_state.user
    with st.sidebar:
        if os.path.exists("logo.png"): st.image("logo.png")
        st.markdown(f"### 👤 {u['name']}")
        st.caption(f"เป้าหมาย: คณะ{u['major']}")
        st.divider()
        if st.button("❌ ออกจากระบบ"):
            st.session_state.logged_in = False
            st.rerun()

    # พื้นที่แชท
    st.markdown(f"<div class='main-card'><b>ห้องแชทคณะ{u['major']}</b></div>", unsafe_allow_html=True)
    st.write("")
    
    with st.container(height=400):
        for m in st.session_state.chat:
            align = "bubble-me" if m['me'] else "bubble-friend"
            st.markdown(f"<div class='{align}'><b>{m['n']}</b><br>{m['t']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        msg = st.text_input("", placeholder="ส่งข้อความ...", key="in", label_visibility="collapsed")
    with col2:
        if st.button("ส่ง", use_container_width=True) and msg:
            st.session_state.chat.append({"n": u['name'], "t": msg, "me": True})
            st.rerun()

if st.session_state.logged_in: main_app()
else: login_page()
