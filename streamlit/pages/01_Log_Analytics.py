import streamlit as st
from qdrant_client.models import PointStruct
import time
st.set_page_config(page_title="Log Analyser", page_icon="👋", layout='wide')
from difflib import SequenceMatcher
import pandas as pd

if "file" not in st.session_state:
    st.error("Upload a file before proceeding")
#uploaded_file = st.file_uploader("Upload your Log file",type=['.txt',".out"])

num_of_lines_to_embedd = st.slider("Lines to Embedd", min_value=500, max_value=70000, value=1000, step=100)
num_of_chunks = st.slider("Lines to Embedd", min_value=10, max_value=1000, value=20, step=10)

lines = []
clean_lines = []
st.header('Log Analyser')
more_embed = []

tab1, tab2= st.tabs(['File Information', 'Log Explorer'])

tab1.subheader('File Information')

# Calculates embeddings for less
def calc_embed(inhalt):
        start = time.time()
        more_embed = st.session_state.model.encode(inhalt)
        end = time.time()
        return more_embed
        #st.write("Finished embeddings in " ,end-start)

# #Calculates Embeddings for all
def calculate_embeddings(to_encode, collection_name):
    with st.spinner("Calculating embeddings, please wait before proceeding"):
        start = time.time()
        embeddings = st.session_state.qdrant.calculate_embeddings(to_encode, num_of_lines_to_embedd, num_of_chunks)
        st.session_state.qdrant.populate_qdrant(collection_name,embeddings)
        st.session_state['embeddings']=embeddings
        # st.session_state["embeddings"] = st.session_state.model.encode(to_encode)
        end = time.time()
        st.write("Finished embeddings in " ,end-start)
        st.session_state["calculated"] = True

with tab1:
    # sum_chars = 0
    # clean_chars = 0 
    # to_encode = []
    # if "file" in st.session_state:
    #         uploaded_file = st.session_state.file 
    #         name = uploaded_file.name
    #         lines = uploaded_file.readlines()
    #         st.session_state["lines"] = lines
    #         size = uploaded_file.size
    #         st.write("Filename: ", name)
    #         st.write("File size: ", round(size/ (1024 * 1024),3) ,"MB")
    #         st.write("Number of log entries: " , len(lines))
    #         st.session_state.read_file = True
    #         with st.spinner("Pre-processing file"):
    #             with st.spinner("Removing unnecesary characters"):
    #                 for line in st.session_state.lines:
    #                     sum_chars += len(line)
    #                     #if "Got Data" not in str(line):
                            
    #                     line = line.replace(line.split(b': ',2)[0],b'')
    #                     #print(line)
    #                     clean_chars += len(line)
    #                     end_line = str(line).replace("b'", "").replace("\\r","").replace("\\n","").replace(": ","")
    #                     clean_lines.append(str(end_line))

    #             st.write("Total character sum before processing: ",sum_chars)
    #             st.write("Total character sum after processing : ",clean_chars)
    #             st.write("Total line sum before processing: ",len(lines))
    #             st.write("Total line sum after processing : ",len(clean_lines))

        # for i in range(0,num_of_lines_to_embedd, num_of_chunks):
        #     to_encode.append(" ;;; ".join(st.session_state.messages[i:i+num_of_chunks]))
            
        if "calculated" not in st.session_state:
            calculate_embeddings(st.session_state.messages, "my_collection")
        elif(st.session_state.calculated == False):
            calculate_embeddings(st.session_state.messages , "my_collection")

                #st.write(res)


def search_vector(query_vector, hit):
        big_id = hit.id
        inhalt = hit.payload["Inhalt"].split(";;;")
        embed = calc_embed(inhalt)

        st.session_state.client.upsert(
                    collection_name="second_coll",
            points=[
                PointStruct(
                        id=idx,
                        vector=vector.tolist(),
                        payload={"Inhalt": inhalt[idx],"Line_Count": idx + big_id*num_of_chunks+1}
                )
            for idx, vector in enumerate(embed)
        ]
        )
        hits = st.session_state.client.search(
        collection_name="second_coll",
        query_vector=query_vector,
        limit=20  # Return 10 closest points
        )
        return hits

# Main search from all for hits
def search_hits(collection_name, query_vector):
        hits = st.session_state.qdrant.search_collection(collection_name, query_vector, 5)


        for hit in hits:
            st.header("Highest vector similiarity in lines: " + str(hit.id * num_of_chunks)+"-"+str(hit.id * num_of_chunks +num_of_chunks) + " with score " + str(hit.score))
            st.subheader("Top Results of this chunk")

            hits_0 = st.session_state.qdrant.search_vector(query_vector, hit,st.session_state.messages)
            for hit_ in hits_0:
                idx = hit_.payload["line_id"] + hit.id*num_of_chunks
                if hit_.score < 0.5:
                    st.write(":red[Line:] " +str(idx) + " :blue[Message:] " +str(st.session_state.messages[idx]).replace("b'", "").replace("\\r","").replace("\\n",""))
                else:
                    st.warning(":red[Line:] " +str(idx) + " :blue[Message:] " +str(st.session_state.messages[idx]).replace("b'", "").replace("\\r","").replace("\\n",""), icon="⚠️")
        st.write(hits)

        # hits_0 = search_vector(query_vector, hit)
        # for hit in hits_0:
        #     idx = hit.payload["Line_Count"]
        #     if hit.score < 0.5:
        #         st.write(":red[Line:] " +str(idx) + " :blue[Message:] " +str(lines[idx]).replace("b'", "").replace("\\r","").replace("\\n",""))
        #     else:
        #         st.warning(":red[Line:] " +str(idx) + " :blue[Message:] " +str(lines[idx]).replace("b'", "").replace("\\r","").replace("\\n",""), icon="⚠️")


with tab2:
    res = st.text_area(label = "Enter keywords youre interested in", value = "SSH connection error CMX")
    st.session_state['user_query'] = res
    query_vector = st.session_state.model.encode(res.replace("log",""))
    if "embeddings" in st.session_state:
        search_hits("my_collection", query_vector)
