import openai
from langchain.vectorstores import  Pinecone
from tqdm.autonotebook import tqdm
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI

import streamlit as st

from langchain.chains.question_answering import load_qa_chain

import pinecone
import os

### uncomment for running locally #######
# from dotenv import load_dotenv
# if load_dotenv():
#     pinecone_api_key = os.getenv('PINECONE_API_KEY')
#     pinecone_api_env = os.getenv('PINECONE_API_ENV')  
#     OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  


#for streamlit cloud - comment to run locally 
pinecone_api_key = st.secrets["PINECONE_API_KEY"]
pinecone_api_env = st.secrets["PINECONE_API_ENV"]

def init_pinecone(idx_name = "oracleexadatadocs"):
    #pinecone index name
    index_name = idx_name

    # initialize pinecone
    pinecone.init(
        api_key=pinecone_api_key,  # find at app.pinecone.io
        environment=pinecone_api_env  # next to api key in console
    )
    
    index = pinecone.Index(index_name)
    return index

    
def openAI_get_response(index ,message, openai_api_key,model = "gpt-3.5-turbo" ):
    
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key) #model = model
    except Exception:
        st.error("Please enter a valid Open API")
        

    docsearch = Pinecone(index, embeddings.embed_query, 'text')
    docs = docsearch.similarity_search(message, include_metadata=True)
    
    try:
        llm = OpenAI(temperature=0, openai_api_key=openai_api_key) #model_name= model
    except Exception:
        st.error("Please enter a valid Open API")
        
    chain = load_qa_chain(llm, chain_type="stuff")

    docs = docsearch.similarity_search(query=message)
    response = chain.run(input_documents=docs, question=message)
    return response


def get_initial_message():
    
    messages=[
            {"role": "system", "content": " You are an expert Oracel database administrator.\
            you are well aware about oracle database administration , maintenance , installation and security procedure \
            and standards. you provide step-by-step procedure as answer for user queries."},
            {"role": "user", "content": "during the planned outage, what is the procedures for powering on and off the components?"}, 
            {"role": "assistant", "content": "use Non-emergency Power Procedures  for powering on and off the components of Oracle Exadata Rack in an orderly fashion.\
                1. Powering On Oracle Exadata Rack, procedure for that is ,\
                    The power on sequence is as follows: \
                        a. Rack, including switches. \
                        Ensure the switches have had power applied for a few minutes to complete power-on configuration before starting Exadata Storage Servers.\
                        b. Exadata Storage Servers. \
                         Ensure all Exadata Storage Servers complete the boot process before starting the \
                        c. database servers. This may take five to ten minutes before all services start. \
                        Database servers.\
                2. Powering On Servers Remotely using ILOM- Servers can be powered on remotely using the Integrated Lights Out Manager (ILOM) interface.  \
                3. Powering Off Oracle Exadata Rack- Power off the components of the Oracle Exadata Rack in the correct order. \
                4.  Powering On and Off Network Switches    "}
            
        ]
    
    
        # messages=[
        #     {"role": "system", "content": "You are a helpful AI Tutor. Who anwers brief questions about AI."},
        #     {"role": "user", "content": "I want to learn AI"},
        #     {"role": "assistant", "content": "Thats awesome, what do you want to know aboout AI"}
        # ]
    return messages

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def get_chatgpt_response(messages, model='gpt-3.5-turbo'):
    print("model: ", model)
    
    # response = openai.ChatCompletion.create(
    # model=model,
    # messages=messages, 
    # temperature = 0  
    # )
    # return  response['choices'][0]['message']['content']



