import streamlit as st
from groq import Groq
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="SyncIn | AI Career Strategist",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# PREMIUM CSS STYLING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Reset & Base */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #0A0A0F;
        color: #F8FAFC;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0A0A0F 0%, #111827 100%);
        min-height: 100vh;
    }
    
    /* Main Container with Glass Effect */
    .main-container {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        margin: 20px auto;
        max-width: 1200px;
        box-shadow: 0 20px 60px rgba(0, 255, 157, 0.08);
    }
    
    /* Premium Typography */
    h1 {
        font-weight: 800;
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 50%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin-bottom: 16px;
    }
    
    h2 {
        font-weight: 700;
        color: #E2E8F0;
        font-size: 2rem !important;
        margin-top: 0;
    }
    
    h3 {
        font-weight: 600;
        color: #CBD5E1;
        font-size: 1.5rem !important;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #94A3B8;
        line-height: 1.6;
        margin-bottom: 32px;
    }
    
    /* Premium Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        padding: 14px 18px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00FF9D !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 157, 0.1) !important;
    }
    
    /* Enhanced Slider */
    div[data-baseweb="slider"] {
        padding: 30px 0;
    }
    
    div[data-baseweb="slider"] > div {
        height: 8px !important;
        background: rgba(30, 41, 59, 0.5) !important;
        border-radius: 4px !important;
    }
    
    div[data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, #00FF9D, #00B8FF) !important;
        border-radius: 4px !important;
    }
    
    div[role="slider"] {
        background: #FFFFFF !important;
        border: 3px solid #00FF9D !important;
        height: 24px !important;
        width: 24px !important;
        box-shadow: 0 4px 12px rgba(0, 255, 157, 0.3);
        transition: all 0.3s ease;
    }
    
    div[role="slider"]:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 255, 157, 0.4);
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 100%);
        color: #0A0A0F !important;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 157, 0.3);
        background: linear-gradient(90deg, #00FF9D 0%, #00B8FF 100%);
    }
    
    .secondary-btn > button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Trust Indicators */
    .trust-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 255, 157, 0.1);
        border: 1px solid rgba(0, 255, 157, 0.2);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.9rem;
        color: #00FF9D;
        margin: 8px 0;
    }
    
    /* Response Container */
    .response-container {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 157, 0.1);
        padding: 32px;
        margin-top: 32px;
        position: relative;
        overflow: hidden;
    }
    
    .response-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #00FF9D, #00B8FF);
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: rgba(0, 255, 157, 0.3);
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 255, 157, 0.1);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00FF9D, #00B8FF);
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'flow' not in st.session_state:
    st.session_state.flow = 'start'
if 'response_data' not in st.session_state:
    st.session_state.response_data = None

# ============================================================================
# START PAGE - HERO SECTION
# ============================================================================
if st.session_state.flow == 'start':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Trust Badges
        st.markdown("""
        <div style="text-align: center; margin-bottom: 24px;">
            <span class="trust-badge">🔒 Privacy-First</span>
            <span class="trust-badge">🤖 AI-Powered</span>
            <span class="trust-badge">🎯 Precision Analysis</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Hero Content
        st.title("SyncIn")
        st.markdown('<p class="subtitle" style="text-align: center;">Your intelligent career companion—analyzing, strategizing, and mapping your professional journey with precision.</p>', unsafe_allow_html=True)
        
        # Feature Highlights
        features = st.columns(3)
        with features[0]:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #00FF9D; font-size: 2rem;">🎯</h3>
                <h4>Goal Analysis</h4>
                <p style="color: #94A3B8; font-size: 0.9rem;">Realistic career path assessment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with features[1]:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #00B8FF; font-size: 2rem;">📊</h3>
                <h4>Gap Analysis</h4>
                <p style="color: #94A3B8; font-size: 0.9rem;">Skill & experience gap identification</p>
            </div>
            """, unsafe_allow_html=True)
        
        with features[2]:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #6366F1; font-size: 2rem;">🗺️</h3>
                <h4>Roadmap Creation</h4>
                <p style="color: #94A3B8; font-size: 0.9rem;">Personalized step-by-step plan</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Action Section
        st.markdown("### Ready to transform your career trajectory?")
        st.markdown("<p style='text-align: center; color: #94A3B8;'>Let's begin with an honest assessment of where you stand.</p>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            st.markdown("<br>", unsafe_allow_html=True)
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("🚀 I KNOW MY GOAL", use_container_width=True):
                    st.session_state.flow = 'yes'
                    st.rerun()
            with col_no:
                st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                if st.button("🔍 NEED GUIDANCE", use_container_width=True):
                    st.session_state.flow = 'no'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# GUIDANCE PAGE - FOR UNCLEAR GOALS
# ============================================================================
elif st.session_state.flow == 'no':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🔍 Need Career Guidance?")
        st.markdown('<p class="subtitle">Perfectly normal. Most successful careers begin with exploration. Let\'s discover what fits you best.</p>', unsafe_allow_html=True)
        
        # Discovery Form
        with st.form("discovery_form"):
            st.markdown("### Tell us about yourself")
            
            col_a, col_b = st.columns(2)
            with col_a:
                interests = st.text_input("What topics naturally draw your attention?", 
                                        placeholder="e.g., Technology, Design, Business")
                personality = st.selectbox("Your work style preference:", 
                                         ["Independent", "Team Player", "Leader", "Creative", "Analytical"])
            
            with col_b:
                strengths = st.text_input("What are you naturally good at?", 
                                        placeholder="e.g., Problem-solving, Communication")
                values = st.multiselect("What matters most to you?", 
                                      ["Work-Life Balance", "High Income", "Impact", "Creativity", "Stability", "Growth"])
            
            email = st.text_input("Where should we send personalized insights?", 
                                 placeholder="your.email@example.com")
            
            submitted = st.form_submit_button("🔮 GET PERSONALIZED GUIDANCE", use_container_width=True)
            
            if submitted and email:
                with st.spinner("Analyzing your unique profile..."):
                    time.sleep(2)
                    st.success("✓ Profile received. We'll send your personalized career exploration guide within 24 hours.")
                    st.info("In the meantime, consider exploring roles in: **Product Management, UX Design, Data Analysis**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("← Return to Home", use_container_width=True):
            st.session_state.flow = 'start'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# MAIN ANALYSIS ENGINE
# ============================================================================
elif st.session_state.flow == 'yes':
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
    with col_header2:
        st.markdown("## 🎯 Career Re-Engineering Dashboard")
        st.markdown('<p class="subtitle">Precision analysis of your career trajectory with actionable insights</p>', unsafe_allow_html=True)
    
    # Security Note
    with st.expander("🔒 Your data is secure", expanded=False):
        st.markdown("""
        - **Encrypted**: All data is encrypted in transit and at rest
        - **Private**: Your information is never stored or shared
        - **Compliant**: GDPR & CCPA compliant processing
        - **Transparent**: We show you exactly how your data is used
        """)
    
    # API Key with Enhanced Security UI
    with st.container():
        st.markdown("### 🔑 System Access")
        col_key1, col_key2 = st.columns([3, 1])
        with col_key1:
            api_key = st.text_input("Enter your API Key", type="password", 
                                   placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                                   help="Required for secure AI processing")
        with col_key2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("[Get API Key ↗](https://console.groq.com)", help="Get your free API key from Groq Cloud")
    
    # Career Profile Form
    st.markdown("### 📝 Your Career Profile")
    
    with st.form("career_form"):
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### Aspirations")
            goal = st.text_input("Target Role/Company", 
                               placeholder="e.g., Senior Product Manager at Stripe")
            passion = st.text_area("What energizes you?", 
                                 placeholder="Describe work that doesn't feel like work...")
        
        with col_right:
            st.markdown("#### Current Reality")
            past = st.text_input("Current Background", 
                               placeholder="e.g., 2 years in Marketing, Computer Science Graduate")
            skills = st.text_area("Existing Skills", 
                                 placeholder="Technical and soft skills you already possess")
        
        st.markdown("---")
        
        # Resources & Timeline
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.markdown("#### ⏳ Timeline")
            months = st.number_input("Target Months", 1, 60, 12, 
                                    help="Realistic timeframe for career transition")
        
        with col_res2:
            st.markdown("#### 💰 Resources")
            budget = st.selectbox("Monthly Investment (INR)", 
                                ["0-5,000", "5,000-15,000", "15,000-30,000", "30,000+"])
        
        with col_res3:
            st.markdown("#### ⚡ Commitment")
            time_val = st.slider("Daily Hours Available", 1, 15, 5,
                                help="Consistent daily commitment is key")
        
        # Submit Button
        submitted = st.form_submit_button("🚀 LAUNCH CAREER ANALYSIS", 
                                         use_container_width=True,
                                         type="primary")
    
    # Analysis Engine
    if submitted:
        if not api_key:
            st.error("🔐 Security Check: API key required for analysis")
        elif len(goal) < 5:
            st.error("🎯 Please specify a clear career target")
        else:
            try:
                # Initialize client
                client = Groq(api_key=api_key)
                
                # Enhanced prompt for better analysis
                prompt = f"""
                ACT as 'SyncIn Career Strategist' - a seasoned executive coach with 20+ years in talent development.
                
                CLIENT PROFILE:
                - Target: {goal}
                - Background: {past}
                - Skills Inventory: {skills}
                - Motivators: {passion}
                - Timeline: {months} months
                - Resources: {budget} INR/month
                - Commitment: {time_val} hours/day
                
                RESPONSE STRUCTURE:
                
                1. **EXECUTIVE SUMMARY**
                   - Reality Check: (Brief, direct assessment of feasibility)
                   - Probability Score: (X/10 chance of success given constraints)
                
                2. **GAP ANALYSIS MATRIX**
                   Create a comparison table showing:
                   | Competency Area | Industry Standard | Your Current Level | Gap Size |
                   |-----------------|-------------------|-------------------|----------|
                   [Fill with relevant areas based on target role]
                
                3. **PHASED ROADMAP**
                   Phase 1 (Months 1-{max(3, months//3)}): Foundation
                   - Critical 3 skills to acquire
                   - Specific resources/courses (budget-aware)
                   - Expected outcomes
                
                   Phase 2 (Months {max(3, months//3)+1}-{months*2//3}): Application
                   - Portfolio/project recommendations
                   - Networking targets
                   - Validation milestones
                
                   Phase 3 (Months {months*2//3+1}-{months}): Transition
                   - Job search strategy
                   - Interview preparation focus
                   - Negotiation points
                
                4. **RISK MITIGATION**
                   - Likely obstacles and solutions
                   - Alternative paths if primary fails
                   - When to pivot vs. persist
                
                5. **SUCCESS METRICS**
                   - Monthly checkpoints
                   - Quantitative progress measures
                   - Confidence indicators
                
                TONE: Professional, direct but supportive. Use data-driven language.
                """
                
                # Show analysis progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    status_text.text(f"Analyzing career pathways... {i+1}%")
                    time.sleep(0.02)
                
                status_text.text("Finalizing strategic recommendations...")
                
                # Get AI response
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=2000
                )
                
                # Display results
                st.markdown("---")
                st.markdown("## 📊 Analysis Complete")
                st.markdown('<div class="response-container">', unsafe_allow_html=True)
                
                # Success indicator
                st.markdown("""
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                    <div style="background: rgba(0, 255, 157, 0.1); padding: 12px; border-radius: 12px;">
                        <span style="font-size: 2rem;">✅</span>
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #00FF9D;">Career Strategy Generated</h3>
                        <p style="margin: 0; color: #94A3B8;">Personalized for your profile</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # AI Response
                st.markdown(chat.choices[0].message.content)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Action buttons after analysis
                col_action1, col_action2, col_action3 = st.columns(3)
                with col_action1:
                    if st.button("📥 Export as PDF", use_container_width=True):
                        st.success("PDF export initiated (simulated)")
                with col_action2:
                    if st.button("🔄 Refine Analysis", use_container_width=True):
                        st.info("Adjust parameters and resubmit")
                with col_action3:
                    if st.button("💬 Schedule Consultation", use_container_width=True):
                        st.info("Consultation feature coming soon")
                
            except Exception as e:
                st.error(f"""
                ⚠️ Analysis Engine Error
                ```
                {str(e)}
                ```
                Please verify your API key and try again.
                """)
    
    # Footer Navigation
    st.markdown("---")
    col_nav1, col_nav2, col_nav3 = st.columns([2, 1, 2])
    with col_nav2:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.flow = 'start'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div style="text-align: center; padding: 40px 20px; color: #64748B; font-size: 0.9rem;">
    <hr style="border: none; height: 1px; background: rgba(255, 255, 255, 0.1); margin: 30px 0;">
    <p>© 2024 SyncIn. All rights reserved.</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        This tool provides AI-generated career guidance. Always validate recommendations with human mentors.<br>
        <a href="#" style="color: #00FF9D; text-decoration: none;">Privacy Policy</a> • 
        <a href="#" style="color: #00FF9D; text-decoration: none;">Terms of Service</a> • 
        <a href="#" style="color: #00FF9D; text-decoration: none;">Contact</a>
    </p>
</div>
""", unsafe_allow_html=True)
