from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain_cohere import CohereRerank
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_core import embeddings

from dotenv import load_dotenv
import extract, os, time
from pprint import pprint

def format_docs(data : any):
    docs = []

    for item in range(len(data)):
        page = Document(page_content=str(data[item]),
        metadata = {"source": "local", "id" : item})
        docs.append(page)

    return docs

# This turns the Documents into a vectorstore, to be stored locally
def vectorise(docs : list, embeddings):
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./db",
        collection_name="rag-chroma"
    )

    return vectorstore

# Used when vectorstore is stored locally in db
def vector_db(embeddings : any):
    vectorstore = Chroma(
        collection_name="rag-chroma",
        embedding_function=embeddings,
        persist_directory="./db"
    )

    return vectorstore

# Naive retriever and rerank to retrieve data
def compress(api : str, cmp : str, vectorstore : Chroma):
    naive_retriever = vectorstore.as_retriever(search_kwargs={"k" : 10})
    compressor = CohereRerank(top_n=3, cohere_api_key=api, model=cmp)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=naive_retriever
    )

    return compression_retriever

def prompting(model : str, qns : str, retriever : any, message : list):
    prompt = ChatPromptTemplate.from_messages(message)
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | model
    response = rag_chain.invoke(qns)
    
    return response


### RUNNING CODE ###
if __name__ == "__main__":
    start = time.time()

    model = OllamaLLM(model="llama3", temperature=1)
    embeddings = OllamaEmbeddings(model="llama3")
    load_dotenv()
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    data = extract.extracting()
    cmp_model = "rerank-v3.5"

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

    Context:
    {context}
    """

    human_msg = """
    Answer this question using the provided context only: 
    {question}
    """


    data = format_docs(data)
    vectorstore = vectorise(docs=data,embeddings=embeddings)


    # Local extraction from db
    #vectorstore = vector_db(embeddings=embeddings)
    '''
    v = time.time()
    compressor_retrieval = compress(api=COHERE_API_KEY, cmp=cmp_model, vectorstore=vectorstore)

    print(f"Vector: {v-start}s\n")

    
    convo.append(("system", sys_msg))
    convo.append(("human", human_msg))

    while True:
        qns = input(">")
        st = time.time()
        resp = prompting(model, qns, compressor_retrieval, convo)
        r = time.time()

        print(f"Retrieve: {r-st}s\n")
        print(resp + "\n\n")

        convo.append(
            ("ai", resp)
        )
    '''
    
