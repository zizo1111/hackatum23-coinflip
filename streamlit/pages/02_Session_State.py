import streamlit as st

st.set_page_config(page_title="Session State", page_icon="👋", layout='wide')

st.header('Session State')

st.write("One key point of Streamlit is that when an interaction with widgets happens, the full script is run from the top.")
st.write("Session state is used to share variables between reruns for each user session.")

tab1, tab2 = st.tabs(['Problem', 'Solution'])   

tab1.subheader("The nested button problem:")
tab1.write("The second button will appear when the first one is clicked. But when clicking it we expect to change the text")
tab1.write("The problem is that on a rerun, the first button state will be lost, so the second button will disappear.")

with tab1:
    with st.echo():
        placeholder = tab1.empty()
        
        if tab1.button('Button 1'):
            tab1.write("You cliked the first buttton")
            if tab1.button('Button 2'):
                placeholder.empty()
                placeholder.write("You cliked the second buttton")

tab2.subheader("Solution to the nested button problem:")
tab2.write("We need to keep the previous run state on the session.")

with tab2:
    with st.echo():
        placeholder_2 = tab2.empty()

        def init_session_states():
            if 'b1_clicked' not in st.session_state:
                st.session_state.b1_clicked = False

        def callback_function_b1():
            st.session_state.b1_clicked = True
        
        init_session_states()

        if tab2.button('Button 1', key='b1_ok', on_click=callback_function_b1) or st.session_state.b1_clicked:
            placeholder_2.write("You cliked the first buttton")
            if tab2.button('Button 2', key='b2_ok'):
                placeholder_2.empty()
                placeholder_2.write("You cliked the second buttton")


        def init_session_states():
            del st.session_state.b1_clicked

        clean_button = st.button('Reset solution to initial state', on_click=init_session_states)