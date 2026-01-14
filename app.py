import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG (SyncIn Branding) ---
st.set_page_config(page_title="SyncIn | Career Re-Engineering", page_icon="🔗", layout="wide")

# Custom CSS for "SyncIn" Sexy Look
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(45deg, #00ffa3, #03a9f4);
        color: black; border-radius: 12px; border: none;
        font-weight: bold; padding: 12px 30px; width: 100%;
        transition: 0.5s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 20px #00ffa3; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #121212; color: white; border-radius: 8px; border: 1px solid #333;
    }
    .syncin-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px;
        border: 1px solid rgba(0, 255, 163, 0.2);
        backdrop-filter: blur(10px);
    }
    h1, h2, h3 { color: #00ffa3; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/connect.png", width=80)
    st.title("SyncIn Admin")
    api_key = st.text_input("api key dal", type="password")
    st.write("---")
    st.markdown("### Mission\nReverse-engineering career success for everyone.")

# --- MAIN UI ---
st.title("🔗 SyncIn")
st.markdown("#### *Re-Engineering the path to your dreams.*")
st.write("---")

# Layout
col1, col2 = st.columns(2)

with col1:
    dream_role = st.text_input("What is your Dream Goal?", placeholder="e.g. Senior Data Scientist")
    current_state = st.text_input("Your Current Status?", placeholder="e.g. Student, No experience")

with col2:
    budget = st.text_input("Budget (e.g. 0, ₹10k, or No Limit)")
    time_avail = st.slider("Daily Hours for Study", 1, 15, 4)

# THE ACTION
if st.button("SYNC MY FUTURE 🚀"):
    if not api_key:
        st.error("Bhai, Sidebar mein API Key daal pehle!")
    elif not dream_role:
        st.warning("Dream role toh likh do!")
    else:
        try:
            # Using Gemini 2.0 Flash (Latest)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash') 
            
            prompt = f"""
            System: You are 'SyncIn AI', a high-end career re-engineering agent.
            Task: Reverse-engineer the path to {dream_role} for someone who is {current_state}.
            Constraints: Budget is {budget} and they have {time_avail} hours/day.
            
            Output Style: 
            1. **The SyncIn Reality Check**: Is it possible in 6-12 months? Be blunt.
            2. **Skill Gap Analysis**: What are the top 3 missing pieces?
            3. **The Zero-Budget Roadmap**: Suggest ONLY high-quality free YouTube/OpenSource links.
            4. **Pro Tip**: One secret hack to get noticed.
            """
            
            with st.spinner("Syncing with the future..."):
                response = model.generate_content(prompt)
                st.markdown('<div class="syncin-card">', unsafe_allow_html=True)
                st.subheader("🏁 Your Personalized Blueprint")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}. Model 'gemini-2.0-flash' shayad tere region mein na ho, check kar.")
