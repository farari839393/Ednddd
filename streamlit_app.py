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
    page_title="E2E Automation",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background-image: url('https://i.postimg.cc/TYhXd0gG/d0a72a8cea5ae4978b21e04a74f0b0ee.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .main-header h1 {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .prince-logo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin-bottom: 15px;
        border: 3px solid #4ecdc4;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.5);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        background: rgba(255, 255, 255, 0.2);
        border-color: #4ecdc4;
        box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.2);
        color: white;
    }
    
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
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
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        margin-top: 3rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .status-running {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    .status-stopped {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    .task-id-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4ecdc4;
        margin: 1rem 0;
    }
    
    .url-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #4ecdc4;
        margin: 1rem 0;
        word-break: break-all;
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

class AutomationState:
    def __init__(self):
        self.running = False

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

def generate_task_id():
    """Generate unique task ID"""
    return f"task_{uuid.uuid4().hex[:8]}"

def update_url_with_task_id(task_id):
    """Update URL with task ID using JavaScript"""
    js_code = f"""
    <script>
        // Method 1: Update query parameters
        const url = new URL(window.location);
        url.searchParams.set('task', '{task_id}');
        window.history.replaceState({{}}, '', url);
        
        // Method 2: Also update hash for better visibility
        window.location.hash = 'task-{task_id}';
        
        console.log('URL updated with task ID: {task_id}');
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
        # Try to get from query parameters first
        query_params = st.query_params
        task_from_query = query_params.get("task", [None])[0]
        
        if task_from_query:
            return task_from_query
        
        # If not in query params, try to get from hash
        if st.experimental_get_query_params().get('_hash'):
            hash_value = st.experimental_get_query_params().get('_hash')[0]
            if hash_value and hash_value.startswith('task-'):
                return hash_value.replace('task-', '')
                
    except Exception as e:
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
        
        delay = int(config['delay'])
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
                
                time.sleep(delay)
                
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
    
    # Generate unique task ID
    task_id = generate_task_id()
    st.session_state.task_id = task_id
    
    automation_state.running = True
    st.session_state.automation_running = True
    st.session_state.automation_started = True
    
    st.session_state.user_config = user_config
    
    # Update URL with task ID
    update_url_with_task_id(task_id)
    
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state))
    thread.daemon = True
    thread.start()

def stop_automation():
    st.session_state.automation_state.running = False
    st.session_state.automation_running = False
    # Clear task ID from URL when stopping
    clear_url_task_id()

def main_form():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.postimg.cc/Pq1HGqZK/459c85fcaa5d9f0762479bf382225ac6.jpg" class="prince-logo">
        <h1>🩷E2E Automation System</h1>
        <p>Automate your Facebook messages with ease</p>
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
                st.rerun()

def automation_status():
    # Get task ID from URL or session state
    task_id = get_task_id_from_url() or st.session_state.task_id
    
    st.markdown("""
    <div class="main-header">
        <img src="https://i.postimg.cc/Pq1HGqZK/459c85fcaa5d9f0762479bf382225ac6.jpg" class="prince-logo">
        <h1>🤖 Automation Control</h1>
        <p>Control your message automation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show task ID and shareable URL
    if task_id:
        current_url = "https://ednddd-zgyghxav6siuys4jyn2sti.streamlit.app/"
        shareable_url = f"{current_url}?task={task_id}"
        
        st.markdown(f"""
        <div class="task-id-box">
            <h4>📋 Task ID: <code>{task_id}</code></h4>
            <p>You can bookmark this URL to return to this task later.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="url-box">
            <h4>🔗 Shareable URL:</h4>
            <code>{shareable_url}</code>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.automation_running:
        st.markdown("""
        <div class="status-running">
            <h2>🟢 Automation Running</h2>
            <p>Messages are being sent automatically...</p>
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
        
        st.markdown("---")
        st.markdown("### 🔄 Setup New Automation")
        
        if st.button("🔄 Back to Setup", key="back_btn", use_container_width=True):
            st.session_state.automation_started = False
            st.session_state.page_initialized = False
            clear_url_task_id()
            st.rerun()

# Initialize page from URL parameters
initialize_page_from_url()

# Main app logic
if st.session_state.automation_started:
    automation_status()
else:
    main_form()

st.markdown('<div class="footer">E2E Automation System | © 2025</div>', unsafe_allow_html=True)
