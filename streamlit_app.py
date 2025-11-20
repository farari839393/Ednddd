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

# Set up data directory for JSON persistence
DATA_DIR = Path("automation_data")
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="E2E Automation",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional artistic CSS style
custom_css = """
<style>
    /* Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
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
        color: #333;
    }
    
    .main .block-container {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        box-sizing: border-box;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 4px 15px rgba(0,0,0,.1);
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
        border-radius: 10px;
        margin-bottom: 20px;
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
    
    .code-logo-inner::before {
        content: '</>';
        position: absolute;
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
    
    /* Input and Form Styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        color: green;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 50px;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
        height: 50px;
        outline: none;
        border: 0.1px solid #ccc;
        font-size: 1rem;
        box-sizing: border-box;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    .stTextArea>div>div>textarea {
        height: 140px;
        resize: none;
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
        width: 100%;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        letter-spacing: 4px;
        background-color: rgb(24, 191, 220);
        color: hsl(0, 0%, 100%);
        box-shadow: rgb(24, 191, 220) 0px 7px 29px 0px;
    }
    
    .stButton>button:active {
        letter-spacing: 3px;
        background-color: hsl(24, 191, 220);
        color: hsl(0, 0%, 100%);
        box-shadow: rgb(24, 191, 220) 0px 0px 0px 0px;
        transform: translateY(10px);
        transition: 100ms;
    }
    
    /* Status Boxes */
    .status-running {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    .status-stopped {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(0, 0, 0, 0.7);
        font-weight: 600;
        margin-top: 3rem;
        background: rgba(0, 0, 0, 0.05);
        border-radius: 10px;
        border-top: 1px solid rgba(0, 0, 0, 0.15);
    }
    
    /* Form Labels */
    label {
        color: #333 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        text-align: left !important;
        display: block;
        margin-bottom: 8px;
    }
    
    /* Section Headers */
    h3 {
        color: var(--dark-color);
        margin-bottom: 15px;
        font-weight: 700;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 8px;
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
if 'automation_threads' not in st.session_state:
    st.session_state.automation_threads = {}

class AutomationState:
    def __init__(self, user_id):
        self.running = False
        self.user_id = user_id

def get_user_id():
    """Generate a unique user ID based on session state"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    return st.session_state.user_id

def save_user_data(user_id, user_config, conversation_data=None):
    """Save user data to JSON file"""
    data = {
        'user_id': user_id,
        'user_config': user_config,
        'conversation_data': conversation_data or {},
        'timestamp': time.time()
    }
    
    file_path = DATA_DIR / f"{user_id}.json"
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_user_data(user_id):
    """Load user data from JSON file"""
    file_path = DATA_DIR / f"{user_id}.json"
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return None

def load_all_automations():
    """Load all saved automations from JSON files"""
    automations = []
    for file_path in DATA_DIR.glob("*.json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            automations.append(data)
    return automations

def log_message(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

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
    user_id = automation_state.user_id
    
    # Save initial state
    save_user_data(user_id, config, {"status": "starting", "process_id": process_id})
    
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
            save_user_data(user_id, config, {"status": "failed", "reason": "message_input_not_found"})
            return
        
        delay = int(config['delay'])
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        message_rotation_index = 0
        
        # Save running state
        save_user_data(user_id, config, {"status": "running", "messages_sent": 0})
        
        while automation_state.running:
            base_message = get_next_message(messages_list, message_rotation_index)
            message_rotation_index += 1
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
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
                
                # Update message count
                user_data = load_user_data(user_id)
                if user_data and 'conversation_data' in user_data:
                    messages_sent = user_data['conversation_data'].get('messages_sent', 0) + 1
                    save_user_data(user_id, config, {"status": "running", "messages_sent": messages_sent})
                
                time.sleep(delay)
                
            except Exception as e:
                time.sleep(5)
        
        # Save stopped state
        save_user_data(user_id, config, {"status": "stopped"})
        
    except Exception as e:
        automation_state.running = False
        st.session_state.automation_running = False
        save_user_data(user_id, config, {"status": "error", "error": str(e)})
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def start_automation(user_config):
    user_id = get_user_id()
    
    if user_id in st.session_state.automation_threads:
        if st.session_state.automation_threads[user_id].running:
            return
    
    automation_state = AutomationState(user_id)
    st.session_state.automation_threads[user_id] = automation_state
    
    automation_state.running = True
    st.session_state.automation_running = True
    
    st.session_state.user_config = user_config
    
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state, f"AUTO-{user_id[:8]}"))
    thread.daemon = True
    thread.start()
    
    # Save initial configuration
    save_user_data(user_id, user_config, {"status": "starting"})

def stop_automation():
    user_id = get_user_id()
    
    if user_id in st.session_state.automation_threads:
        st.session_state.automation_threads[user_id].running = False
    
    st.session_state.automation_running = False
    
    # Update status in saved data
    user_data = load_user_data(user_id)
    if user_data:
        save_user_data(user_id, user_data['user_config'], {"status": "stopped"})

def restart_automations():
    """Restart all automations from saved JSON files"""
    automations = load_all_automations()
    
    for automation in automations:
        user_id = automation['user_id']
        user_config = automation['user_config']
        status = automation.get('conversation_data', {}).get('status', 'unknown')
        
        # Only restart if it was running when saved
        if status == 'running':
            log_message(f"Restarting automation for user {user_id}")
            start_automation(user_config)

def main_form():
    st.markdown("""
    <div class="main-header">
        <div class="header-decoration"></div>
        <div class="header-content">
            <div class="code-logo">
                <div class="code-logo-inner"></div>
            </div>
            <div class="header-text">
                <h1>E2E Automation System</h1>
                <p>Automate your Facebook messages with ease</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("automation_form"):
        st.markdown("### 🔧 Automation Configuration")
        
        chat_id = st.text_input(
            "Chat/Conversation ID *", 
            placeholder="e.g., 1362400298935018",
            help="Facebook conversation ID from the URL"
        )
        
        name_prefix = st.text_input(
            "Name Prefix", 
            placeholder="e.g., [E2E]",
            help="Prefix to add before each message"
        )
        
        delay = st.number_input(
            "Delay between messages (seconds) *", 
            min_value=1, 
            max_value=300, 
            value=10,
            help="Wait time between sending messages"
        )
        
        cookies = st.text_area(
            "Facebook Cookies *", 
            placeholder="Paste your Facebook cookies here...",
            height=100,
            help="Your Facebook authentication cookies"
        )
        
        messages = st.text_area(
            "Messages to Send *", 
            placeholder="Enter each message on a new line...",
            height=150,
            help="Enter each message on a separate line"
        )
        
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
                    'messages': messages
                }
                
                start_automation(user_config)
                st.session_state.automation_started = True
                st.rerun()

def automation_status():
    st.markdown("""
    <div class="main-header">
        <div class="header-decoration"></div>
        <div class="header-content">
            <div class="code-logo">
                <div class="code-logo-inner"></div>
            </div>
            <div class="header-text">
                <h1>🤖 Automation Control</h1>
                <p>Control your message automation</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show current automation status
    user_id = get_user_id()
    user_data = load_user_data(user_id)
    
    if st.session_state.automation_running:
        messages_sent = 0
        if user_data and 'conversation_data' in user_data:
            messages_sent = user_data['conversation_data'].get('messages_sent', 0)
            
        st.markdown(f"""
        <div class="status-running">
            <h2>🟢 Automation Running</h2>
            <p>Messages are being sent automatically...</p>
            <p><strong>Messages Sent:</strong> {messages_sent}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🛑 Stop Automation")
        
        if st.button("⏹️ Stop Automation", key="stop_btn", use_container_width=True, type="primary"):
            stop_automation()
            st.success("✅ Automation stopped successfully!")
            st.rerun()
            
    else:
        st.markdown("""
        <div class="status-stopped">
            <h2>🔴 Automation Stopped</h2>
            <p>No messages are being sent currently.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show previous run stats if available
        if user_data and 'conversation_data' in user_data:
            messages_sent = user_data['conversation_data'].get('messages_sent', 0)
            if messages_sent > 0:
                st.info(f"Last run sent {messages_sent} messages")
        
        st.markdown("---")
        st.markdown("### 🔄 Setup New Automation")
        
        if st.button("🔄 Back to Setup", key="back_btn", use_container_width=True):
            st.session_state.automation_started = False
            st.rerun()

# Check for and restart any saved automations on startup
if 'automations_restarted' not in st.session_state:
    restart_automations()
    st.session_state.automations_restarted = True

# Main app logic
if not st.session_state.automation_started:
    main_form()
else:
    automation_status()

st.markdown('<div class="footer">E2E Automation System | © 2025</div>', unsafe_allow_html=True)
