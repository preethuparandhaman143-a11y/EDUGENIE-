import streamlit as st
import os
import base64
import requests

# --- 1. THE BRAIN SETUP ---
API_KEY = "AIzaSyAeR71bgrPCMTdHl8PHPSeXRrK1RRYfXWY"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

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
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    button[data-baseweb="tab"] p {{ font-size: 26px !important; font-weight: bold !important; color: #00d4ff !important; }}
    h1, h3, p, label {{ color: white !important; }}
    .profile-card {{
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #00d4ff;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE APP UI ---
st.title("🧞 EduGenie")
st.write("Welcome dude!")

tab1, tab2, tab3 = st.tabs(["💬 Chat", "🪄 AI Genie", "👤 Profile"])

with tab1:
    with tab1:
    st.subheader("💬 Classroom Hub")
    
    # 1. Create a Sidebar for Groups
    st.sidebar.title("🏫 My Groups")
    group_choice = st.sidebar.radio("Select a Class:", ["AI & DS Batch", "ML Seminar Group", "3R Project Team"])
    
    # 2. Initialize Memory for Groups
    if "group_chats" not in st.session_state:
        st.session_state.group_chats = {
            "AI & DS Batch": [{"id": "@Staff_HOD", "msg": "Welcome to the official AI batch group!"}],
            "ML Seminar Group": [{"id": "@Staff_ML", "msg": "Notes for Unit 2 are pinned."}],
            "3R Project Team": [{"id": "@System", "msg": "Group created for 3R Seminar."}]
        }

    st.info(f"Currently viewing: **{group_choice}**")

    # 3. Display Chat for the Selected Group
    for chat in st.session_state.group_chats[group_choice]:
        # Using IDs instead of names
        st.markdown(f"**{chat['id']}**: {chat['msg']}")

    # 4. Input with Your Unique ID
    # This pulls the ID you set in the Profile Tab!
    current_user_id = st.session_state.get('user_id', "@User_Genie")
    
    if prompt := st.chat_input(f"Chatting as {current_user_id}..."):
        # Add message to the specific group memory
        st.session_state.group_chats[group_choice].append({
            "id": current_user_id, 
            "msg": prompt
        })
        st.rerun()

with tab2:
    st.subheader("🪄 Ask Your AI Genie")
    user_query = st.text_input("Ask me anything (Thanglish is okay!):", key="genie_input")
    
    if user_query:
        with st.spinner("Genie is thinking..."):
            payload = {"contents": [{"parts": [{"text": user_query}]}]}
            try:
                response = requests.post(URL, json=payload, timeout=15)
                if response.status_code == 200:
                    st.markdown("### 🧞 Genie says:")
                    st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Genie's door is stuck (Error {response.status_code}).")
            except:
                st.error("Connection error! Check your internet.")

with tab3:
    st.subheader("👤 Academic Dashboard")
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Change Profile Photo", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, width=150)
    user_id = st.text_input("Edit Unique ID / Name", value="@User_Genie")
    st.write(f"**Current User:** {user_id}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.button("📁 Module 1: ML", use_container_width=True)
        st.button("📁 Module 2: DBMS", use_container_width=True)
    with col2:
        st.button("📁 Module 3: OS", use_container_width=True)
        st.button("📁 Module 4: Networks", use_container_width=True)
