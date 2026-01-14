   import streamlit as st
from groq import Groq

# --- SYNCIN ELITE CONFIG ---
st.set_page_config(page_title="SyncIn | Career OS", page_icon="🔗", layout="wide")

# CUSTOM CSS: Premium Branding + Thick Slider Fix
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
        justify-content: center; height: 75vh; text-align: center;
    }

    h1 {
        font-weight: 900;
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 5rem !important; letter-spacing: -4px;
        margin-bottom: 0px;
    }

    /* THE SLIDER FIX: Making the bar thick and emerald */
    div[data-baseweb="slider"] {
        padding-top: 25px;
        padding-bottom: 25px;
    }
    div[data-baseweb="slider"] > div {
        height: 8px !important; /* Thickens the bar */
        background-color: #1A1A1A !important;
    }
    /* The part of the bar that is "filled" */
    div[data-baseweb="slider"] > div > div > div {
        background-color: #00FF9D !important;
    }
    /* The actual slider knob/dot */
    div[role="slider"] {
        background-color: #00FF9D !important;
        border: 2px solid #00FF9D !important;
        height: 20px !important;
        width: 20px !important;
    }

    /* Premium Form Card */
    .sync-card {
        background: #0A0A0A; padding: 40px; border-radius: 30px;
        border: 1px solid #1A1A1A; margin-top: 10px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    .stButton>button {
        background: transparent; color: #00FF9D; border: 1px solid #00FF9D;
        border-radius: 8px; padding: 12px 40px; font-weight: 700;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover { background: #00FF9D; color: #000; box-shadow: 0 0 20px rgba(0, 255, 157, 0.4); }

    /* Report Box Styling */
    .report-output {
        background: #0D0D0D; padding: 30px; border-radius: 15px;
        border-left: 5px solid #00FF9D; line-height: 1.7;
    }
    </style>
    """, unsafe_allow_html=True)

if 'flow' not in st.session_state:
    st.session_state.flow = 'start'

# --- START PAGE ---
if st.session_state.flow == 'start':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.markdown("<p style='font-size: 1.5rem; opacity: 0.6;'>Reverse-Engineering the Future of Work.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("YES, ACCESS SYSTEM"):
            st.session_state.flow = 'yes'
            st.rerun()
        if st.button("NO, NOT YET"):
            st.session_state.flow = 'no'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- NO BRANCH ---
elif st.session_state.flow == 'no':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.title("🔗 SyncIn")
    st.write("### Exploration is a strategic phase.")
    st.write("Join the waitlist for **SyncIn Career Games** (Launch Q1 2026).")
    email = st.text_input("Professional Email:", placeholder="you@company.com")
    if st.button("SYNC ME IN"):
        st.success("Priority Access Granted.")
    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- YES BRANCH (THE DEEP ANALYTICS) ---
elif st.session_state.flow == 'yes':
    st.markdown("<h2 style='color: #00FF9D; font-weight: 800; text-align: center;'>STRATEGIC BLUEPRINT ENGINE</h2>", unsafe_allow_html=True)
    
    api_key = st.text_input("🔑 GROQ API KEY", type="password")
    
    st.markdown('<div class="sync-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        goal = st.text_input("TARGET DESTINATION", placeholder="e.g. Marketing Manager @ Oracle")
        past = st.text_input("CURRENT BASELINE", placeholder="e.g. BMS Graduate, Fresh")
        budget = st.text_input("FINANCIAL BUDGET (INR)", value="0")
    with c2:
        months = st.number_input("SYNC TIMELINE (MONTHS)", 1, 60, 12)
        time_val = st.slider("DAILY BANDWIDTH (HOURS)", 1, 15, 5)
        passion = st.text_input("DOMAIN VERTICAL", placeholder="e.g. Cloud, Fintech")

    if st.button("RE-ENGINEER CAREER PATH"):
        if not api_key:
            st.error("Engine requires an API key for live market computation.")
        elif len(goal) < 4 or goal.lower() in ["groot", "bdbbdjs", "asdf"]:
            st.error("Input Validation Error: Please provide a valid professional role.")
        else:
            try:
                client = Groq(api_key=api_key)
                # THE DEEP DATA PROMPT
                prompt = f"""
                You are a Lead Strategy Consultant at a Top-Tier Career Firm.
                Profile: {past} targeting {goal} within {months} months on a budget of {budget}.
                
                Generate a data-heavy report using Markdown tables.
                1. **FEASIBILITY ANALYSIS**: Compare 'Industry Standard Experience' vs 'User Baseline'.
                2. **COMPETENCY MATRIX**: A table with Skill, Gap %, and Hours to Bridge.
                3. **REVERSE QUARTERLY SPRINT**: Precise milestones from Month {months} back to Month 1.
                4. **HACKING THE SYSTEM**: One specific 'Proof of Work' project and one LinkedIn Boolean string.
                5. **VERDICT**: Be blunt. If {goal} usually requires 5 years and the user has 12 months, explain the 'Associate' pivot.
                """
                with st.spinner("Analyzing high-fidelity hiring data..."):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown("<div class='report-output'>", unsafe_allow_html=True)
                    st.markdown(chat.choices[0].message.content)
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Computation failure: {e}")
    
    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
