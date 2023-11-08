import streamlit as st
from PIL import Image


st.set_page_config(page_title="Streamlit Code Snippets",
                   page_icon="👋",
                   layout='wide')

st.write("# Welcome to the Streamlit Code Snippet 👋")
st.write("We start the app by runnning the home page with:")
st.code("streamlit run Home.py")

st.write(
    "The app project structure contains the main page py file, and a folder called pages, with other subpages py files."
)

image = Image.open('snippet_tree.png')

st.image(image)

st.write(
    "They all are rendered in the navigation panel on top of the sidebar.")
st.write(
    "Make sure to name the subpages correctly by indicating the order on the beginning of the name."
)

st.write(
    "All pages can set their title, icon and default layout format (wide or centered) plus other default behaviour (initial sidebar state, menu items...)"
)
st.code(""" 
import streamlit as st

# As first st command in the page:
st.set_page_config(page_title="Streamlit Code Snippets",
                       page_icon="👋",
                       layout='wide')

st.write(......)

""")

st.sidebar.success("Select a page above.")

st.markdown("""
    Navigate throught the different pages on the navigation panel on the left
""")