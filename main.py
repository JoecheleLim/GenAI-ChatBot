import streamlit as st
import os 
from setup_st import (
    set_desgin, 
    initiallise_session_state, 
    get_user_config, 
    sidebar, 
    clear_button, 
    download_button
)
from index_functions import load_data, generate_response_index
from helper_functions import generate_response

# 1. Setup UI/UX elements
set_desgin()
initiallise_session_state()
sidebar()
get_user_config()
clear_button()
download_button()

# 2. Initialise Data and Chat Engine
if st.session_state.get('api_key'):
    try: 
        index = load_data(st.session_state.api_key) 
        if index and "chat_engine" not in st.session_state:
            st.session_state.chat_engine = index.as_chat_engine(
                chat_mode="condense_question", 
                streaming=True
            )
    except Exception as e:
        st.error(f'Error initializing AI engine: {e}')
else:
    st.info("Please enter your Gemini API Key in the sidebar to activate the chatbot.")
    
if not st.session_state.get('use_index', False):
    st.sidebar.warning('Index is disabled. Chatbot using general knowledge.')

# 3. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        
# 4. Chat Input & AI Processing 
if prompt := st.chat_input("How can the Glorious help you today?"):
    
    # Save user message immediately
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    # Display user message so it shows up while the assistant works
    with st.chat_message('user'):
        st.markdown(prompt)
        
    with st.chat_message('assistant'):
        status_placeholder = st.empty()
        
        # A. Process and show status
        with status_placeholder.status("Glorious is thinking...", expanded=False) as status:
            facts = ""
            if st.session_state.get('use_index', False) and "chat_engine" in st.session_state:
                st.write("Searching local documentation...")
                facts = generate_response_index(st.session_state.chat_engine, prompt)
            else:
                st.write("Consulting general knowledge...")
            
            st.write("Synthesizing answer...")
            status.update(label="Information retrieved!", state="complete", expanded=False)
        
        # B. Clear the status box right before generating text
        status_placeholder.empty() 

        # C. Generate and Stream response
        try:
            augmented_prompt = f"Facts from Documentation: {facts}\n\nUser Question: {prompt}"
            
            response_generator = generate_response(
                prompt=augmented_prompt,
                history=st.session_state.messages[:-1], 
                model_name=st.session_state.model_name,
                temperature=st.session_state.temperature,
                api_key=st.session_state.api_key
            )
            
            # This streams the text directly into the UI
            full_response = st.write_stream(response_generator)
            
            # D. Save to history ONLY after completion
            st.session_state.messages.append({'role': 'assistant', 'content': full_response})
            st.session_state.message_count = st.session_state.get('message_count', 0) + 1
            
            # E. Rerun to lock the history and clear any temporary UI states
            st.rerun() 
                
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")