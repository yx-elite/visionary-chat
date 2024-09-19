import os, time
import streamlit as st
import pandas as pd
from datetime import datetime
from backend.usage import (
    retrieve_model_info, calculate_model_pricing, retrieve_key_usage_details
)
from utils import Logger


# Initialize logging
module_name = os.path.basename(__file__).split('.')[0]
log = Logger(logger_name=module_name, log_level='info')
logger = log.get_logger()

st.header("API Usage")

tab1_pricing_calculator, tab2_usage_tracker = st.tabs([
    "1\. 📊 - Pricing Calculator - ",
    "2\. 📈 - Usage Tracker - "
])

# ------ Pricing Calculator ------
with tab1_pricing_calculator:
    model_infos = retrieve_model_info()
    token_based_models = [
        model_info['model_name']
        for model_info in model_infos['data']
        if model_info['available'] == True and model_info['quota_type'] == 0
    ]
    
    # User input form for model pricing calculation
    with st.form("Pricing Calculator Form", clear_on_submit=False, border=False):
        model_option = st.selectbox(
            label="Model",
            options=sorted(token_based_models),
            index=37   # gpt-4o-mini
        )
        col1, col2 = st.columns(2)
        with col1:
            input_token = st.number_input(
                label="Input Tokens",
                min_value=0,
                max_value=None,
                step=10,
                value=0
            )
        with col2:
            output_token = st.number_input(
                label="Output Tokens",
                min_value=0,
                max_value=None,
                step=10,
                value=0
            )
        st.caption('_Note:_ Choose a model tailored to your usage or preference. For detailed information, refer to the "Available Models" section.')
        submitted_pricing = st.form_submit_button("Check Usage Pricing", type='secondary')
    
    # Create placeholder to store results
    pc_status_placeholder = st.empty()
    pc_result_placeholder = st.empty()
    
    # Actions after form submission
    if submitted_pricing:
        pc_status_placeholder.empty()
        pc_result_placeholder.empty()
        time.sleep(0.5)
        try:
            usage_pricing = calculate_model_pricing(model_option, input_token, output_token, model_infos=model_infos)
            pc_status_placeholder.success("Usage pricing has been calculated successfully!", icon=':material/task_alt:')
            # disp_usage_pricing = math.ceil(usage_pricing*1e6) / 1e6
            
            # Display calculated model pricing based on tokens
            with pc_result_placeholder.container():
                with st.expander("Computed Result", expanded=True, icon=':material/expand_circle_down:'):
                    st.markdown(f"""
                        > - *Model :* `{model_option}`
                        > - *Input Tokens :* `{input_token}`
                        > - *Output Tokens :* `{output_token}`
                        ---
                        ##### Usage Pricing : ${usage_pricing:.6f}
                        """)
        except Exception as e:
            st.error("Error calculating usage pricing. Please contact the administrator to report this issue.", icon=':material/error:')


# ------ Usage Tracker ------
with tab2_usage_tracker:
    col1, col2 = st.columns([0.85, 0.15], vertical_alignment='bottom')
    with col1:
        api_key = st.text_input(
            label="Visionary AI API Key",
            type='default',
            placeholder="e.g. sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Please claim your free API KEY or purchase via XXX"
        )
    with col2:
        submitted_tracker = st.button("Submit", type='secondary', use_container_width=True, help="Track API Usage")
    st.caption("_Note:_ Your API key is not stored on our website in any form. For transparency, please ensure it is deleted after use.")
    
    # Create placeholder to store results
    tc_status_placeholder = st.empty()
    tc_usage_placeholder = st.empty()
    tc_token_info_placeholder = st.empty()
    tc_log_placeholder = st.empty()
    
    # Actions after API key submission
    if submitted_tracker:
        tc_status_placeholder.empty()
        tc_usage_placeholder.empty()
        tc_token_info_placeholder.empty()
        tc_log_placeholder.empty()
        
        with st.spinner("Token usage is being calculated..."):
            try:
                subscription, key_usage, usage_logs = retrieve_key_usage_details(api_key=api_key)
                st.session_state['subscription'] = subscription
                st.session_state['key_usage'] = key_usage
                st.session_state['usage_logs'] = usage_logs
                st.session_state['tracker_error'] = None
            except:
                st.session_state['tracker_error'] = "Unable to calculate token usage. Please verify that the API Key is entered correctly."
                logger.warning(st.session_state['tracker_error'])
    
    # Display the results from session state if available
    if st.session_state['tracker_error']:
        tc_status_placeholder.error(st.session_state['tracker_error'], icon=':material/error:')
    
    elif st.session_state['subscription'] and st.session_state['key_usage']:
        subscription = st.session_state['subscription']
        key_usage = st.session_state['key_usage']
        usage_logs = st.session_state['usage_logs']
        
        total_limit = subscription.get('soft_limit_usd', 99999)
        total_usage = key_usage.get('total_usage', 99999)
        
        # Check there is presence of errors
        if total_limit != 99999 and total_usage != 99999:
            total_usage = total_usage / 100  # Conversion
            remainder = total_limit - total_usage
            
            logger.info("Token usage has been calculated successfully!")
            tc_status_placeholder.success(
                "Token usage has been calculated successfully!", icon=':material/task_alt:'
            )
            usage_bar = tc_usage_placeholder.progress(
                remainder / total_limit,
                text=f"Current Usage: &nbsp;&nbsp;&nbsp;\\${remainder:.2f} / \\${total_limit:.2f}"
            )
            
            with tc_token_info_placeholder.container():
                with st.expander("API Key Information", expanded=True, icon=':material/expand_circle_down:'):
                    key_status = 'Inactive' if total_limit == 0 else "Active"
                    st.markdown(f"""
                        > - *Total Limit :* `{total_limit:.3f}`
                        > - *Total Usage :* `{total_usage:.3f}`
                        > - *Status :* `{key_status}`
                        > - *Expiration :* `None`
                        ---
                        ##### Remainding Quota : ${remainder:.3f}
                        """)
            
            with tc_log_placeholder.container():
                with st.expander("Usage History", expanded=True, icon=':material/history:'):
                    usage_log_details = usage_logs.get('data')
                    
                    # If there is any usage history
                    if len(usage_log_details) >= 1:
                        usage_log_df = pd.DataFrame([
                            {
                                "Created At": datetime.fromtimestamp(log['created_at']).strftime('%Y-%m-%d %H:%M:%S'),
                                "API Key": log['token_name'],
                                "Model": log['model_name'],
                                "Response Time": log['use_time'],
                                "Input Tokens": log['prompt_tokens'],
                                "Output Tokens": log['completion_tokens'],
                                "Total Costs": log['quota'] * 2e-6
                            }
                            for log in usage_log_details
                        ])
                        usage_log_df = usage_log_df.sort_values(by='Created At', ascending=False)
                        pd.options.display.float_format = '{:.6f}'.format
                    else:
                        # If there is no usage history
                        usage_log_df = pd.DataFrame(columns = ["Created At", "API Key", "Model", "Response Time", "Input Tokens", "Output Tokens", "Total Costs"])
                    
                    st.dataframe(
                        usage_log_df, 
                        use_container_width=True, 
                        hide_index=True,
                        column_config={
                            "Total Costs": st.column_config.NumberColumn(
                                format="$ %.6f"
                            )
                        }
                    )
        else:
            st.session_state['tracker_error'] = "Error calculating token usage. Please contact the administrator to report this issue."
            # Handle the tracker error on runtime
            tc_status_placeholder.error(st.session_state['tracker_error'], icon=':material/error:')
            logger.error(st.session_state['tracker_error'])