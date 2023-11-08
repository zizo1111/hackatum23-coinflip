import streamlit as st

st.set_page_config(page_title="Tips", page_icon="👋", layout='wide')

st.header('Tips and tricks')

desc = """
Some interesting hacks and tricks:

* Redirection of stdout and stderr to th ui.

* Change the UI CSS properties, for example, to modify the space and colorss.

"""

st.markdown(desc)

with st.echo():
    import utils.streamlit_utils as st_utils
    import logging

    st_utils.set_page_container_style(
        max_width=1100,
        max_width_100_percent=True,
        padding_top=3,
        padding_right=3,
        padding_left=2,
        padding_bottom=2,
        color='red',
        background_color='yellow',
    )

    placeholder = st.empty()

    with st_utils.stdout(to=placeholder), st_utils.stderr(to=placeholder):

        print("This must be printed!!")