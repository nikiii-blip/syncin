import streamlit as st
from groq import Groq

# --- SYNCIN ELITE CONFIG ---
st.set_page_config(page_title="SyncIn", page_icon="🔗", layout="centered")

# CSS for Zero Gaps, Thick Slider, and Centered UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    
    /* Overall Background & Font */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #000000;
        color: #FFFFFF;
    }
    .stApp { background-color: #000000; }

    /* Centering and Gap Removal */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
        max-width: 700px !important;
    }

    /* Hero Section Centering */
    .hero {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; height: 60vh; text-align: center;
        margin: 0px; padding: 0px;
    }

    h1 {
        font-weight: 900;
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important; letter-spacing: -3px;
        margin-bottom: -10px !important;
    }

    /* THE SLIDER FIX: Removing Gaps & Coloring */
    div[data-baseweb="slider"] {
        margin-top: -20px !important; /* Forces slider up */
        margin-bottom: -10px !important;
    }
    div[data-baseweb="slider"] > div { 
        height: 8px !important; background-color: #1A1A1A !important; 
    }
    div[data-baseweb="slider"] > div > div > div { background-color: #00FF9D !important; }
    div[role="slider"] {
        background-color: #00FF9D !important; border: none !important;
        height: 20px !important; width: 20px !important;
    }

    /* Input Card */
    .sync-card {
        background: #0A0A0A; padding: 25px; border-radius: 20px;
        border: 1px solid #1A1A1A; margin-top: 0px;
    }

    /* Button Styling */
    .stButton>button {
        background: #00FF9D; color: #000; border-radius: 8px;
        font-weight: 700; width: 100%; border: none; padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #00cc7d; transform: scale(1.02); }

    /* Response Box */
    .response-box {
        background: #0D0D0D; padding: 20px; border-radius: 15px;
        border-left: 5px solid #00FF9D; margin-top: 15px;
    }

    /* Table Depth */
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { color: #00FF9D; text-align: left; border-bottom: 2px solid #222; padding: 10px; }
    td { padding: 10px; border-bottom: 1px solid #111; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

if 'flow' not in st.session_state:
    st.session_state.flow = 'start'

# --- START PAGE ---
if st.session_state.flow == 'start':
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.write("### Your Smart Sibling.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("YES"):
            st.session_state.flow = 'yes'
            st.rerun()
    with col2:
        if st.button("NO"):
            st.session_state.flow = 'no'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- NO BRANCH ---
elif st.session_state.flow == 'no':
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.write("## It's okay. We'll find it together.")
    st.write("Join the waitlist for **Career Games**.")
    email = st.text_input("Your Email:")
    if st.button("NOTIFY ME"):
        st.success("Priority Access Granted.")
    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- YES BRANCH ---
elif st.session_state.flow == 'yes':
    st.markdown("<h2 style='text-align:center; color:#00FF9D;'>RE-ENGINEERING ENGINE</h2>", unsafe_allow_html=True)
    
    api_key = st.text_input("🔑 API KEY", type="password")
    
    c1, c2 = st.columns(2)
    with c1:
        goal = st.text_input("DREAM ROLE", placeholder="e.g. Oracle Manager")
        past = st.text_input("BACKGROUND", placeholder="e.g. BMS Student")
        budget = st.text_input("BUDGET (INR)", value="0")
    with c2:
        months = st.number_input("TIMELINE (MONTHS)", 1, 60, 12)
        st.write("DAILY HOURS")
        time_val = st.slider("", 1, 15, 5, label_visibility="red")
        passion = st.text_input("DOMAIN PASSION")
    
    skills = st.text_area("CURRENT SKILLS")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("let's SYNC-in"):
        if not api_key:
            st.error("Bud, API key please.")
        else:
            try:
                client = Groq(api_key=api_key)
                prompt = f"""
                Identity: Smart older sibling named SyncIn. 
                Goal: {goal}, Education: {past}, Skills: {skills}, Time: {months} months, {time_val} hrs/day.
                
                1. Reality Check: Be a brutally honest sibling. If they want to fly a plane before learning to walk, call them out.
                2. Data Table: Industry Standard vs User Status.
                3. The Pivot: What should they REALLY focus on if the dream is too big?
                4. Skills Matrix: Table with Skill, Current %, Target %.
                5. The Year: When will they actually hit the original {goal}?
                """
                with st.spinner("Processing..."):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown("<div class='response-box'>", unsafe_allow_html=True)
                    st.markdown(chat.choices[0].message.content)
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
