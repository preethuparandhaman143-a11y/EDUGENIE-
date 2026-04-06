import streamlit as st
import os
import base64
import requests
import time

# --- 1. THE STABLE ENGINE (LOCKED VERSION) ---
API_KEY = "AIzaSyD-lFSiJA98bpXrHxWuyCildY8hdDnupMI"
# Using the most globally accessible stable endpoint
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- 2. STYLE ENGINE (BIG TABS & DESIGN) ---
st.set_page_config(page_title="EduGenie", layout="centered")
img_base64 = get_base64("ocean.jpg") or get_base64("ocean.png")

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
    }}
    button[data-baseweb="tab"] p {{ 
        font-size: 24px !important; 
        font-weight: bold !important; 
        color: #00d4ff !important; 
    }}
    .ig-profile {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 1px solid #ffffff33;
        color: white;
    }}
    .ig-avatar {{
        width: 110px; height: 110px; border-radius: 50%; 
        border: 3px solid #e1306c; margin: 0 auto;
        display: flex; align-items: center; justify-content: center;
        background: rgba(255,255,255,0.1); font-size: 14px;
    }}
    .tag-admin {{ background: #ff4b4b; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: white; }}
    .tag-representative {{ background: #00d4ff; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: white; }}
    .tag-student {{ background: #555; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if "user_role" not in st.session_state: st.session_state.user_role = "Student"
if "user_id" not in st.session_state: st.session_state.user_id = "user_79"
if "group_chats" not in st.session_state:
    st.session_state.group_chats = {
        "Public Lounge (Open)": [{"id": "@Staff_HOD", "role": "Admin", "msg": "Welcome to EduGenie!"}],
        "ML Private Group": [{"id": "@Prof_Raj", "role": "Admin", "msg": "Notes uploaded."}],
        "Rep Council": [{"id": "@Class_Rep", "role": "Representative", "msg": "Meeting at 4pm."}]
    }

# --- 4. APP UI ---
st.title("🧞 EduGenie")
tab1, tab2, tab3 = st.tabs(["💬 Groups", "🪄 AI Genie", "👤 Profile"])

with tab1:
    selected_group = st.selectbox("Switch Group", list(st.session_state.group_chats.keys()))
    
    can_access = True
    if "Private" in selected_group and st.session_state.user_role == "Student":
        can_access = False
        st.error("🚫 Access Restricted to Admins & Reps")
    
    if can_access:
        st.write(f"Logged in: **@{st.session_state.user_id}**")
        for chat in st.session_state.group_chats[selected_group]:
            role = chat.get('role', 'Student')
            st.markdown(f"<span class='tag-{role.lower()}'>{role}</span> **{chat['id']}**: {chat['msg']}", unsafe_allow_html=True)

        if prompt := st.chat_input("Message..."):
            st.session_state.group_chats[selected_group].append({
                "id": f"@{st.session_state.user_id}", "role": st.session_state.user_role, "msg": prompt
            })
            st.rerun()

with tab2:
    st.subheader("🪄 Ask Your AI Genie")
    # Added clear instructions for the user
    user_query = st.text_input("Ask me anything:", placeholder="Type here and press ENTER", key="genie_box")
    
    if user_query:
        # The spinner ensures the user sees that the "Genie" is actually working
        with st.status("🧞 Genie is searching for your answer...", expanded=True) as status:
            payload = {"contents": [{"parts": [{"text": user_query}]}]}
            try:
                # Increased timeout and direct handling
                res = requests.post(URL, json=payload, timeout=30)
                if res.status_code == 200:
                    answer = res.json()['candidates'][0]['content']['parts'][0]['text']
                    status.update(label="✅ Answer Found!", state="complete", expanded=False)
                    st.markdown("### 🧞 Genie says:")
                    st.write(answer)
                else:
                    status.update(label="❌ Genie is busy. Please try again.", state="error")
            except Exception as e:
                status.update(label="❌ Connection Timeout. Try again.", state="error")

with tab3:
    st.markdown('<div class="ig-profile">', unsafe_allow_html=True)
    st.markdown('<div class="ig-avatar"><b>Add Pic</b></div>', unsafe_allow_html=True)
    st.write(f"### @{st.session_state.user_id}")
    
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        st.image(uploaded_file, width=120)
    
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.user_id = st.text_input("Username", value=st.session_state.user_id)
    with c2:
        st.session_state.user_role = st.selectbox("Role", ["Student", "Representative", "Admin"])
    
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; margin: 20px 0;'>
            <div style='text-align:center;'><b>12</b><br><small>Courses</small></div>
            <div style='text-align:center;'><b>450</b><br><small>Points</small></div>
            <div style='text-align:center;'><b>{st.session_state.user_role[:3]}</b><br><small>Rank</small></div>
        </div>
        <div style='text-align:left; font-size: 14px;'>
            <b>Preethika P</b><br>
            🎓 Anna University | AI & DS<br>
            🪄 Building EduGenie Platform
        </div>
    """, unsafe_allow_html=True)
    st.button("Edit Profile", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
