import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION (APNI KEY YAHAN DAALO) ---
# 🔴 IMPORTANT: Replace the text below with your actual API Key
genai.configure(api_key="AIzaSyBbJHA4HEIOLt-Ke9zWlfmdcM7fJWZlN2I")

# --- PAGE SETUP (Making it look professional) ---
st.set_page_config(
    page_title="Syncin | SYNC-IN Your Future",
    page_icon="🚀",
    layout="wide", # Wide mode looks more professional
    initial_sidebar_state="expanded"
)

# Custom CSS to hide Streamlit branding and make it look cleaner
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- SIDEBAR (The "About" Section) ---
with st.sidebar:
    st.title("🚀SyncIn")
    st.markdown("### The Goal Re-engineering Engine")
    st.write("Most career advice is generic. This engine reverse-engineers your path based on your *actual* constraints.")
    st.write("---")
    st.markdown("**Built for the zero-budget hustler.**")
    st.caption("Powered by Google Gemini AI")

# --- MAIN PAGE UI ---
st.title("⚡ Reverse-Engineer Your Dream Career")
st.markdown("##### Tell us the goal. We calculate the fastest, cheapest path back to today.")
st.divider()

# Using columns to create a dashboard feel instead of a boring form
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎯 The Destination")
    dream_role = st.text_input("Dream Role", placeholder="e.g. AI Engineer at Google")
    current_status = st.text_input("Current Status", placeholder="e.g. B.Tech 3rd Year, no coding xp")

with col2:
    st.subheader("⏳ The Constraints")
    hours = st.slider("Hours Available (Daily)", 1, 12, 4)
    deadline = st.selectbox("Target Timeline", ["3 Months (Aggressive)", "6 Months (Realistic)", "1 Year (Relaxed)"])

with col3:
    st.subheader("💰 The Fuel")
    budget_type = st.radio("Budget Constraint", ["₹0 (Free Resources Only)", "Low Budget (<₹5k)", "High Budget (>₹20k)"])
    passion = st.text_input("Key Interests/Passions", placeholder="e.g. Problem solving, Gaming")

st.divider()

# --- THE AI BUTTON ---
generate_btn = st.button("🚀 Blueprint Generate Karo (Generate Blueprint)", type="primary", use_container_width=True)

# --- AI LOGIC ---
if generate_btn:
    if not dream_role or not current_status:
        st.error("Please specify a dream role and current status to begin.")
    else:
        # Using the fast, free model
        model = genai.GenerativeModel('gemini-3-pro preview')
        
        # A professional system prompt to ensure sexy output structure
        system_prompt = f"""
        Act as an elite Career Strategy AI. Reverse-engineer the path for a user currently serving as "{current_status}" to become a "{dream_role}".
        
        Constraints: {hours} hours/day, Timeline: {deadline}, Budget: {budget_type}. Interests: {passion}.
        
        You must provide a structured report with these exact sections in bold:
        1. **🚨 The Reality Check** (Is this feasible given constraints? Be honest using math.)
        2. **🧩 The Skill Gap Matrix** (What they have vs. what they need.)
        3. **🗺️ The Phase-Wise Roadmap** (Break down into 3 phases. IMPORTANT: Because budget is {budget_type}, suggest ONLY relevant resources like free YouTube playlists, documentation, or specific cheap courses.)
        4. **⚡ The "Hack"** (One unconventional tip to speed this up.)
        
        Use emojis, bold text, and clear formatting to make it scannable and professional.
        """
        
        with st.spinner("⚙️ Crunching the data, mapping the skills, finding free resources..."):
            try:
                response = model.generate_content(system_prompt)
                st.success("Blueprint Generated Successfully!")
                st.markdown("---")
                # Displaying the result in a nice container
                with st.container(border=True):
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}. Check your API key.")
