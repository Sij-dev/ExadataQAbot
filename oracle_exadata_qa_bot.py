import streamlit as st
from streamlit_chat import message
import os
import openai_util


st.set_page_config(page_title="OracleExaData-QA-bot", page_icon=":robot:")
st.header("Ask your question about Oracle Exadata installation, configuration and maintenance")
st.markdown("##### based on 'Oracle Admin guides (installaion, configuration and maintenance guide'")
st.divider()

##### Get Open AI API Key from User
st.markdown("Provide your OpenAI API Key - check out this to get OpenAI API Key. \
        [link](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)")
def get_api_key():
    input_text = st.text_input(label= "Open API Key", 
        placeholder="Ex: sk-2twmA8tfCb8un4...",
        key="openai_api_key_input")

    return input_text

openai_api_key = get_api_key() 

if len(openai_api_key) <= 25:
    st.error("give a valid Open API key to proceed")
else:    

# model = st.selectbox(
#     "Select a model",
#     ("gpt-3.5-turbo (default)", "gpt-4 (make sure you have access to this model)","text-davinci-003","text-ada-001")
# )

        ## pinecone init
    index_name = "oracleexadatadocs"
    pincone_index = openai_util.init_pinecone(index_name)


    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
        

    query = st.text_input("Ask your question about consciousness,destiny,freedom,spirtual anatomy etc.: ", key="input")
    #print(query)

    if 'messages' not in st.session_state:
        st.session_state['messages'] = openai_util.get_initial_message()
        #print(st.session_state['messages'])
        
    if query:
        with st.spinner("generating..."):
            messages = st.session_state['messages']
            messages = openai_util.update_chat(messages, "user", query)
            response = openai_util.openAI_get_response(pincone_index,query,openai_api_key)
            #print(response)
            
            #response = openai_util.get_chatgpt_response(messages,model)
            messages = openai_util.update_chat(messages, "assistant", response)
            st.session_state.past.append(query)
            st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
     

# with st.expander("Show Messages"):
#     st.write(st.session_state['messages'])
    