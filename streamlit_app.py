import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

st.set_page_config(
    page_title="WhatsApp Offline Loader Setup v4.0",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# WhatsApp Loader Custom CSS
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    :root {
        --primary-color: #7d7dff;
        --secondary-color: #25d366;
        --accent-color: #ff6b6b;
        --dark-color: #2c3e50;
        --light-color: #f8f9fa;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
    }
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header Styling */
    .main-header {
        position: relative;
        width: 100%;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,.1);
        overflow: hidden;
        background: linear-gradient(90deg, var(--primary-color) 0%, #6a6aff 100%);
        color: white;
        margin-bottom: 2rem;
        border-radius: 0 0 15px 15px;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
        text-align: center;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    
    .header-text {
        text-align: left;
        margin-left: 20px;
    }
    
    .header-content h1 {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-content p {
        font-size: 0.9rem;
        margin: 5px 0 0;
        font-weight: 500;
        letter-spacing: 0.5px;
        opacity: 0.9;
    }
    
    .code-logo {
        width: 70px;
        height: 70px;
        background-color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .code-logo-inner {
        font-family: 'Courier New', monospace;
        font-weight: 900;
        font-size: 1.8rem;
        color: var(--primary-color);
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        position: relative;
    }
    
    .code-logo::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border: 2px solid rgba(125, 125, 255, 0.3);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(0.95);
            opacity: 0.7;
        }
        70% {
            transform: scale(1.1);
            opacity: 0.3;
        }
        100% {
            transform: scale(0.95);
            opacity: 0.7;
        }
    }
    
    .header-decoration {
        position: absolute;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkZWZzPjxwYXR0ZXJuIGlkPSJwYXR0ZXJuIiB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiIHBhdHRlcm5UcmFuc2Zvcm09InJvdGF0ZSg0NSkiPjxyZWN0IHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgZmlsbD0icmdiYSgyNTUsMjU1LDI1NSwwLjA1KSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNwYXR0ZXJuKSIvPjwvc3ZnPg=='), linear-gradient(90deg, rgba(0,0,0,0.1) 0%, transparent 50%, rgba(0,0,0,0.1) 100%);
    }

    /* Container Styling */
    .main-container {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        max-width: 800px;
        margin: 0 auto;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Input and Form Styling */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        color: green !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        border-radius: 50px !important;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        outline: none !important;
        border: 1px solid #ccc !important;
        font-size: 1rem !important;
        box-sizing: border-box !important;
        margin-top: 8px !important;
        margin-bottom: 8px !important;
        background: white !important;
    }
    
    .stTextArea>div>div>textarea {
        height: 140px !important;
        resize: none !important;
        border-radius: 15px !important;
    }
    
    /* Button Styling */
    .stButton>button {
        padding: 17px 40px;
        border-radius: 50px;
        cursor: pointer;
        border: 0;
        background-color: white;
        box-shadow: rgb(0 0 0 / 50%) 0 0 8px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-size: 15px;
        transition: all 0.5s ease;
        margin: 10px 5px;
        color: #333;
        font-weight: 600;
        width: auto;
    }

    .stButton>button:hover {
        letter-spacing: 4px;
        background-color: rgb(24, 191, 220);
        color: hsl(0, 0%, 100%);
        box-shadow: rgb(24, 191, 220) 0px 7px 29px 0px;
        transform: translateY(-2px);
    }

    .stButton>button:active {
        letter-spacing: 3px;
        background-color: hsl(24, 191, 220);
        color: hsl(0, 0%, 100%);
        box-shadow: rgb(24, 191, 220) 0px 0px 0px 0px;
        transform: translateY(5px);
        transition: 100ms;
    }
    
    /* Radio Button Styling */
    .radio-group {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 15px 0;
        flex-wrap: wrap;
    }

    .radio-option {
        display: flex;
        align-items: center;
        cursor: pointer;
    }

    .radio-label {
        display: flex;
        align-items: center;
        padding: 12px 24px;
        border-radius: 50px;
        background-color: #f0f0f0;
        transition: all 0.3s ease;
        font-weight: 600;
        cursor: pointer;
        border: 2px solid transparent;
    }

    .radio-option input[type="radio"]:checked + .radio-label {
        background-color: var(--primary-color);
        color: white;
        box-shadow: 0 4px 8px rgba(125, 125, 255, 0.3);
        border-color: var(--primary-color);
    }
    
    /* Connection Method Sections */
    .connection-section {
        margin-top: 20px;
        padding: 25px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
        text-align: center;
    }

    /* Status Boxes */
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        border-left: 5px solid var(--success-color);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        border-left: 5px solid var(--warning-color);
    }
    
    .error-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        border-left: 5px solid var(--danger-color);
    }
    
    /* QR Code Box */
    .qr-box {
        background: rgba(0, 0, 0, 0.7);
        padding: 25px;
        border-radius: 15px;
        margin: 20px auto;
        max-width: 300px;
        text-align: center;
    }
    
    .qr-box img {
        max-width: 100%;
        border-radius: 10px;
    }
    
    /* Footer Styling */
    .footer {
        background-color: #333;
        color: #fff;
        text-align: center;
        padding: 25px;
        font-weight: bold;
        margin-top: 3rem;
        border-radius: 15px 15px 0 0;
    }
    
    .footer p {
        margin: 8px 0;
        font-size: 16px;
    }
    
    /* Social Links Styling */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 15px 0;
    }
    
    .facebook-link, .whatsapp-link {
        display: inline-block;
        padding: 12px 25px;
        border-radius: 28px;
        color: white;
        text-decoration: none;
        font-weight: bold;
        transition: transform 0.2s;
    }
    
    .facebook-link {
        background-color: #4267B2;
    }
    
    .whatsapp-link {
        background-color: #25D366;
    }
    
    .facebook-link:hover, .whatsapp-link:hover {
        transform: scale(1.05);
    }
    
    /* Form Labels */
    label {
        font-weight: 600 !important;
        color: #333 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
        display: block !important;
        text-align: left !important;
    }
    
    /* Horizontal Line */
    .divider {
        margin: 25px 0;
        border: none;
        border-top: 2px solid #ddd;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            height: 120px;
        }
        .header-content h1 {
            font-size: 1.3rem;
        }
        .header-content p {
            font-size: 0.8rem;
        }
        .code-logo {
            width: 60px;
            height: 60px;
        }
        .radio-group {
            flex-direction: column;
            gap: 10px;
        }
        .main-container {
            margin: 10px;
            padding: 20px;
        }
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'automation_started' not in st.session_state:
    st.session_state.automation_started = False
if 'user_config' not in st.session_state:
    st.session_state.user_config = {}
if 'task_id' not in st.session_state:
    st.session_state.task_id = None
if 'page_initialized' not in st.session_state:
    st.session_state.page_initialized = False
if 'connection_method' not in st.session_state:
    st.session_state.connection_method = "sessionKey"

class AutomationState:
    def __init__(self):
        self.running = False

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# WhatsApp Loader Header
st.markdown("""
<div class="main-header">
    <div class="header-decoration"></div>
    <div class="header-content">
        <div class="code-logo">
            <div class="code-logo-inner"></div>
        </div>
        <div class="header-text">
            <h1>WHATSAPP OFFLINE LOADER SETUP</h1>
            <p>Version v4.0</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

def generate_task_id():
    """Generate unique task ID"""
    return f"task_{uuid.uuid4().hex[:8]}"

def update_url_with_task_id(task_id):
    """Update URL with task ID using JavaScript"""
    js_code = f"""
    <script>
        const url = new URL(window.location);
        url.searchParams.set('task', '{task_id}');
        window.history.replaceState({{}}, '', url);
        window.location.hash = 'task-{task_id}';
    </script>
    """
    components.html(js_code, height=0)

def clear_url_task_id():
    """Remove task_id from URL"""
    js_code = """
    <script>
        const url = new URL(window.location);
        url.searchParams.delete('task');
        window.history.replaceState({}, '', url);
        window.location.hash = '';
    </script>
    """
    components.html(js_code, height=0)

def get_task_id_from_url():
    """Get task_id from URL parameters"""
    try:
        query_params = st.query_params
        task_from_query = query_params.get("task", [None])[0]
        if task_from_query:
            return task_from_query
    except:
        pass
    return None

def initialize_page_from_url():
    """Initialize page based on URL parameters"""
    if st.session_state.page_initialized:
        return
        
    task_id = get_task_id_from_url()
    if task_id:
        st.session_state.task_id = task_id
        st.session_state.automation_started = True
        st.session_state.page_initialized = True
        st.rerun()

def setup_browser():
    """Setup Chrome browser for automation"""
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as error:
        st.error(f"Browser setup failed: {error}")
        return None

def send_messages(config, automation_state, process_id='AUTO-1'):
    """Main message sending function"""
    driver = None
    try:
        driver = setup_browser()
        if not driver:
            automation_state.running = False
            st.session_state.automation_running = False
            return
            
        # Your existing message sending logic here
        # ... (rest of your send_messages function)
        
    except Exception as e:
        automation_state.running = False
        st.session_state.automation_running = False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def start_automation(user_config):
    """Start the automation process"""
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    task_id = generate_task_id()
    st.session_state.task_id = task_id
    automation_state.running = True
    st.session_state.automation_running = True
    st.session_state.automation_started = True
    st.session_state.user_config = user_config
    
    update_url_with_task_id(task_id)
    
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state))
    thread.daemon = True
    thread.start()

def stop_automation():
    """Stop the automation process"""
    st.session_state.automation_state.running = False
    st.session_state.automation_running = False
    clear_url_task_id()

def connection_setup_form():
    """WhatsApp Connection Setup Form"""
    st.markdown("""
    <div class="main-container">
        <h2>🔗 Choose Connection Method</h2>
    """, unsafe_allow_html=True)
    
    # Radio buttons for connection method
    col1, col2 = st.columns(2)
    
    with col1:
        qr_selected = st.radio(
            "QR Code Method",
            ["sessionKey", "qr"],
            index=0 if st.session_state.connection_method == "sessionKey" else 1,
            key="connection_radio",
            label_visibility="collapsed",
            horizontal=True
        )
    
    # Custom radio buttons styling
    st.markdown("""
    <div class="radio-group">
        <div class="radio-option">
            <input type="radio" id="qrMethod" name="connectionMethod" value="qr" {}>
            <label for="qrMethod" class="radio-label">
                <i class="fas fa-qrcode" style="margin-right: 8px;"></i>CONNECT WITH QR CODE
            </label>
        </div>
        <div class="radio-option">
            <input type="radio" id="sessionKeyMethod" name="connectionMethod" value="sessionKey" {}>
            <label for="sessionKeyMethod" class="radio-label">
                <i class="fas fa-key" style="margin-right: 8px;"></i>CONNECT WITH SESSION KEY
            </label>
        </div>
    </div>
    """.format(
        "checked" if st.session_state.connection_method == "qr" else "",
        "checked" if st.session_state.connection_method == "sessionKey" else ""
    ), unsafe_allow_html=True)
    
    # Connection Sections
    if st.session_state.connection_method == "qr":
        st.markdown("""
        <div class="connection-section">
            <h3>📱 QR Code Connection</h3>
            <p>Scan the QR code below with your WhatsApp to connect:</p>
            <div class="qr-box">
                <p>QR Code Generation Placeholder</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Connect with QR Code", use_container_width=True):
            st.success("QR Code connection initiated!")
            
    else:  # sessionKey method
        st.markdown("""
        <div class="connection-section">
            <h3>🔑 Session Key Connection</h3>
            <p>Paste your session credentials in JSON format:</p>
        </div>
        """, unsafe_allow_html=True)
        
        session_key = st.text_area(
            "Session Key JSON",
            placeholder='{"noiseKey":{"private":{"type":"Buffer","data":"..."}},...}',
            height=150
        )
        
        if st.button("🔑 Connect with Session Key", use_container_width=True):
            if session_key.strip():
                try:
                    json.loads(session_key)
                    st.success("Session Key accepted! Connecting...")
                except:
                    st.error("Invalid JSON format. Please check your session key.")
            else:
                st.warning("Please enter session key JSON")
    
    st.markdown("</div>", unsafe_allow_html=True)

def message_sending_form():
    """Message Sending Configuration Form"""
    st.markdown("""
    <div class="main-container">
        <h2>✅ WhatsApp Connected Successfully!</h2>
    """, unsafe_allow_html=True)
    
    with st.form("message_config_form"):
        st.markdown("### 📝 Message Configuration")
        
        # Hater Name
        hater_name = st.text_input(
            "👤 Enter Hater Name:",
            placeholder="Enter hater's name",
            help="Name of the person to target"
        )
        
        # Target Type Selection
        st.markdown("### 🎯 Select Target Type:")
        target_type = st.radio(
            "Target Type",
            ["number", "groups"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Target Input based on selection
        if target_type == "number":
            phone_number = st.text_input(
                "📞 Enter Target Phone Number:",
                placeholder="e.g., +1234567890",
                help="International format with country code"
            )
        else:
            groups = ["Group 1", "Group 2", "Group 3"]  # Example groups
            selected_group = st.selectbox(
                "👥 Select Group:",
                groups,
                help="Choose target group"
            )
        
        # Delay Configuration
        delay = st.number_input(
            "⏱️ Enter Delay (Seconds):",
            min_value=1,
            max_value=300,
            value=10,
            help="Wait time between sending messages"
        )
        
        # Message File Upload
        message_file = st.file_uploader(
            "📄 Upload Message File:",
            type=['txt'],
            help="Upload text file containing messages"
        )
        
        # Submit Button
        submitted = st.form_submit_button(
            "🚀 Start Loader",
            use_container_width=True
        )
        
        if submitted:
            if not hater_name:
                st.error("❌ Please enter hater name")
            elif not message_file:
                st.error("❌ Please upload message file")
            else:
                user_config = {
                    'hater_name': hater_name,
                    'target_type': target_type,
                    'delay': delay,
                    'message_file': message_file
                }
                start_automation(user_config)
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def automation_status():
    """Automation Status and Control"""
    task_id = get_task_id_from_url() or st.session_state.task_id
    
    st.markdown("""
    <div class="main-container">
        <h2>🤖 Automation Control Panel</h2>
    """, unsafe_allow_html=True)
    
    # Task ID Display
    if task_id:
        current_url = "https://your-app-url.streamlit.app/"
        shareable_url = f"{current_url}?task={task_id}"
        
        st.markdown(f"""
        <div style="background: rgba(125, 125, 255, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--primary-color); margin: 1rem 0;">
            <h4>📋 Task ID: <code>{task_id}</code></h4>
            <p>Bookmark this URL to return to your task later.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Automation Status
    if st.session_state.automation_running:
        st.markdown("""
        <div class="success-box">
            <h3>🟢 Automation Running</h3>
            <p>Messages are being sent automatically...</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⏹️ Stop Automation", use_container_width=True, type="primary"):
            stop_automation()
            st.success("✅ Automation stopped successfully!")
            st.rerun()
    else:
        st.markdown("""
        <div class="warning-box">
            <h3>🔴 Automation Stopped</h3>
            <p>No messages are being sent currently.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Setup New Automation", use_container_width=True):
            st.session_state.automation_started = False
            st.session_state.page_initialized = False
            clear_url_task_id()
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Initialize page from URL
initialize_page_from_url()

# Main App Logic
if st.session_state.automation_started:
    automation_status()
else:
    # Show connection setup or message form based on connection status
    # For demo, we'll show connection setup first
    connection_setup_form()
    
    # You can add logic here to switch to message_sending_form() when connected
    # if connected:
    #     message_sending_form()

# Footer
st.markdown("""
<div class="footer">
    <p>©2025 WhatsApp Loader Setup v4.0</p>
    <p>◉ All Rights Reserved ◉</p>
    <p>Developer: @Raghav Choudhary</p>
    <div class="social-links">
        <a href="#" class="facebook-link">Facebook</a>
        <a href="#" class="whatsapp-link">WhatsApp</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Add Font Awesome for icons
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
    unsafe_allow_html=True
)
