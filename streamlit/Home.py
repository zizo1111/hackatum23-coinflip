import streamlit as st
from PIL import Image
import os
import time

st.write("# Welcome to the CoinFlip Log Analyser")

### XXX  Load the vetor database Qdrant in memory

with st.spinner("Initilaizing in-memory Qdrant vector database for the session"):
    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient, models
    from qdrant_client.models import PointStruct
    client  = QdrantClient(":memory:")
    client.create_collection("my_collection", vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE) )
    st.session_state["client"] = client
    st.session_state["model"] = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


st.sidebar.success("Database and model loaded in memory")
st.write("Qdrant Database initiliaized in memory")
