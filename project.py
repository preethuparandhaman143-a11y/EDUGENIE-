import streamlit as st
import os
import base64
import requests

# --- 1. THE STABLE ENGINE ---
API_KEY = "AIzaSyD-lFSiJA98bpXrHxWuyCildY8hdDnupMI"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- 2. STYLE ENGINE ---
st.set_page_config(page_title="EduGenie", layout="centered")
img_base64 = get_base64("ocean.jpg") or get_base64("ocean.png")

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
    }}
    .ig-profile {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid #ffffff33;
    }}
    .tag-admin {{ background: #ff4b4b; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: white; }}
    .tag-representative {{ background: #00d4ff; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: white; }}
    .tag-student {{ background: #666; padding: 2px 8px; border-radius: 5px; font-size: 11px; color: white; }}
    button[data-baseweb="tab"] p {{ font-size: 18px !important; font-weight: bold !important; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. STABLE STATE MANAGEMENT ---
if "user_role" not in st.session_state:
    st.session_state.user_role = "Student"
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_79"
if "group_chats" not in st.session_state:
    st.session_state.group_chats = {
        "Public Lounge (Open)": [{"id": "@Staff_HOD", "role": "Admin", "msg": "Welcome everyone!"}],
        "ML Private Group": [{"id": "@Prof_Raj", "role": "Admin", "msg": "Only for ML staff."}],
        "Rep Council": [{"id": "@Class_Rep", "role": "Representative", "msg": "Meeting at 4pm."}]
    }

# --- 4. THE UI ---
st.title("🧞 EduGenie")
tab1, tab2, tab3 = st.tabs(["💬 Groups", "🪄 AI Genie", "👤 Profile"])

with tab1:
    st.sidebar.title("🔐 Access Control")
    selected_group = st.sidebar.selectbox("Choose Group:", list(st.session_state.group_chats.keys()))
    
    can_access = True
    if "Private" in selected_group and st.session_state.user_role == "Student":
        can_access = False
        st.error("🚫 Access Denied: Admin/Rep Only.")
    
    if can_access:
        st.write(f"Logged in: **@{st.session_state.user_id}** ({st.session_state.user_role})")
        for chat in st.session_state.group_chats[selected_group]:
            # FIXED: Safe role checking to avoid KeyError
            role_name = chat.get('role', 'Student')
            st.markdown(f"<span class='tag-{role_name.lower()}'>{role_name}</span> **{chat['id']}**: {chat['msg']}", unsafe_allow_html=True)

        if prompt := st.chat_input("Type here..."):
            st.session_state.group_chats[selected_group].append({
                "id": f"@{st.session_state.user_id}",
                "role": st.session_state.user_role,
                "msg": prompt
            })
            st.rerun()

with tab2:
    st.subheader("🪄 Ask Your AI Genie")
    user_query = st.text_input("Ask me anything:", key="genie_input")
    if user_query:
        with st.spinner("Processing..."):
            try:
                payload = {"contents": [{"parts": [{"text": user_query}]}]}
                res = requests.post(URL, json=payload, timeout=15)
                if res.status_code == 200:
                    st.write(res.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error("Genie busy. Try again.")
            except:
                st.error("Connection issue.")

with tab3:
    st.markdown('<div class="ig-profile">', unsafe_allow_html=True)
    st.write("### Instagram Style Profile")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=100)
    
    st.session_state.user_id = st.text_input("Username", value=st.session_state.user_id)
    st.session_state.user_role = st.selectbox("Role", ["Student", "Representative", "Admin"])
    
    st.markdown(f"""
        <hr style='border: 0.5px solid #333'>
        <div style='display: flex; justify-content: space-around; font-weight: bold;'>
            <div>12<br><span style='font-size:10px; color:gray;'>Courses</span></div>
            <div>450<br><span style='font-size:10px; color:gray;'>Points</span></div>
            <div>{st.session_state.user_role[:3]}<br><span style='font-size:10px; color:gray;'>Rank</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
