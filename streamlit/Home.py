import streamlit as st
from PIL import Image
import os
import time
import sys
parent_dir = os.path.dirname(os.path.realpath("src"))
sys.path.append(parent_dir)
from src import qdrant
from src import db_creator
from src import db_connector


st.title("CoinFlip Log Analyser")

### XXX  Load the vector database Qdrant in memory

with st.spinner("Initilaizing in-memory Qdrant vector database for the session"):
    qdrantt = qdrant.Qdrant()
    st.session_state["client"] = qdrantt.client
    st.session_state["model"] = qdrantt.model
    st.session_state["qdrant"] = qdrantt
    db_cr = db_creator.DBCreator()


st.sidebar.success("Database and model loaded in memory")
st.write("Qdrant Database initiliaized in memory")

uploaded_file = st.file_uploader("Upload your Log file",type=['.txt',".out"])

if uploaded_file is not None and "file" not in st.session_state:
    with st.spinner("Initilaizing SQLite Database"):
        st.session_state["file"] = uploaded_file
        print(uploaded_file.name)
        db_path = db_cr.run('/home/hackathon26/omar/hackatum23-coinflip/data/'+uploaded_file.name )
        db_conn = db_connector.DBConnector(db_path)
        db_conn.connect()
        st.session_state["db_connector"] = db_conn
        messages = db_conn.query_col('message')
        for idx,message in enumerate(messages):
            if "Got Data" in message:
                messages[idx] = ""

        st.session_state["messages"] = messages
        st.success("File uploaded successfully")