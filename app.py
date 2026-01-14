import streamlit as st
from groq import Groq

# --- SYNCIN PREMIUM SETUP ---
st.set_page_config(page_title="SyncIn | SYNC-IN your career", page_icon="🔗", layout="centered")

# Custom CSS for the "Silicon Valley" Aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
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
        font-size: 3rem !important;
    }

    .stButton>button {
        background: #111;
        color: #00FF9D;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 700;
        transition: 0.4s;
        width: 100%;
    }

    .stButton>button:hover {
        border-color: #00FF9D;
        box-shadow: 0px 0px 15px rgba(0, 255, 157, 0.3);
        background: #00FF9D;
        color: black;
    }

    .card {
        background: #0A0A0A;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #1A1A1A;
        margin-bottom: 20px;
    }

    input { background-color: #0A0A0A !important; border: 1px solid #333 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if 'flow' not in st.session_state:
    st.session_state.flow = 'start'

# --- START PAGE ---
if st.session_state.flow == 'start':
    st.title("🔗 SyncIn")
    st.markdown("### Hey buddy, do you know what you want to be?")
    st.write("Let's map your future together.")
    
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
    st.write("Figuring it out is the hardest part. We are building **Career Games** to help you play and discover.")
    st.write("---")
    email = st.text_input("Drop your email, we'll reach out when we're ready:")
    if st.button("Notify Me"):
        st.success("All the best, bud! We'll sync up soon.")
    if st.button("← Back"):
        st.session_state.flow = 'start'
        st.rerun()

# --- YES BRANCH: THE AI ENGINE ---
elif st.session_state.flow == 'yes':
    st.title("🔗 SyncIn")
    st.write("### Let's Re-Engineer your path. ⚡")
    
    api_key = st.text_input("Enter Groq API Key (Keep it secret)", type="password")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            goal = st.text_input("Dream Role", placeholder="e.g. VC / Founder")
            past = st.text_input("Current Education", placeholder="e.g. B.Com 2nd Year")
        with c2:
            budget = st.text_input("Budget (INR)", placeholder="e.g. ₹5000")
            time_val = st.slider("Daily Hours", 1, 15, 4)
        
        skills = st.text_area("Existing Skills")
        passion = st.text_input("Your Passion")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SYNC MY FUTURE 🚀"):
        if not api_key:
            st.error("Add your API key first!")
        else:
            try:
                client = Groq(api_key=api_key)
                # This prompt forces the AI to give you the Flowchart and LinkedIn IDs
                prompt = f"""
                You are SyncIn AI Career Strategist. 
                Goal: {goal}. Background: {past}. Skills: {skills}. Budget: {budget}. Time: {time_val} hrs/day.
                
                Respond in English with:
                1. Reality Check (Math-based feasibility)
                2. Step-by-Step Roadmap (Phases)
                3. Courses (Specific free/cheap YouTube or platform names)
                4. Visual Flowchart (A 4-step written description of the flow)
                5. LinkedIn Profiles: Suggest 3 specific job titles to search for on LinkedIn to find mentors.
                """
                with st.spinner("Calculating the optimal path..."):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-specdec",
                    )
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(chat.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    if st.button("← Back"):
        st.session_state.flow = 'start'
        st.rerun()
