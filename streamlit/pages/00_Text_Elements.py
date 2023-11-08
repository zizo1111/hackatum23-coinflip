import streamlit as st

st.set_page_config(page_title="Text Elements",
                   page_icon="👋",
                   layout='wide')

st.header('Text Elements')
st.write("First, import streamlit!!")
st.code("import streamlit as st")

with st.echo():
    st.write("You can use st.write for almost everything")
    st.title("This is a title")
    st.header("This is a header")
    st.subheader("This is a subheader")
    st.caption("This is a caption")
    st.markdown("You can enter markdown **_Content_** :smiley:")
    st.write("st.echo will show the code in the app, AND run it, not like st.code, which just format text")
    st.code("""with st.echo:
    code = function(arg)
    """)    


st.header('Text Elements')
with st.echo():
    st.sidebar.info("This is an info message on the sidebar.")
    st.sidebar.success("This is an Success message on the sidebar.")
    st.sidebar.warning("This is an Warning message on the sidebar.")




    
