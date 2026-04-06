import streamlit as st
import os
import base64
import requests

# --- 1. THE STABLE ENGINE (GEMINI 1.5 FLASH) ---
# This key and model are set for maximum stability to avoid 403 errors.
API_KEY = "AIzaSyD-lFSiJA98bpXrHxWuyCildY8hdDnupMI"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- 2. THE DESIGN ENGINE (INSTAGRAM VIBE) ---
st.set_page_config(page_title="EduGenie", layout="centered")
img_base64 = get_base64("ocean.jpg") or get_base64("ocean.png")

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
    }}
    /* INSTAGRAM PROFILE BOX */
    .ig-profile {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 1px solid #ffffff33;
    }}
    .ig-stats {{
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        font-weight: bold;
    }}
    /* ROLE TAGS */
    .tag-admin {{ background: #ff4b4b; padding: 2px 8px; border-radius: 5px; font-size: 12px; }}
    .tag-rep {{ background: #00d4ff; padding: 2px 8px; border-radius: 5px; font-size: 12px; }}
    .tag-student {{ background: #444; padding: 2px 8px; border-radius: 5px; font-size: 12px; }}
    
    button[data-baseweb="tab"] p {{ font-size: 20px !important; font-weight: bold !important; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. GLOBAL STATE MANAGEMENT ---
if "user_role" not in st.session_state:
    st.session_state.user_role = "Student"
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_79"
if "group_chats" not in st.session_state:
    st.session_state.group_chats = {
        "Public Lounge (Open)": [{"id": "@Staff_HOD", "role": "Admin", "msg": "Welcome everyone!"}],
        "ML Private Group": [{"id": "@Prof_Raj", "role": "Admin", "msg": "Only for ML students."}],
        "Rep Council": [{"id": "@Class_Rep", "role": "Representative", "msg": "Meeting at 4pm."}]
    }

# --- 4. APP NAVIGATION ---
st.title("🧞 EduGenie")
tab1, tab2, tab3 = st.tabs(["💬 Groups", "🪄 AI Genie", "👤 Profile"])

with tab1:
    st.subheader("Classroom Hub")
    
    # ACCESSIBLE CONTROL (SIDEBAR)
    st.sidebar.title("🔐 Access Control")
    selected_group = st.sidebar.selectbox("Choose Group:", list(st.session_state.group_chats.keys()))
    
    # Logic: Who can access?
    can_access = True
    if "Private" in selected_group and st.session_state.user_role == "Student":
        can_access = False
        st.error("🚫 Access Denied: This group is for Admins and Representatives only.")
    
    if can_access:
        st.write(f"Logged in as: **{st.session_state.user_id}** ({st.session_state.user_role})")
        for chat in st.session_state.group_chats[selected_group]:
            role_class = f"tag-{chat['role'].lower()}"
            st.markdown(f"<span class='{role_class}'>{chat['role']}</span> **{chat['id']}**: {chat['msg']}", unsafe_allow_html=True)

        if prompt := st.chat_input("Message..."):
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
                # Direct JSON payload for maximum stability
                payload = {"contents": [{"parts": [{"text": user_query}]}]}
                res = requests.post(URL, json=payload, timeout=15)
                if res.status_code == 200:
                    st.write(res.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Error {res.status_code}: Please refresh the page.")
            except:
                st.error("Check connection.")

with tab3:
    # INSTAGRAM STYLE PROFILE
    st.markdown('<div class="ig-profile">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Change Photo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=120)
    else:
        st.write("📸")
    
    st.session_state.user_id = st.text_input("Username", value=st.session_state.user_id)
    
    # ROLE SELECTOR (FOR THE USER)
    st.session_state.user_role = st.selectbox("Account Type", ["Student", "Representative", "Admin"])
    
    st.markdown(f"""
        <div class="ig-stats">
            <div>12<br><span style="font-size:12px; color:gray;">Courses</span></div>
            <div>450<br><span style="font-size:12px; color:gray;">Points</span></div>
            <div>{st.session_state.user_role}<br><span style="font-size:12px; color:gray;">Rank</span></div>
        </div>
        <button style="width:100%; border-radius:5px; border:none; padding:5px;">Edit Profile</button>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
