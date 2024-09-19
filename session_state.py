import streamlit as st

def init_session_state():
    # ------ Pricing Calculator ------
    if 'pricing_history' not in st.session_state:
        st.session_state['pricing_history'] = {}
    
    if 'pricing_error' not in st.session_state:
        st.session_state['pricing_error'] = None
    
    
    # ------ Usage Tracker ------
    if 'subscription' not in st.session_state:
        st.session_state['subscription'] = None
    
    if 'key_usage' not in st.session_state:
        st.session_state['key_usage'] = None
    
    if 'usage_logs' not in st.session_state:
        st.session_state['usage_logs'] = None
    
    if 'tracker_error' not in st.session_state:
        st.session_state['tracker_error'] = None