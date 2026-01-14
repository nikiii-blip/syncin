import streamlit as st
from groq import Groq

# --- SYNCIN ELITE CONFIG ---
st.set_page_config(page_title="SyncIn", page_icon="🔗", layout="wide")

# CUSTOM CSS: Centering, Slider Colors, and Minimalist Spacing
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
        color: #FFFFFF;
    }

    /* Centering the Start Page */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 70vh;
        text-align: center;
    }

    h1 {
        font-weight: 900;
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem !important;
        margin-bottom: 0px;
    }

    /* Fix Slider Color */
    div[data-baseweb="slider"] > div > div { background: #00FF9D !important; }
    div[role="slider"] { background-color: #00FF9D !important; border: 2px solid #00FF9D !important; }

    /* Premium Card Look */
    .sync-card {
        background: #0D0D0D;
        padding: 40px;
        border-radius: 28px;
        border: 1px solid #1A1A1A;
        margin-top: -20px;
    }

    /* Remove huge block under API input */
    .stTextInput { margin-bottom: -15px !important; }

    .stButton>button {
        background: transparent;
        color: #00FF9D;
        border: 1px solid #00FF9D;
        border-radius: 50px;
        padding: 10px 40px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: #00FF9D;
        color: #000;
    }
    </style>
    """, unsafe_allow_html=True)

if 'flow' not in st.session_state:
    st.session_state.flow = 'start'

# --- START PAGE (NOW CENTERED) ---
if st.session_state.flow == 'start':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.write("### Hey buddy, do you know what you want to be?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("YES"):
            st.session_state.flow = 'yes'
            st.rerun()
        if st.button("NO"):
            st.session_state.flow = 'no'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- NO BRANCH ---
elif st.session_state.flow == 'no':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.write("## Don't sweat it. It's a journey.")
    st.write("We are building **Career Games** to help you find your spark.")
    email = st.text_input("Drop your email to get early access:")
    if st.button("NOTIFY ME"):
        st.success("We got you, bud!")
    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- YES BRANCH (THE DASHBOARD) ---
elif st.session_state.flow == 'yes':
    st.markdown("<h2 style='text-align: center; color: #00FF9D;'>STRATEGIC RE-ENGINEERING</h2>", unsafe_allow_html=True)
    
    # API Key - Minimalist
    api_key = st.text_input("🔑 API ACCESS KEY", type="password")
    
    st.markdown('<div class="sync-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        goal = st.text_input("TARGET ROLE", placeholder="e.g. Associate Product Manager")
        past = st.text_input("CURRENT BACKGROUND", placeholder="e.g. 4th Year BMS Student")
        budget = st.text_input("BUDGET (INR)", value="0")
    with c2:
        months = st.number_input("TIMELINE (MONTHS)", 1, 120, 12)
        time_val = st.slider("AVAILABLE HRS/DAY", 1, 15, 5)
        passion = st.text_input("WHAT EXCITES YOU?")

    if st.button("RUN SYNC-ENGINE"):
        if not api_key:
            st.error("Missing API Key.")
        else:
            try:
                client = Groq(api_key=api_key)
                # HARDCORE STRATEGIST PROMPT
                prompt = f"""
                You are 'SyncIn Strategic Engine'. You are a blunt, elite career architect. 
                User is a {past} wanting to be {goal} in {months} months.
                
                CRITICAL RULES:
                1. If a student wants a 'Manager' role at a Top Tech firm (Google/Oracle), explain that they lack the 'Years of Experience' (YOE). Pivot them to 'Associate' or 'Entry Level' roles.
                2. Use the 'Reality Check' to be honest. If it's impossible, say so.
                3. Do NOT use more than 2 emojis.
                
                Response Structure:
                - **GATEKEEPER ANALYSIS**: Why this role is/isn't realistic for a student.
                - **THE MATH**: Hours required vs available.
                - **THE REVERSE PATH**: What to do in Month {months}, then Month {months//2}, then Month 1.
                - **SYNC-FLOW**: [Current] >> [Skill] >> [Proof of Work] >> [Target].
                - **LINKEDIN SEARCH**: Exact strings to find alumni.
                """
                with st.spinner("SYNCING..."):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown("### SYNCIN BLUEPRINT")
                    st.markdown(chat.choices[0].message.content)
            except Exception as e:
                st.error(f"Engine Failure: {e}")
    
    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
