import streamlit as st
import os
import base64

# 1. Set up the page's layout and design elements
def set_desgin():

    # Convert local image to Base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Load logo 
    try:
        img_base64 = get_base64_image("logo.png")
    except Exception:
        img_base64 = ""


    l_spacer, center_area, r_spacer = st.columns([1, 1, 1])

    with center_area:
        # 3. Combined HTML with Base64 Image (No Title)
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{img_base64}" style="width: 200px; height: auto;">
            </div>
            """, 
            unsafe_allow_html=True
        )
    
# 2. Initialise session state variables
def initiallise_session_state():
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {'role': 'assistant', 'content': 'Hi there, how can I help you today?'}
        ]
    
    if 'message_count' not in st.session_state:
        st.session_state['message_count'] = 0

    # Default to Gemini 1.5 Flash
    if 'model_name' not in st.session_state:
        st.session_state['model_name'] = 'models/gemini-1.5-flash'
    
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = 0.7
    
    if 'use_index' not in st.session_state:
        st.session_state['use_index'] = False
    
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = ""

# 3. Sidebar Container
def sidebar():
    st.sidebar.markdown("<h1 style='font-size: 24px;'>Glorious Config</h1>", unsafe_allow_html=True)

# 4. Clear Conversation Logic
def clear_button():
    if st.sidebar.button('Clear Conversation', key='clear', use_container_width=True):
        st.session_state['messages'] = [
            {'role': 'assistant', 'content': 'Hi there! How can I help you today?'}
        ]
        st.session_state['message_count'] = 0
        st.rerun() 

# 5. Helper for formatting download data
def prepare_download_data():
    if len(st.session_state['messages']) > 1:
        full_conversation = ""
        for msg in st.session_state['messages']:
            full_conversation += f"{msg['role'].upper()}: {msg['content']}\n{'-'*30}\n"
        return full_conversation
    return None

# 6. Download Button UI
def download_button():
    data = prepare_download_data()
    if data:
        st.sidebar.download_button(
            label='Download Conversation',
            data=data,
            file_name='conversation.txt',
            mime='text/plain',
            use_container_width=True
        )

# 7. User Configuration Inputs (Updated for Gemini)
def get_user_config():
    # Updated mapping for Gemini Models
    model_options = {
        'Gemini 3 Flash (Latest)': 'models/gemini-3-flash-preview',
        'Gemini 2.5 Flash (Stable)': 'models/gemini-2.5-flash',
        'Gemini 2.5 Pro': 'models/gemini-2.5-pro'
    }
    
    st.sidebar.subheader("Model Settings")
    
    # Model Selection
    model_label = st.sidebar.selectbox('Select AI Model:', list(model_options.keys()))
    st.session_state['model_name'] = model_options[model_label]
    
    # Temperature
    st.sidebar.markdown(f"**Temperature:** {st.session_state.temperature}")
    st.session_state['temperature'] = st.sidebar.slider(
        'Randomness Control', 
        min_value=0.0, max_value=1.0, value=0.7, step=0.1,
        label_visibility="collapsed"
    )
    
    # API Key - Updated label for Google AI Studio
    st.sidebar.markdown("**Google API Key**")
    api_key_input = st.sidebar.text_input(
        'Gemini API Key', 
        type='password', 
        placeholder="Enter your Google AI Studio key here...",
        label_visibility="collapsed"
    )
    
    if api_key_input:
        st.session_state['api_key'] = api_key_input
    
    # Index Toggle
    st.sidebar.markdown("---")
    st.session_state['use_index'] = st.sidebar.checkbox(
        'Enable PDF Context', 
        value=st.session_state.get('use_index', False)
    )