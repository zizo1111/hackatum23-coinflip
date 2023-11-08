import streamlit as st

st.set_page_config(page_title="Layout", page_icon="👋", layout='wide')

st.header('Layout')

with st.echo():
    tab1, tab2, tab3, tab4 = st.tabs(['Container', 'Columns', 'Expander', "Empty containers"])

tab1.subheader('Object notation and "with" notation')
tab1.write(
    "This applies to any layout container: sidebar, expanders, tabs, columns..."
)

with tab1:
    with st.echo():
        container = tab1.container()
        container.write("This will be written in container")

        with container:
            st.write("This will be written in the container also!")

tab2.subheader('Controls in the Sidebar, effects in the columns')

with tab2:
    with st.echo():
        with tab2:
            selected_option = st.sidebar.selectbox(
                "Select a column here!",
                options=['Column 1', 'Column 2'],
                help="Select the column where the text should be displayed")

            col1, col2 = st.columns(2)
            if selected_option == "Column 1":
                col1.header('The text is in column 1')
            else:
                col2.header('The text is in column 2')

tab3.subheader('Expanders')
with tab3:
    with st.echo():
        selected_value = st.sidebar.radio(
            "Select a value here!",
            options=['Value 1', 'Value 2'],
            help="Select the value to be displayed in the expander")

        with tab3.expander("The expander", expanded=True):
            st.success(f'The value selected in the radiobuttons is {selected_value}')

tab4.subheader('Empty containers')

with tab4:
    with st.echo():
        st.write("You can create placeholders and empty them when desired")
        placeholder = st.empty()
        fill_button = st.button("Fill the empty container")
        clean_button = st.button("Empty the container")
        if fill_button:
            placeholder.subheader("We are filling something here")
        if clean_button:
            placeholder.empty()

        st.info("This must appear below the container")
