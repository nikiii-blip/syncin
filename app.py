import streamlit as st
from groq import Groq

# --- SYNCIN LIGHT MODE CONFIG ---
st.set_page_config(page_title="SyncIn", page_icon="🔗", layout="centered")

# --- CUSTOM CSS: APPLE/STRIPE AESTHETIC ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* 1. LIGHT MODE BACKGROUND */
    .stApp { 
        background-color: #FFFFFF; 
        color: #111827; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Remove top whitespace */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 850px !important;
    }

    /* 2. TYPOGRAPHY (Clean Black & Gradients) */
    h1 {
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #000000, #434343);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem !important;
        letter-spacing: -3px;
        margin-bottom: 10px !important;
        text-align: center;
    }
    
    h3 {
        color: #6B7280; /* Cool Gray */
        font-weight: 500;
        text-align: center;
        margin-bottom: 40px !important;
    }

    h2 { color: #111827; font-weight: 800; text-align: center; }

    /* 3. INPUT FIELDS (No Black Lines - Soft Grey) */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #F3F4F6 !important; /* Soft Grey Background */
        color: #111827 !important; /* Dark Text */
        border: none !important; /* REMOVED THE BLACK LINE */
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* Focus State (Subtle Blue Glow instead of Line) */
    .stTextInput input:focus, .stNumberInput input:focus {
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5) !important;
    }

    /* 4. BUTTONS (Clean Pills) */
    .stButton>button {
        background-color: #000000; /* Solid Black Button */
        color: #FFFFFF;
        border: none !important; /* REMOVED THE BLACK LINE */
        border-radius: 50px;
        padding: 15px 30px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); /* Soft Shadow */
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2563EB; /* Turns Blue on Hover */
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }

    /* 5. SLIDER (Clean Blue/Black) */
    div[data-baseweb="slider"] { padding-top: 20px; }
    div[role="slider"] { 
        background-color: #000000 !important; 
        box-shadow: 0 0 10px rgba(0,0,0,0.2); 
    }
    div[data-baseweb="slider"] > div > div > div { background-color: #2563EB !important; }

    /* 6. CARDS (Soft Shadows, No Borders) */
    .sync-card {
        background: #FFFFFF;
        padding: 40px;
        border-radius: 24px;
        border: 1px solid #F3F4F6; /* Very subtle grey border */
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.01);
        margin-top: 20px;
    }

    /* 7. RESPONSE BOX */
    .sibling-box {
        background: #F9FAFB; /* Very Light Grey */
        padding: 30px;
        border-radius: 16px;
        border-left: 5px solid #2563EB; /* Blue Accent */
        color: #374151;
        line-height: 1.6;
        margin-top: 30px;
    }
    
    /* Table Styling for Light Mode */
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th { color: #111; border-bottom: 2px solid #E5E7EB; padding: 10px; text-align: left; }
    td { border-bottom: 1px solid #F3F4F6; padding: 12px; color: #4B5563; }
    
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
if 'flow' not in st.session_state:
    st.session_state.flow = 'start'

# ==========================================
# PAGE 1: CENTERED LIGHT MODE HERO
# ==========================================
if st.session_state.flow == 'start':
    # HACK: Spacer to push content to middle
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    st.title("SyncIn")
    st.markdown("<h3>Hey buddy, do you know what you want to be?</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        if st.button("YES, I HAVE A DREAM"):
            st.session_state.flow = 'yes'
            st.rerun()
        st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
        if st.button("NO, I'M LOST"):
            st.session_state.flow = 'no'
            st.rerun()

# ==========================================
# PAGE 2: NO BRANCH (Support)
# ==========================================
elif st.session_state.flow == 'no':
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    st.title("SyncIn")
    st.markdown("<h3>It's okay to be lost. Discovery is part of the code.</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        email = st.text_input("Drop your email for Career Games:", placeholder="name@email.com")
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        if st.button("NOTIFY ME"):
            st.success("We'll find your path together.")
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        if st.button("← BACK"):
            st.session_state.flow = 'start'
            st.rerun()

# ==========================================
# PAGE 3: YES BRANCH (Smart Sibling Engine)
# ==========================================
elif st.session_state.flow == 'yes':
    st.markdown("<h2>CAREER RE-ENGINEERING</h2>", unsafe_allow_html=True)
    
    # Input is inside a clean card now
    st.markdown('<div class="sync-card">', unsafe_allow_html=True)
    
    api_key = st.text_input("SYSTEM ACCESS KEY", type="password", help="Enter your Groq API Key")
    
    c1, c2 = st.columns(2)
    with c1:
        goal = st.text_input("THE DREAM ROLE", placeholder="e.g. Product Manager at Google")
        past = st.text_input("YOUR BACKGROUND", placeholder="e.g. 3rd Year Engineering Student")
        budget = st.text_input("BUDGET (INR)", value="0")
    with c2:
        months = st.number_input("TIMELINE (MONTHS)", 1, 60, 12)
        time_val = st.slider("DAILY COMMITMENT (HRS)", 1, 15, 5)
        passion = st.text_input("WHAT EXCITES YOU?", placeholder="e.g. Design, Data")
    
    skills = st.text_area("SKILLS YOU HAVE", height=100)
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    if st.button("SYNC MY FUTURE 🚀"):
        if not api_key:
            st.error("Bud, I need the API key to run the numbers.")
        elif len(goal) < 3:
            st.error("Enter a real goal. Don't waste the engine's time.")
        else:
            try:
                client = Groq(api_key=api_key)
                # SMART SIBLING PROMPT
                prompt = f"""
                Act as 'SyncIn', a smart, honest older sibling (Mentor Persona).
                User: {past} -> {goal}. Timeline: {months} months.
                
                1. **THE REALITY CHECK**: Be blunt but kind. If they are a student asking for a Senior Role, explain 'Years of Experience'.
                
                2. **THE FEASIBILITY TABLE**:
                | Metric | Reality |
                | :--- | :--- |
                | YOE Required | [Industry Standard] |
                | Your Status | {past} |
                | Gap Analysis | [High/Med/Low] |
                
                3. **THE STRATEGY**: 
                - If the goal is impossible, pivot them to the 'Step 1' job.
                - List 3 HARD SKILLS they need.
                
                4. **TIMELINE TRUTH**: When will the dream actually happen? (Give a year).
                """
                with st.spinner("Analyzing your odds..."):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown("<div class='sibling-box'>", unsafe_allow_html=True)
                    st.markdown(chat.choices[0].message.content)
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    if st.button("← BACK"):
        st.session_state.flow = 'start'
        st.rerun()
