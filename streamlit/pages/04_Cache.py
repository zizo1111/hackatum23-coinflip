import streamlit as st

st.set_page_config(page_title="Cache", page_icon="👋", layout='wide')

st.header('Streamlit Cache')

desc = """
Streamlit can cache the results of a long process, allowing to speed up the app.

There exists two ways: with th `@st.cache` decorator (see https://docs.streamlit.io/library/advanced-features/caching),
and with the new experimental @st.experimental_memo and @st.experimental_singleton 
(see https://docs.streamlit.io/library/advanced-features/experimental-cache-primitives)

In this example, the first time a button is clicked the function will be run, and the results will be cached.

The second time it is clicked, it will look for the cached results of a call with the same arguments, and return it

"""

st.markdown(desc)

col1, col2 = st.columns(2)

with col1:
    with st.echo():
        import time as time
        
        @st.experimental_memo
        def slooooooooow_function(secs):
            time.sleep(secs)
            return f'Return value: {secs}!'


        button_5 = col2.button('Run it for 5 seconds!')
        button_3 = col2.button('Run it for 3 seconds!')

        clear_button = col2.button("Clear the cache!")
        if clear_button:
            slooooooooow_function.clear()

        placeholder = col2.empty()
            
        if button_5:
            placeholder.empty()
            placeholder.write(slooooooooow_function(5))

        if button_3:
            placeholder.empty()
            placeholder.write(slooooooooow_function(3))