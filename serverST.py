'''
Where the streamlit server is stored and response is displayed in WebUI 
'''

import streamlit as st
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_core import embeddings
import os, extract, mainMemory, time
from dotenv import load_dotenv


model = OllamaLLM(model="llama3", temperature=1)
embeddings = OllamaEmbeddings(model="llama3")
load_dotenv()
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
data = extract.extracting()
cmp_model = "rerank-v3.5"

# Retrieving vectorstore and compression
vectorstore = mainMemory.vector_db(embeddings=embeddings)
compressor_retrieval = mainMemory.compress(api=COHERE_API_KEY, cmp=cmp_model, vectorstore=vectorstore)

convo = []

sys_msg = """
The documentation supplied to you is in the format of a Python Dictionary, below are the explanations of each Key and Value pairs:
-Component is the name of the project
-Description is the general description of the project
-The next few pairs comprised of subheaders and pointers, subheaders are the names of specific parts of the components and the pointers are the information that you will be giving the user.

Subheaders and their pointers are directly linked to the components.
If you cannot answer the question, let the user know.
The user is an administrator, thus all knowledge available to you must be supplied to the user if required.
Be concise with your response.
Format your answer if possible

Context:
{context}
"""

human_msg = """
Answer this question using the provided context only: 
{question}
"""

# History
convo.append(("system", sys_msg))
convo.append(("human", human_msg))

### WebUI ###

# Streaming
def resp_gen():
    resp = mainMemory.prompting(model, text, compressor_retrieval, convo)

    for word in resp.split():
        yield word + " "
        time.sleep(0.05)


st.title("GAO Internal GPT")

# Display history of conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Checking if message box is empty
if text := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": text})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(text)
    
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = st.write_stream(resp_gen())

    st.session_state.messages.append({"role": "assistant", "content": response})
