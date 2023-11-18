import streamlit as st
from qdrant_client.models import PointStruct
import time
st.set_page_config(page_title="Log Analyser", page_icon="👋", layout='wide')


uploaded_file = st.file_uploader("Upload your Log file",type=['.txt',".out"])
num_of_lines_to_embedd = st.slider("Lines to Embedd", min_value=500, max_value=70000, value=1000, step=100)
num_of_chunks = st.slider("Lines to Embedd", min_value=10, max_value=1000, value=20, step=10)

lines = None
clean_lines = []
to_encode = []
st.header('Log Analyser')
more_embed = []

if "model" not in st.session_state or "client not in st.session_state":
    with st.spinner("Initilaizing in-memory Qdrant vector database for the session"):
        from sentence_transformers import SentenceTransformer
        from qdrant_client import QdrantClient, models
        from qdrant_client.models import PointStruct
        client  = QdrantClient(":memory:")
        client.create_collection("my_collection", vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE) )#COSINE;DOT;EUCLIDEAN
        client.create_collection("second_coll", vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE) )
        st.session_state["client"] = client
        st.session_state["model"] = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

tab1, tab2, tab3, tab4 = st.tabs(['File Information', 'Questions and Answers', 'Pre-processing', "Empty containers"])

tab1.subheader('File Information')

def calc_embed(hits):
        care = hits[0].payload["Inhalt"].split(";;;")
        start = time.time()
        more_embed = st.session_state.model.encode(care)
        end = time.time()
        return more_embed
        #st.write("Finished embeddings in " ,end-start)

def calculate_embeddings():
    with st.spinner("Calculating embeddings, please wait before proceeding"):
        start = time.time()
        st.session_state["embeddings"] = st.session_state.model.encode(to_encode)
        end = time.time()
        st.write("Finished embeddings in " ,end-start)
        st.session_state["calculated"] = True

with tab1:
    sum_chars = 0
    clean_chars = 0 
    if uploaded_file is not None:  
            st.sidebar.success("File uploaded successfully")
            name = uploaded_file.name
            lines = uploaded_file.readlines()
            size = uploaded_file.size
            st.write("Filename: ", name)
            st.write("File size: ", round(size/ (1024 * 1024),3) ,"MB")
            st.write("Number of log entries: " , len(lines))
            st.session_state.read_file = True
            with st.spinner("Pre-processing file"):
                with st.spinner("Removing unnecesary characters"):
                    for line in lines:
                        sum_chars += len(line)
                        if "Got Data" not in str(line):
                            
                            line = line.replace(line.split(b': ',2)[0],b'')
                            #print(line)
                            clean_chars += len(line)
                            end_line = str(line).replace("b'", "").replace("\\r","").replace("\\n","").replace(": ","")
                            clean_lines.append(str(end_line))
                st.write("Total character sum before processing: ",sum_chars)
                st.write("Total character sum after processing : ",clean_chars)
                st.write("Total line sum before processing: ",len(lines))
                st.write("Total line sum after processing : ",len(clean_lines))


                for i in range(0,num_of_lines_to_embedd, num_of_chunks):
                    to_encode.append(" ;;; ".join(clean_lines[i:i+num_of_chunks]))
            if "calculated" not in st.session_state:
                calculate_embeddings()
            elif(st.session_state.calculated == False):
                calculate_embedings()
            
                #st.write(res)
tab2.subheader('Controls in the Sidebar, effects in the columns')



def search_vector(query_vector,hits):
        inhalt = hits[0].payload["Inhalt"].split(";;;")
        embed = calc_embed(hits)

        st.session_state.client.upsert(
                    collection_name="second_coll",
            points=[
                PointStruct(
                        id=idx,
                        vector=vector.tolist(),
                        payload={"Inhalt": inhalt[idx]}
                )
            for idx, vector in enumerate(embed)
        ]
        )
        hits = st.session_state.client.search(
        collection_name="second_coll",
        query_vector=query_vector,
        limit=10  # Return 10 closest points
        )
        print("HITS")
        print(hits)


def search_hits(query_vector):
        st.session_state.client.upsert(
                    collection_name="my_collection",
            points=[
                PointStruct(
                        id=idx,
                        vector=vector.tolist(),
                        payload={"Inhalt": to_encode[idx]}
                )
            for idx, vector in enumerate(st.session_state.embeddings)
        ]
        )
        hits = st.session_state.client.search(
            collection_name="my_collection",
            query_vector=query_vector,
            limit=5  # Return 5 closest points
            )
        print(hits[0].id)

        for hit in hits:
            st.header("Hit number: " + str(hit.id) + " with score " + str(hit.score))
            st.write(hit.payload["Inhalt"])
        

        search_vector(query_vector,hits)
        
        #st.write(hits)


with tab2:
    res = st.text_area(label = "Ask your questions here", value = "Which logs have errors or connection problems")
    query_vector = st.session_state.model.encode(res.replace("log",""))
    if "embeddings" in st.session_state:
        search_hits(query_vector)
