import streamlit as st
import plotly.graph_objects as go
import json
import datetime
import random
from password_analyzer import analyze_password
from utils import get_strength_color, get_emoji_rating
from assets.password_tips import get_password_tips, get_security_facts
from password_insights import (
    get_funny_comment, 
    get_historical_insight, 
    get_password_strength_description,
    get_security_strategy,
    get_password_hash_preview
)

# Set page configuration
st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for password history
if 'password_history' not in st.session_state:
    # Try to load from local storage
    try:
        with open('.password_history.json', 'r') as f:
            st.session_state.password_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.password_history = []

# Initialize session state for used passwords (to prevent reuse)
if 'used_passwords' not in st.session_state:
    try:
        with open('.used_passwords.json', 'r') as f:
            st.session_state.used_passwords = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.used_passwords = []
        
# Initialize session state for active section in sidebar
if 'active_section' not in st.session_state:
    st.session_state.active_section = 'security_tips'

# Custom CSS with dark theme, neon effects, and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap');
    
    /* General styling */
    body {
        background: linear-gradient(135deg, #0D0D13 0%, #13131E 100%);
    }
    
    .main-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #00FFBB 0%, #4D65FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 15px rgba(0, 255, 187, 0.7);
        animation: pulse-glow 3s infinite alternate;
        position: relative;
        padding-top: 15px;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 80px;
        height: 5px;
        background: linear-gradient(90deg, #00FFBB, transparent);
        border-radius: 5px;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        right: 0;
        width: 120px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #4D65FF);
        border-radius: 5px;
    }
    
    @keyframes pulse-glow {
        0% {
            text-shadow: 0 0 5px rgba(0, 255, 187, 0.3);
        }
        50% {
            text-shadow: 0 0 15px rgba(0, 255, 187, 0.5), 0 0 30px rgba(77, 101, 255, 0.3);
        }
        100% {
            text-shadow: 0 0 20px rgba(0, 255, 187, 0.7), 0 0 40px rgba(77, 101, 255, 0.5);
        }
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: rgba(233, 233, 242, 0.8);
        margin-bottom: 1.5rem;
        margin-top: 1rem;
        font-family: 'Outfit', sans-serif;
        font-weight: 300;
        letter-spacing: 0.5px;
        position: relative;
        padding-left: 15px;
        border-left: 3px solid #4D65FF;
    }
    
    .password-input-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #E9E9F2;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        position: relative;
    }
    
    .password-input-label::before {
        content: '>';
        color: #00FFBB;
        margin-right: 8px;
        font-weight: 700;
        animation: cursor-blink 1s infinite;
    }
    
    @keyframes cursor-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    /* Modern card styling with glowing borders */
    .result-section {
        background: linear-gradient(135deg, #171722 0%, #20203A 100%);
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(77, 101, 255, 0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
    }
    
    .result-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00FFBB, #4D65FF);
        opacity: 0.8;
    }
    
    .result-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.6);
        border-color: rgba(77, 101, 255, 0.6);
    }
    
    .result-section:hover::before {
        opacity: 1;
        animation: border-flow 2s linear infinite;
    }
    
    @keyframes border-flow {
        0% { background-position: 0% 0; }
        100% { background-position: 100% 0; }
    }
    
    .strength-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        color: #00FFBB;
        letter-spacing: 1px;
        text-transform: uppercase;
        position: relative;
        display: inline-block;
        padding-bottom: 5px;
    }
    
    .strength-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60%;
        height: 2px;
        background: linear-gradient(90deg, #00FFBB, transparent);
    }
    
    .warning {
        color: #FF416C;
        font-weight: bold;
        background: rgba(255, 65, 108, 0.1);
        padding: 12px 15px;
        border-radius: 5px;
        border-left: 3px solid #FF416C;
        display: flex;
        align-items: center;
        margin: 15px 0;
    }
    
    .tip-title {
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #FF00FF;
        text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
    }
    
    .tip-item {
        margin-bottom: 0.3rem;
        transition: all 0.2s ease;
    }
    
    .footer {
        margin-top: 3rem;
        text-align: center;
        color: #757575;
        font-size: 0.9rem;
    }
    
    /* Modern Cyberpunk Button Style */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 187, 0.1) 0%, rgba(77, 101, 255, 0.1) 100%);
        color: #00FFBB;
        font-weight: 600;
        border-radius: 4px;
        padding: 0.8rem 1.5rem;
        border: 1px solid rgba(0, 255, 187, 0.3);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(0, 255, 187, 0.4) 0%, rgba(77, 101, 255, 0.4) 100%);
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s ease;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #00FFBB, #4D65FF);
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.4s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border-color: rgba(0, 255, 187, 0.6);
        color: white;
    }
    
    .stButton > button:hover::before {
        opacity: 1;
    }
    
    .stButton > button:hover::after {
        transform: scaleX(1);
        transform-origin: left;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Section Headers */
    .real-time-header {
        font-family: 'Rajdhani', sans-serif;
        color: #4D65FF;
        font-weight: 600;
        font-size: 1.3rem;
        margin-top: 2rem;
        margin-bottom: 0.8rem;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        text-transform: uppercase;
    }
    
    .real-time-header::before {
        content: '';
        display: inline-block;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00FFBB 0%, #4D65FF 100%);
        margin-right: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 187, 0.5);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Strength Colors with Neon Effect */
    .strength-weak {
        color: #FF073A;
        text-shadow: 0 0 5px #FF073A;
    }
    
    .strength-medium {
        color: #FFAA00;
        text-shadow: 0 0 5px #FFAA00;
    }
    
    .strength-strong {
        color: #00FF66;
        text-shadow: 0 0 5px #00FF66;
    }
    
    /* Password History Styling */
    .history-container {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid #333;
        box-shadow: 0 0 5px rgba(0, 255, 102, 0.2);
    }
    
    .history-header {
        color: #00FFFF;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    .history-item {
        padding: 8px;
        margin-bottom: 8px;
        border-radius: 5px;
        background-color: #2A2A2A;
        transition: all 0.2s ease;
        border-left: 3px solid;
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 0 8px rgba(0, 255, 102, 0.3);
    }
    
    .history-weak {
        border-left-color: #FF073A;
    }
    
    .history-medium {
        border-left-color: #FFAA00;
    }
    
    .history-strong {
        border-left-color: #00FF66;
    }
    
    .clear-button {
        background-color: #333;
        color: #FF073A;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.2s ease;
    }
    
    .clear-button:hover {
        background-color: #FF073A;
        color: #121212;
    }
    
    /* Fun result message styling */
    .fun-result {
        margin-top: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Modern sidebar section styling */
    .custom-section {
        background: linear-gradient(135deg, #171722 0%, #1A1A2E 100%);
        border-radius: 8px;
        padding: 20px 15px;
        margin-top: 20px;
        border: 1px solid rgba(77, 101, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .custom-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00FFBB, #4D65FF);
        opacity: 0.5;
    }
    
    .custom-section:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        transform: translateY(-3px);
        border-color: rgba(77, 101, 255, 0.4);
    }
    
    .custom-section:hover::before {
        opacity: 1;
    }
    
    .custom-section-header {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.2rem;
        color: #00FFBB;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        border-bottom: 1px solid rgba(77, 101, 255, 0.2);
        padding-bottom: 10px;
    }
    
    .custom-section-header::before {
        content: '';
        display: inline-block;
        width: 10px;
        height: 10px;
        background: linear-gradient(135deg, #00FFBB, #4D65FF);
        margin-right: 8px;
        border-radius: 2px;
        transform: rotate(45deg);
    }
    
    /* Make st.progress bars more neon with better contrast */
    div.stProgress > div > div {
        background-color: #00FFBB !important;
        box-shadow: 0 0 8px #00FFBB;
    }
    
    /* Override streamlit progress bar text to ensure better visibility */
    div.stProgress > div > div > div {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        text-shadow: 0 0 2px #000000, 0 0 3px #000000 !important;
        background-color: transparent !important;
        padding: 0 8px !important;
    }
    
    /* Improve visibility of all text in result sections */
    .result-section {
        background: transparent;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(0, 255, 187, 0.4);
        box-shadow: 0 0 15px rgba(0, 255, 187, 0.15);
    }
    
    .result-section p, .result-section li {
        color: #FFFFFF !important;
    }
    
    /* Make all markdown text more visible */
    p, li, h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Make captions more visible */
    .css-1offfwp {
        color: #B8E6FF !important;
        opacity: 0.9 !important;
    }
    
    /* Better styling for markdown headers */
    h3, h4 {
        color: #00FFBB !important;
        text-shadow: 0 0 10px rgba(0, 255, 187, 0.3);
        letter-spacing: 0.5px;
    }
    
    /* Tooltip hover effect */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: #2A2A2A;
        color: #E0E0E0;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
        border: 1px solid #00FF66;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<div class="main-header">Password Strength Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Check how strong your password is in real-time</div>', unsafe_allow_html=True)

# Password input
st.markdown('<div class="password-input-label">Enter a password to check:</div>', unsafe_allow_html=True)
password = st.text_input("Password", type="password", key="password_input", help="Your password is never stored or transmitted", label_visibility="collapsed")

# Add a check strength button
check_button = st.button("Check Strength", key="check_strength")

# Password policy disclaimer
st.caption("Your password is never stored, transmitted, or logged. All analysis happens directly in your browser.")

# Sidebar with interactive sections
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; position: relative; padding: 15px 0;">
        <h2 style="font-family: 'Rajdhani', sans-serif; color: #00FFBB; text-shadow: 0 0 10px rgba(0, 255, 187, 0.5); 
                  letter-spacing: 1.5px; font-weight: 700; text-transform: uppercase;">
            🔐 SECURITY HUB
        </h2>
        <div style="position: absolute; height: 3px; width: 80px; background: linear-gradient(90deg, transparent, #00FFBB, transparent); 
                    bottom: 0; left: 50%; transform: translateX(-50%);"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create sidebar tabs for different sections
    tab_options = {
        'security_tips': '🛡 Security Tips',
        'history': '📜 Password History',
        'facts': '🧠 Security Facts',
        'visualization': '📊 Hash Visualization',
        'funny': '😂 Fun Facts',
        'insights': '🔍 Insights'
    }
    
    # Navigation buttons for sidebar sections
    cols = st.columns(3)
    btn_idx = 0
    
    for section_id, section_name in tab_options.items():
        with cols[btn_idx % 3]:
            is_active = st.session_state.active_section == section_id
            button_style = "primary" if is_active else "secondary"
            if st.button(section_name, key=f"btn_{section_id}", type=button_style):
                st.session_state.active_section = section_id
        btn_idx += 1
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Security Tips Section
    if st.session_state.active_section == 'security_tips':
        st.markdown('<div class="custom-section-header">🛡 Security Tips</div>', unsafe_allow_html=True)
        tips = get_password_tips()
        for tip in tips:
            with st.expander(f"{tip['title']}"):
                st.markdown(tip['content'])
                
    # Password History Section
    elif st.session_state.active_section == 'history':
        st.markdown('<div class="custom-section-header">📜 Password History</div>', unsafe_allow_html=True)
        
        if not st.session_state.password_history:
            st.info("No password history yet. Check some passwords to see your history.")
        else:
            # Create a clear history button
            if st.button("Clear History", key="clear_history"):
                st.session_state.password_history = []
                st.session_state.used_passwords = []
                
                # Save empty history to files
                with open('.password_history.json', 'w') as f:
                    json.dump([], f)
                with open('.used_passwords.json', 'w') as f:
                    json.dump([], f)
                    
                st.success("Password history cleared!")
                
            # Display each history item
            for idx, item in enumerate(st.session_state.password_history):
                with st.container():
                    # Determine strength class
                    if item["score"] <= 1:
                        strength_class = "history-weak"
                    elif item["score"] <= 2:
                        strength_class = "history-medium"
                    else:
                        strength_class = "history-strong"
                        
                    # Create HTML for history item
                    st.markdown(f"""
                    <div class="history-item {strength_class}">
                        <strong>Date:</strong> {item["date"]}<br>
                        <strong>Strength:</strong> {get_emoji_rating(item["score"])}<br>
                        <strong>Crack time:</strong> {item["crack_time"]}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Security Facts Section
    elif st.session_state.active_section == 'facts':
        st.markdown('<div class="custom-section-header">🧠 Security Facts</div>', unsafe_allow_html=True)
        facts = get_security_facts()
        
        # Create tabs for navigating facts
        fact_tabs = st.tabs(["Fact " + str(i+1) for i in range(min(5, len(facts)))])
        for i, tab in enumerate(fact_tabs):
            with tab:
                st.info(facts[i])
    
    # Hash Visualization Section
    elif st.session_state.active_section == 'visualization':
        st.markdown('<div class="custom-section-header">📊 Hash Visualization</div>', unsafe_allow_html=True)
        
        if not password:
            st.info("Enter a password in the main panel to see its hash visualization.")
        else:
            # Show hash visualization
            hash_preview = get_password_hash_preview(password)
            st.code(hash_preview, language="text")
            st.caption("This is not your actual stored password, but a visual representation of how password hashing works.")
            
            # Add simple hash animation
            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <div style="font-family: monospace; color: #00FF66; animation: hashAnimation 3s infinite;">
                    Password → [Hashing Algorithm] → Secure Hash
                </div>
            </div>
            <style>
                @keyframes hashAnimation {
                    0% { opacity: 0.5; }
                    50% { opacity: 1; }
                    100% { opacity: 0.5; }
                }
            </style>
            """, unsafe_allow_html=True)
                
    # Fun Facts Section
    elif st.session_state.active_section == 'funny':
        st.markdown('<div class="custom-section-header">😂 Fun Password Facts</div>', unsafe_allow_html=True)
        
        fun_facts = [
            "The average person spends about 12 days of their life thinking about passwords.",
            "The most commonly used password globally is still '123456', used by millions of people.",
            "A quantum computer could theoretically crack most passwords in seconds... but they're still a ways off.",
            "Over 80% of data breaches involve weak or stolen passwords.",
            "A 12-character password takes about 62 trillion times longer to crack than a 6-character one!",
            "The strongest password created by AI was so complex that even the AI couldn't remember it.",
            "Password reuse is so common that there's a specific attack named for it: 'credential stuffing'."
        ]
        
        selected_fact = random.choice(fun_facts)
        st.info(selected_fact)
        
        # Add fun password meme/gif reference
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p style="color: #FF00FF;">Password strength:</p>
            <div style="font-size: 20px; color: #FF073A; margin: 5px 0;">weak: password</div>
            <div style="font-size: 20px; color: #FFAA00; margin: 5px 0;">medium: P@ssw0rd</div>
            <div style="font-size: 20px; color: #00FF66; margin: 5px 0;">strong: kX9^p2!LmZ@vQ</div>
            <div style="font-size: 20px; color: #00FFFF; margin: 5px 0;">unbreakable: correct horse battery staple</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Security Insights Section
    elif st.session_state.active_section == 'insights':
        st.markdown('<div class="custom-section-header">🔍 Security Insights</div>', unsafe_allow_html=True)
        
        if not password:
            st.info("Enter a password in the main panel to see personalized security insights.")
        elif not check_button:
            st.info("Click 'Check Strength' to get detailed security insights.")
        elif 'current_score' in st.session_state:
            # Display relevant security strategies based on the password score
            strategies = get_security_strategy(st.session_state.current_score)
            
            st.markdown("### Recommendations:")
            for strategy in strategies:
                st.markdown(f"- {strategy}")
                
            # Add a historical insight
            st.markdown("### Historical Context:")
            insight = get_historical_insight(st.session_state.current_score, password)
            st.info(insight)

# Add real-time feedback section before full analysis
if password:
    # Quick real-time feedback
    st.markdown('<div class="real-time-header">Real-time Feedback:</div>', unsafe_allow_html=True)
    
    # Add a container with custom styling for real-time feedback
    with st.container():
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        
        # Basic length check
        length = len(password)
        length_percent = min(100, (length / 16) * 100)  # 16 chars is 100%
        
        if length < 8:
            length_color = "#FF4B4B"  # Red
            length_msg = f"Too short ({length} chars) - minimum 8 characters recommended"
        elif length < 12:
            length_color = "#FFA500"  # Orange
            length_msg = f"Acceptable length ({length} chars) - 12+ characters is better"
        else:
            length_color = "#00CC66"  # Green
            length_msg = f"Good length ({length} chars)"
        
        st.markdown("*Length:*")
        st.progress(length_percent/100, text=length_msg)
        
        # Basic character type checks
        st.markdown("*Character Types:*")
        
        # Check for different character types
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        # Display each character type with a styled icon
        col1, col2 = st.columns(2)
        with col1:
            upper_style = "color: #00FFBB; font-weight: bold;" if has_upper else "color: #FF4B4B; font-weight: bold;"
            lower_style = "color: #00FFBB; font-weight: bold;" if has_lower else "color: #FF4B4B; font-weight: bold;"
            upper_icon = "✓" if has_upper else "✗"
            lower_icon = "✓" if has_lower else "✗"
            st.markdown(f"<span style='{upper_style}'>[{upper_icon}]</span> <span style='color: #FFFFFF; font-weight: 500;'>Uppercase letters</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='{lower_style}'>[{lower_icon}]</span> <span style='color: #FFFFFF; font-weight: 500;'>Lowercase letters</span>", unsafe_allow_html=True)
        
        with col2:
            digit_style = "color: #00FFBB; font-weight: bold;" if has_digit else "color: #FF4B4B; font-weight: bold;"
            special_style = "color: #00FFBB; font-weight: bold;" if has_special else "color: #FF4B4B; font-weight: bold;"
            digit_icon = "✓" if has_digit else "✗"
            special_icon = "✓" if has_special else "✗"
            st.markdown(f"<span style='{digit_style}'>[{digit_icon}]</span> <span style='color: #FFFFFF; font-weight: 500;'>Numbers</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='{special_style}'>[{special_icon}]</span> <span style='color: #FFFFFF; font-weight: 500;'>Special characters</span>", unsafe_allow_html=True)
        
        # Calculate overall complexity
        complexity_score = sum([has_upper, has_lower, has_digit, has_special])
        complexity_percent = (complexity_score / 4) * 100
        
        if complexity_score <= 2:
            complexity_text = "Low complexity - add more character types"
        elif complexity_score == 3:
            complexity_text = "Medium complexity - good mix of characters"
        else:
            complexity_text = "High complexity - excellent character variety"
        
        st.markdown("*Overall Complexity:*")
        st.progress(complexity_percent/100, text=complexity_text)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Full analysis only when the button is clicked and there's a password
if check_button and password:
    # Check if this password is in the used passwords list
    password_previously_used = False
    if password in st.session_state.used_passwords:
        password_previously_used = True
    
    # Analyze password
    analysis = analyze_password(password)
    score = analysis['score']
    feedback = analysis['feedback']
    time_to_crack = analysis['crack_time_display']
    warnings = analysis['warnings']
    suggestions = analysis['suggestions']
    strength_details = analysis['strength_details']
    
    # Store current analysis in session state for sidebar access
    st.session_state.current_score = score
    st.session_state.current_time_to_crack = time_to_crack
    
    # Get a funny comment based on the score
    funny_comment = get_funny_comment(score, time_to_crack)
    
    # Get a strength description
    strength_desc = get_password_strength_description(score)

    # Create two columns for layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        
        # Add warning for previously used password
        if password_previously_used:
            st.markdown('<div class="warning">⚠ This password has been checked before! Using the same password for multiple accounts is not recommended.</div>', unsafe_allow_html=True)
        
        # Password strength gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 4], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': get_strength_color(score)},
                'steps': [
                    {'range': [0, 1], 'color': "#FF4B4B"},  # Very Weak (as per style guide)
                    {'range': [1, 2], 'color': "#FF4B4B"},  # Weak (as per style guide)
                    {'range': [2, 3], 'color': "#FFA500"},  # Medium (as per style guide)
                    {'range': [3, 4], 'color': "#00CC66"}   # Strong (as per style guide)
                ],
            },
            title={'text': f"Password Strength: {get_emoji_rating(score)}"}
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#E0E0E0"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Time to crack info
        st.markdown(f"### Estimated time to crack: *{time_to_crack}*")
        
        # Strength description
        st.markdown(f"<div class='strength-header'>{strength_desc['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"{strength_desc['content']}")
        
        # Add the funny comment with appropriate styling based on score
        if score <= 1:
            color_class = "strength-weak"
        elif score <= 2:
            color_class = "strength-medium"
        else:
            color_class = "strength-strong"
            
        st.markdown(f"<div class='fun-result {color_class}'>{funny_comment}</div>", unsafe_allow_html=True)
        
        # Warnings and suggestions
        if warnings:
            st.markdown(f"<div class='warning'>⚠ {warnings}</div>", unsafe_allow_html=True)
        
        if suggestions:
            st.markdown("### Improvement suggestions:")
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown('<div class="strength-header">Password Details</div>', unsafe_allow_html=True)
        
        # Password criteria checks with better styling
        for criteria, details in strength_details.items():
            if details['pass']:
                status_style = "color: #00FFBB; font-weight: bold;"
                status_icon = "✓"
                message_style = "color: #BDE0FE;"
            else:
                status_style = "color: #FF4B4B; font-weight: bold;"
                status_icon = "✗"
                message_style = "color: #E0E0E0;"
            
            st.markdown(f"""
            <div style="margin-bottom: 15px; border-bottom: 1px solid rgba(0, 255, 187, 0.2);">
                <span style="{status_style}">[{status_icon}]</span> 
                <span style="color: #00FFBB; font-weight: 500;">{criteria}:</span> 
                <span style="color: #FFFFFF; font-weight: 400;">{details['message']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Add this password check to history if it's new
    if not password_previously_used:
        # Add to used passwords list
        st.session_state.used_passwords.append(password)
        
        # Create history entry with masked password
        history_item = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": score,
            "crack_time": time_to_crack
        }
        
        # Add to history (at the beginning)
        st.session_state.password_history.insert(0, history_item)
        
        # Keep only the last 10 history items
        if len(st.session_state.password_history) > 10:
            st.session_state.password_history = st.session_state.password_history[:10]
            
        # Save history to file
        try:
            with open('.password_history.json', 'w') as f:
                json.dump(st.session_state.password_history, f)
            with open('.used_passwords.json', 'w') as f:
                json.dump(st.session_state.used_passwords, f)
        except Exception as e:
            st.error(f"Failed to save history: {e}")
            
    # Add an extra section for more advanced security insights
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown('<div class="strength-header">Security Context</div>', unsafe_allow_html=True)
    
    # Show relevant security strategies
    strategies = get_security_strategy(score)
    st.markdown("#### Key Recommendations:")
    for idx, strategy in enumerate(strategies[:3]):  # Show top 3 strategies
        st.markdown(f"{idx+1}. {strategy}")
        
    # Add a "View More in Security Insights" button to direct to the sidebar
    if st.button("View More in Security Insights", key="view_insights"):
        st.session_state.active_section = 'insights'
        st.experimental_rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">This tool is for educational purposes only. Always use unique passwords and a password manager.</div>', unsafe_allow_html=True)