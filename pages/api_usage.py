import time
import streamlit as st
import pandas as pd
from datetime import datetime
from backend.usage import retrieve_model_info, calculate_model_pricing


st.header("API Usage")

tab1_pricing_calculator, tab2_usage_tracker = st.tabs([
    "1\. 📊 - Pricing Calculator - ",
    "2\. 📈 - Usage Tracker -"
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
        submitted = st.form_submit_button("Check Usage Pricing", type='secondary')
    
    # Create placeholder to store results
    pc_status_placeholder = st.empty()
    pc_result_placeholder = st.empty()
    
    # Actions after form submission
    if submitted:
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
    