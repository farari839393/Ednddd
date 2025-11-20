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
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

# Create data directory if it doesn't exist
DATA_DIR = Path("automation_data")
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="E2E Automation Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with artistic elements
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: #6c757d;
        font-size: 1.2rem;
        margin-top: 0;
        font-weight: 400;
    }
    
    .automation-logo {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        margin-bottom: 20px;
        border: 4px solid #fff;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        margin: 0 auto 20px;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-top: 2rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        color: #333;
        padding: 0.85rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        background: white;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        color: #333;
    }
    
    label {
        color: #495057 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .success-box {
        background: linear-gradient(135deg, #4cd964 0%, #5ac8fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 5px 15px rgba(76, 217, 100, 0.3);
    }
    
    .error-box {
        background: linear-gradient(135deg, #ff2d55 0%, #ff3b30 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 5px 15px rgba(255, 59, 48, 0.3);
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.75rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        margin-top: 3rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .status-running {
        background: linear-gradient(135deg, #4cd964 0%, #5ac8fa 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(76, 217, 100, 0.3);
    }
    
    .status-stopped {
        background: linear-gradient(135deg, #ff9500 0%, #ff5e3a 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(255, 149, 0, 0.3);
    }
    
    .stop-button {
        background: linear-gradient(135deg, #ff3b30 0%, #ff2d55 100%) !important;
        font-size: 1.1rem !important;
        padding: 1rem 2rem !important;
        margin: 1rem 0;
    }
    
    .back-button {
        background: linear-gradient(135deg, #5ac8fa 0%, #007aff 100%) !important;
        font-size: 1.1rem !important;
        padding: 1rem 2rem !important;
        margin: 1rem 0;
    }
    
    .config-display {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .timing-input {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .timing-input input {
        flex: 1;
    }
    
    .section-header {
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 0.75rem;
        margin-bottom: 1.5rem;
        color: #495057;
        font-weight: 600;
        font-size: 1.3rem;
    }
    
    .data-file-list {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .file-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .file-item:last-child {
        border-bottom: none;
    }
    
    .file-name {
        font-weight: 500;
        color: #495057;
    }
    
    .file-date {
        font-size: 0.85rem;
        color: #6c757d;
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
if 'saved_configs' not in st.session_state:
    st.session_state.saved_configs = []

class AutomationState:
    def __init__(self):
        self.running = False
        self.config_id = None

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

def log_message(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def save_config_to_file(user_config):
    """Save configuration to JSON file"""
    config_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    config_data = {
        'config_id': config_id,
        'timestamp': timestamp,
        'user_config': user_config,
        'status': 'active'
    }
    
    filename = f"automation_config_{config_id}_{timestamp}.json"
    filepath = DATA_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    return config_id, filename

def load_config_from_file(filename):
    """Load configuration from JSON file"""
    filepath = DATA_DIR / filename
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        log_message(f"Error loading config {filename}: {e}")
        return None

def get_saved_configs():
    """Get list of all saved configuration files"""
    config_files = []
    for file in DATA_DIR.glob("automation_config_*.json"):
        try:
            with open(file, 'r') as f:
                config_data = json.load(f)
                config_files.append({
                    'filename': file.name,
                    'config_id': config_data.get('config_id', 'Unknown'),
                    'timestamp': config_data.get('timestamp', 'Unknown'),
                    'status': config_data.get('status', 'unknown')
                })
        except Exception as e:
            log_message(f"Error reading config file {file}: {e}")
    
    # Sort by timestamp, newest first
    config_files.sort(key=lambda x: x['timestamp'], reverse=True)
    return config_files

def find_message_input(driver, process_id):
    log_message(f'{process_id}: Finding message input...')
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            return element
                        elif idx < 10:
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            return element
                except Exception:
                    continue
        except Exception:
            continue
    
    return None

def setup_browser():
    log_message('Setting up Chrome browser...')
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}')
        raise error

def get_next_message(messages, message_rotation_index=0):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    message = messages[message_rotation_index % len(messages)]
    return message

def send_messages(config, automation_state, process_id='AUTO-1'):
    driver = None
    try:
        driver = setup_browser()
        
        log_message(f'{process_id}: Navigating to Facebook...')
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies'] and config['cookies'].strip():
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id)
        
        if not message_input:
            automation_state.running = False
            st.session_state.automation_running = False
            return
        
        # Get timing configuration for each message
        timing_config = config.get('message_timing', {})
        default_delay = int(config['delay'])
        
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        message_rotation_index = 0
        
        while automation_state.running:
            base_message = get_next_message(messages_list, message_rotation_index)
            message_rotation_index += 1
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            # Get custom delay for this message if specified
            message_delay = timing_config.get(base_message, default_delay)
            
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                        
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                
                time.sleep(message_delay)
                
            except Exception as e:
                time.sleep(5)
        
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
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    st.session_state.automation_running = True
    
    # Save configuration to file
    config_id, filename = save_config_to_file(user_config)
    automation_state.config_id = config_id
    st.session_state.user_config = user_config
    
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state))
    thread.daemon = True
    thread.start()

def stop_automation():
    st.session_state.automation_state.running = False
    st.session_state.automation_running = False

def main_form():
    st.markdown("""
    <div class="main-header">
        <div class="automation-logo">🤖</div>
        <h1>E2E Automation Pro</h1>
        <p>Professional Message Automation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show saved configurations
    saved_configs = get_saved_configs()
    if saved_configs:
        with st.expander("📁 Saved Configurations", expanded=False):
            st.markdown("### Previously Saved Automations")
            for config in saved_configs[:5]:  # Show only 5 most recent
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**ID:** {config['config_id']}")
                with col2:
                    st.markdown(f"**Date:** {config['timestamp']}")
                with col3:
                    if st.button("Load", key=f"load_{config['config_id']}"):
                        loaded_config = load_config_from_file(config['filename'])
                        if loaded_config:
                            st.session_state.loaded_config = loaded_config['user_config']
                            st.rerun()
    
    with st.form("automation_form"):
        st.markdown("""
        <div class="section-header">
            🔧 Automation Configuration
        </div>
        """, unsafe_allow_html=True)
        
        # Check if we have a loaded config
        if 'loaded_config' in st.session_state:
            loaded_config = st.session_state.loaded_config
            del st.session_state.loaded_config
        else:
            loaded_config = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            chat_id = st.text_input(
                "Chat/Conversation ID *", 
                value=loaded_config.get('chat_id', ''),
                placeholder="e.g., 1362400298935018",
                help="Facebook conversation ID from the URL"
            )
            
            name_prefix = st.text_input(
                "Name Prefix", 
                value=loaded_config.get('name_prefix', ''),
                placeholder="e.g., [E2E]",
                help="Prefix to add before each message"
            )
            
            delay = st.number_input(
                "Default Delay (seconds) *", 
                min_value=1, 
                max_value=300, 
                value=loaded_config.get('delay', 10),
                help="Default wait time between sending messages"
            )
        
        with col2:
            cookies = st.text_area(
                "Facebook Cookies *", 
                value=loaded_config.get('cookies', ''),
                placeholder="Paste your Facebook cookies here...",
                height=120,
                help="Your Facebook authentication cookies"
            )
            
            messages = st.text_area(
                "Messages to Send *", 
                value=loaded_config.get('messages', ''),
                placeholder="Enter each message on a new line...",
                height=150,
                help="Enter each message on a separate line"
            )
        
        # Message timing configuration
        st.markdown("""
        <div class="section-header">
            ⏱️ Message Timing Configuration
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <p><strong>Custom Timing:</strong> Specify custom delays for specific messages. 
            For each message you want to customize, enter the exact message text and the delay in seconds.</p>
        </div>
        """, unsafe_allow_html=True)
        
        timing_config = {}
        if messages:
            message_list = [msg.strip() for msg in messages.split('\n') if msg.strip()]
            if len(message_list) > 0:
                st.markdown("**Set custom delays for messages:**")
                
                # Create 2 columns for message timing inputs
                cols = st.columns(2)
                for i, msg in enumerate(message_list):
                    col_idx = i % 2
                    with cols[col_idx]:
                        timing = st.number_input(
                            f"Delay for: '{msg[:30]}{'...' if len(msg) > 30 else ''}'",
                            min_value=1,
                            max_value=300,
                            value=delay,
                            key=f"timing_{i}"
                        )
                        timing_config[msg] = timing
        
        submitted = st.form_submit_button(
            "🚀 Start Automation", 
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not chat_id or not cookies or not messages:
                st.error("❌ Please fill all required fields (Chat ID, Cookies, and Messages)")
            else:
                user_config = {
                    'chat_id': chat_id,
                    'name_prefix': name_prefix,
                    'delay': delay,
                    'cookies': cookies,
                    'messages': messages,
                    'message_timing': timing_config
                }
                
                start_automation(user_config)
                st.session_state.automation_started = True
                st.rerun()

def automation_status():
    st.markdown("""
    <div class="main-header">
        <div class="automation-logo">⚙️</div>
        <h1>Automation Control Center</h1>
        <p>Monitor and control your message automation</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.automation_running:
        st.markdown("""
        <div class="status-running">
            <h2>🟢 Automation Running</h2>
            <p>Messages are being sent automatically according to your configuration</p>
            <p><strong>Config ID:</strong> {}</p>
        </div>
        """.format(st.session_state.automation_state.config_id), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Show current configuration
        st.markdown("### 📋 Current Configuration")
        user_config = st.session_state.user_config
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="config-display">
                <p><strong>Chat ID:</strong> {user_config.get('chat_id', 'N/A')}</p>
                <p><strong>Name Prefix:</strong> {user_config.get('name_prefix', 'None')}</p>
                <p><strong>Default Delay:</strong> {user_config.get('delay', 'N/A')} seconds</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            messages_count = len([msg for msg in user_config.get('messages', '').split('\n') if msg.strip()])
            st.markdown(f"""
            <div class="config-display">
                <p><strong>Messages Configured:</strong> {messages_count}</p>
                <p><strong>Custom Timings:</strong> {len(user_config.get('message_timing', {}))}</p>
                <p><strong>Config ID:</strong> {st.session_state.automation_state.config_id}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🛑 Stop Automation")
        
        if st.button("⏹️ Stop Automation", key="stop_btn", use_container_width=True, type="primary"):
            stop_automation()
            st.success("✅ Automation stopped successfully!")
            time.sleep(1)
            st.rerun()
            
    else:
        st.markdown("""
        <div class="status-stopped">
            <h2>🔴 Automation Stopped</h2>
            <p>No messages are being sent currently.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🔄 Setup New Automation")
        
        if st.button("🔄 Back to Setup", key="back_btn", use_container_width=True):
            st.session_state.automation_started = False
            st.rerun()

# Check for saved configurations on startup and auto-start if any exist
def check_and_auto_start():
    saved_configs = get_saved_configs()
    if saved_configs and not st.session_state.automation_running:
        # Auto-start the most recent configuration
        latest_config = saved_configs[0]
        config_data = load_config_from_file(latest_config['filename'])
        if config_data:
            st.info(f"🔄 Auto-starting previous configuration: {latest_config['config_id']}")
            start_automation(config_data['user_config'])
            st.session_state.automation_started = True
            st.rerun()

# Main app logic
if not st.session_state.automation_started:
    # Check for auto-start on initial load
    if not st.session_state.automation_running:
        check_and_auto_start()
    main_form()
else:
    automation_status()

st.markdown("""
<div class="footer">
    E2E Automation Pro | Professional Message Automation System | © 2025
</div>
""", unsafe_allow_html=True)
