import streamlit as st
from PIL import Image
import os
import time

st.title("CoinFlip Log Analyser")

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

uploaded_file = st.file_uploader("Upload your Log file",type=['.txt',".out"])

if uploaded_file is not None and "file" not in st.session_state:
    st.session_state["file"] = uploaded_file
    st.success("File uploaded successfully")

# uploaded_file = st.file_uploader("Upload your Log file",type=['.txt',".out"])
# lines = None
# clean_lines = []
# st.header('Log Analyser')

# tab1, tab2, tab3, tab4 = st.tabs(['File Information', 'Questions and Answers', 'Pre-processing', "Empty containers"])

# tab1.subheader('File Information')



# with tab1:
#     sum_chars = 0
#     clean_chars = 0 
#     if uploaded_file is not None:  
#             st.sidebar.success("File uploaded successfully")
#             name = uploaded_file.name
#             lines = uploaded_file.readlines()
#             size = uploaded_file.size
#             st.write("Filename: ", name)
#             st.write("File size: ", round(size/ (1024 * 1024),3) ,"MB")
#             st.write("Number of log entries: " , len(lines))
#             st.session_state.read_file = True
#             with st.spinner("Pre-processing file"):
#                 with st.spinner("Processing file "):
#                     for line in lines:
#                         sum_chars += len(line)
#                         line = line.replace(line.split(b': ',2)[0],b'')
#                         #print(line)
#                         clean_chars += len(line)
#                         clean_lines.append(str(line))
#                 st.write("Total character sum before processing: ",sum_chars)
#                 st.write("Total character sum after processing : ",clean_chars)
#             with st.spinner("Caluclating embedings"):
#                 embeddings = model.encode(clean_lines)



# with tab2:
#     res = st.text_area("Ask your questions here")
#     if res is not None :
#         st.write(res)

# tab3.subheader('Pre processing')

# tab4.subheader('Empty containers')

# with tab4:
#     with st.echo():
#         st.write("You can create placeholders and empty them when desired")
#         placeholder = st.empty()
#         fill_button = st.button("Fill the empty container")
#         clean_button = st.button("Empty the container")
#         if fill_button:
#             placeholder.subheader("We are filling something here")
#         if clean_button:
#             placeholder.empty()

#         st.info("This must appear below the container")



# st.sidebar.success("Select a page above.")