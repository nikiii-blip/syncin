import streamlit as st
from groq import Groq

# --- SYNCIN PREMIUM SETUP ---
st.set_page_config(page_title="SyncIn | Sync-IN your Career", page_icon="🔗", layout="centered")

# Custom CSS for the "Silicon Valley" Aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #000000;
        color: #E2E8F0;
    }
    
    .stApp { background-color: #000000; }
    
    h1 {
        font-weight: 800;
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        letter-spacing: -2px;
    }

    .stButton>button {
        background: #111;
        color: #00FF9D;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        transition: 0.3s;
        width: 100%;
    }

    .stButton>button:hover {
        border-color: #00FF9D;
        box-shadow: 0px 0px 20px rgba(0, 255, 157, 0.4);
        background: #00FF9D;
        color: black;
    }

    .card {
        background: #0A0A0A;
        padding: 30px;
        border-radius: 24px;
        border: 1px solid #1A1A1A;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    input, textarea { 
        background-color: #0A0A0A !important; 
        border: 1px solid #333 !important; 
        color: white !important; 
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if 'flow' not in st.session_state:
    st.session_state.flow = 'start'

# --- START PAGE ---
if st.session_state.flow == 'start':
    st.title("🔗 SyncIn")
    st.markdown("### Hey buddy, do you know what you want to be?")
    st.write("The first step to syncing your future is knowing the destination.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("YES, I KNOW 🎯"):
            st.session_state.flow = 'yes'
            st.rerun()
    with col2:
        if st.button("NO, NOT YET 🤔"):
            st.session_state.flow = 'no'
            st.rerun()

# --- NO BRANCH: EMOTIONAL SUPPORT ---
elif st.session_state.flow == 'no':
    st.title("🔗 SyncIn")
    st.markdown("## Please don't be sad. It's a long journey! 🌊")
    st.write("Exploration is part of the process. We are building **Career Games** to help you discover your strengths through play.")
    st.write("---")
    email = st.text_input("Leave your email, and we'll sync up when the games are ready:", placeholder="buddy@example.com")
    if st.button("Notify Me"):
        if email:
            st.success("All the best, bud! We'll reach out soon.")
        else:
            st.error("Please enter a valid email.")
    if st.button("← Back"):
        st.session_state.flow = 'start'
        st.rerun()

# --- YES BRANCH: THE AI ENGINE ---
elif st.session_state.flow == 'yes':
    st.title("🔗 SyncIn")
    st.write("### Let's Re-Engineer your path. ⚡")
    
    api_key = st.text_input("Enter Groq API Key", type="password")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            goal = st.text_input("Dream Role", placeholder="e.g. VC Founder, AI Dev")
            past = st.text_input("Current Education", placeholder="e.g. B.Com 2nd Year")
        with c2:
            budget = st.text_input("Budget (INR)", placeholder="e.g. ₹0 or ₹5000")
            time_val = st.slider("Daily Hours for Study", 1, 15, 4)
        
        skills = st.text_area("Skills you already have")
        passion = st.text_input("What truly excites you?")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SYNC MY FUTURE 🚀"):
        if not api_key:
            st.error("Please provide your API key to start the engine.")
        elif not goal:
            st.error("Tell us your dream role first!")
        else:
            try:
                client = Groq(api_key=api_key)
                # THE UPDATED MODEL NAME: llama-3.3-70b-versatile
                prompt = f"""
                Identify as 'SyncIn Career Strategist'. 
                Goal: {goal}. Education: {past}. Skills: {skills}. Budget: {budget}. Time: {time_val} hrs/day.
                
                Provide:
                1. Reality Check (Is this mathematically possible?)
                2. Phase-wise Roadmap (The most efficient path)
                3. Top Resources (Specific free YouTube/Cheap courses)
                4. Visual Flowchart Description (A clear 4-step logic flow)
                5. LinkedIn Mentors: Titles of people to search for on LinkedIn.
                """
                with st.spinner("Syncing with the future..."):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### 🗺️ Your Strategic Blueprint")
                    st.markdown(chat.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Sync failed: {e}")

    if st.button("← Back"):
        st.session_state.flow = 'start'
        st.rerun()

st.markdown("<br><center><small>SyncIn v2.1 | Premium Edition | 2026</small></center>", unsafe_allow_html=True)
