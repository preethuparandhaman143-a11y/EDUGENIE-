import streamlit as st
import os
import base64
import requests
import time

# --- 1. THE STABLE ENGINE (LOCKED VERSION) ---
# --- 1. THE STABLE ENGINE (LOCKED VERSION) ---
API_KEY = "AIzaSyBWklIysRD_7978YEYxxoFs3aVZMAflBKw"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- 2. STYLE ENGINE (BIG TABS & DESIGN) ---
st.set_page_config(page_title="EduGenie", layout="centered")
img_base64 = get_base64("ocean.jpg")

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
    }}
    .st-emotion-cache-16idsys p {{ font-size: 20px !important; color: white !important; }}
    .ig-profile {{ background: rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 20px; text-align: center; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'user_role' not in st.session_state: st.session_state.user_role = "Student"
if 'user_id' not in st.session_state: st.session_state.user_id = "user_79"
if 'group_chats' not in st.session_state:
    st.session_state.group_chats = {
        "Public Lounge (Open)": [{"role": "Admin", "msg": "Welcome to EduGenie!"}],
        "ML Private Group": [{"role": "Staff", "msg": "Notes uploaded."}]
    }

# --- 4. APP UI ---
st.title("🧞 EduGenie")
tab1, tab2, tab3 = st.tabs(["💬 Groups", "🪄 AI Genie", "👤 Profile"])

# --- TAB 1: GROUPS ---
with tab1:
    selected_group = st.selectbox("Switch Group", list(st.session_state.group_chats.keys()))
    for chat in st.session_state.group_chats[selected_group]:
        st.markdown(f"**{chat['role']}**: {chat['msg']}")
    
    if msg_input := st.chat_input("Message the group..."):
        st.session_state.group_chats[selected_group].append({"role": st.session_state.user_id, "msg": msg_input})
        st.rerun()

# --- TAB 2: AI GENIE (UPDATED) ---
with tab2:
    st.subheader("🪄 Ask Your AI Genie")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about ML, 3R, or anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
       with st.chat_message("assistant"):
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                # We move the API_KEY into the 'params' for better security/stability
                res = requests.post(
                    URL, 
                    json=payload, 
                    params={'key': API_KEY}, 
                    timeout=30
                )
                
                if res.status_code == 200:
                    answer = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Genie is sleeping. Error Code: {res.status_code}")
            except Exception as e:
                st.error("Connection timeout. Try again.")

# --- TAB 3: PROFILE ---
with tab3:
    st.markdown(f"""
    <div class="ig-profile">
        <img src="https://via.placeholder.com/100" style="border-radius:50%">
        <h2>{st.session_state.user_id}</h2>
        <p>Anna University | AI & DS</p>
        <hr>
        <p>Rank: #42 | Points: 1250</p>
    </div>
    """, unsafe_allow_html=True)
    
    new_name = st.text_input("Change Username", value=st.session_state.user_id)
    if st.button("Update Profile"):
        st.session_state.user_id = new_name
        st.rerun()
