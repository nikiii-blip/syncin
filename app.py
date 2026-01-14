import streamlit as st
from groq import Groq

# --- SYNCIN BRANDING & PREMIUM CSS ---
st.set_page_config(page_title="SyncIn | Your Career Sibling", page_icon="🔗", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
        color: #E2E8F0;
    }
    .stApp { background-color: #050505; }

    /* Perfect Centering for Start Page */
    .hero-container {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; height: 70vh; text-align: center;
    }

    h1 {
        font-weight: 900;
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 5rem !important; letter-spacing: -4px;
        margin-bottom: 0px;
    }

    /* THE SLIDER FIX: Thick & Emerald */
    div[data-baseweb="slider"] { padding: 30px 0; }
    div[data-baseweb="slider"] > div { height: 12px !important; background-color: #111 !important; border-radius: 10px; }
    div[data-baseweb="slider"] > div > div > div { background-color: #00FF9D !important; }
    div[role="slider"] {
        background-color: #00FF9D !important; border: none !important;
        height: 24px !important; width: 24px !important; box-shadow: 0 0 10px #00FF9D;
    }

    /* Premium Form Card */
    .sync-card {
        background: #0A0A0A; padding: 40px; border-radius: 30px;
        border: 1px solid #1A1A1A; margin-top: 5px;
    }
    
    .stTextInput, .stNumberInput, .stTextArea { margin-bottom: -15px !important; }

    .stButton>button {
        background: #00FF9D; color: #000; border: none;
        border-radius: 8px; padding: 12px 40px; font-weight: 800;
        width: 100%; transition: 0.2s;
    }
    .stButton>button:hover { background: #00cc7d; transform: translateY(-2px); }

    /* Response Box */
    .sibling-response {
        background: #0D0D0D; padding: 30px; border-radius: 20px;
        border-left: 6px solid #00FF9D; line-height: 1.6; font-size: 1.1rem;
    }

    /* Table Styling for the "Depth" look */
    table { width: 100%; border-collapse: collapse; margin-top: 20px; color: #E2E8F0; }
    th { background-color: #111; color: #00FF9D; padding: 12px; text-align: left; border-bottom: 2px solid #222; }
    td { padding: 12px; border-bottom: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

if 'flow' not in st.session_state:
    st.session_state.flow = 'start'

# --- START PAGE ---
if st.session_state.flow == 'start':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.markdown("<p style='font-size: 1.5rem; opacity: 0.6;'>Your Smart Career Sibling.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("### Hey buddy, do you know what you want to be?")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("YES, I HAVE A DREAM 🎯"):
            st.session_state.flow = 'yes'
            st.rerun()
        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        if st.button("NO, I'M LOST 🤔"):
            st.session_state.flow = 'no'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- NO BRANCH ---
elif st.session_state.flow == 'no':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.write("### It's okay to be lost. That's where discovery happens.")
    st.write("I'm building **Career Games** to help you figure it out. Drop your email.")
    email = st.text_input("Your Email:", placeholder="bud@example.com")
    if st.button("NOTIFY ME"):
        st.success("Got it. We'll find your path together.")
    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- YES BRANCH (THE SMART SIBLING ENGINE) ---
elif st.session_state.flow == 'yes':
    st.markdown("<h2 style='text-align: center; color: #00FF9D; font-weight: 800;'>CAREER RE-ENGINEERING</h2>", unsafe_allow_html=True)
    
    api_key = st.text_input("🔑 SYSTEM ACCESS KEY", type="password")
    
    st.markdown('<div class="sync-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        goal = st.text_input("WHAT'S THE DREAM?", placeholder="e.g. Marketing Manager at Google")
        past = st.text_input("YOUR BACKGROUND", placeholder="e.g. 1st Year Student")
        budget = st.text_input("BUDGET (INR)", value="0")
    with c2:
        months = st.number_input("TIMELINE (MONTHS)", 1, 60, 12)
        time_val = st.slider("HOURS YOU CAN COMMIT/DAY", 1, 15, 5)
        passion = st.text_input("WHAT EXCITES YOU?")
    
    skills = st.text_area("SKILLS YOU ALREADY HAVE")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SYNC MY FUTURE 🚀"):
        if not api_key:
            st.error("Bud, I need the API key to run the numbers.")
        elif len(goal) < 4:
            st.error("Enter a real goal. Don't waste the engine's time.")
        else:
            try:
                client = Groq(api_key=api_key)
                prompt = f"""
                Identify as 'SyncIn', the user's smart, honest older sibling. Use a tone that is encouraging but brutally realistic. 
                
                User Profile: 
                - Goal: {goal}
                - Education: {past}
                - Skills: {skills}
                - Passion: {passion}
                - Timeline: {months} Months
                - Budget: {budget}
                - Time: {time_val} hrs/day
                
                Structure the response as follows:
                1. **THE SIBLING REALITY CHECK**: Start with a blunt, metaphor-heavy paragraph. (e.g., 'Bud, you can't fly the plane the first day you see it'). Tell them if their goal is realistic or a hallucination.
                2. **THE DATA (Why Not?)**: Use a Markdown Table to show the 'Industry Standards' vs 'User Status'. Include 'Years of Experience needed' and 'Skill Gap %'.
                3. **THE SYNC-IN STRATEGY**: If the dream is too big for {months} months, tell them what goal is ACTUALLY achievable in this time. 
                4. **THE CORE FOCUS**: List 3 specific things they must master.
                5. **THE LONG-TERM SYNC**: When will the original dream ({goal}) actually be true? Give a realistic year.
                """
                with st.spinner("Analyzing the gaps..."):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown("<div class='sibling-response'>", unsafe_allow_html=True)
                    st.markdown(chat.choices[0].message.content)
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Engine Failure: {e}")

    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
