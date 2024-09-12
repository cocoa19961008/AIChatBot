import streamlit as st
import os
import random
from groq import Groq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

groq_api_key = ""

def main():

    css = '''
    <style>
        .st-emotion-cache-1yiq2ps {
            padding-bottom: 6%;
        }
        .st-emotion-cache-13ln4jf {
            max-width: 70%;
            width: 100%;
            padding: 6rem 1rem 10rem;
        }
        .st-emotion-cache-bm2z3a {
            align-items: left !important;
        }
        .stAppViewBlockContainer{
            margin: 0px !important;
            padding: 0px !important;
        }
        header {
            display: none !important;
        }
        div.css-1om1ktf.e1y61itm0 {
          display: none !important;
        }
        .element-container:has(>.stTextArea), .stTextArea {
            width: 100% !important;
            z-index: 1000 !important;
            position: fixed !important;
            bottom: 0 !important;
            margin-bottom: 20px !important;
            width: 62.5% !important;
            left: 14.5% !important;
            border: 0px solid #D3D3D3 !important;
        }
        .stTextArea textarea {
            height: 42px !important;
            min-height: 42px !important;
            padding: 8px 8px !important;
            border: 0px solid #D3D3D3 !important;
        }
        .stButton {
            position: fixed !important;
            bottom: 0 !important;
            left: 76% !important;
            padding: 0px 20px !important;
            align-items: center !important;
            justify-content: center !important;
            margin-bottom: 20px !important;
            width: 100% !important;
        }
        .stButton button {
            width: 12.5px !important;
            padding: 8px 20px !important;
            background-color: #D3D3D3 !important;
            color: white !important;
            background-color: black !important;
            border: none !important;
            border-radius: 14px !important;
            cursor: pointer!important;
            z-index: 1000 !important;
        }
        .stButton button:hover {
            background-color: #151922 !important;
            color: white !important;
            box-shadow: 0 0 0 0.1rem grey !important;
        }
        .e1f1d6gn2 > :nth-child(n+5):nth-child(even):not(:last-child) {
            background-color: #F3F3F3 !important;
            width: fit-content !important;
            color: black !important;
            font-weight: 700 !important;
            padding: 0px 10px !important;
            border-radius: 14px !important;
        }

    </style>
    '''
    st.write(css, unsafe_allow_html=True)

    
    st.title("Testing Chatbot - Dipen")
    # st.sidebar.title("Select an LLM")
    # model = st.sidebar.selectbox(
    #     'Choose a model',
    #     ['Mixtral-8x7b-32768', 'llama3-8b-8192']
    # )

    # conversational_memory_length = st.sidebar.slider('Conversational Memory Length:', 1, 10, value=5)
    model = 'llama3-8b-8192'
    conversational_memory_length = 10

    memory = ConversationBufferMemory(k=conversational_memory_length)

    # Inject custom CSS
    st.markdown("""
        <style>

        .chat-history {
            margin-bottom: 80px;  /* Adjust this value based on the height of your input box */
        }
        .e1f1d6gn2 :nth-child(5) {
            display: none !important;
        }

        </style>
        """, unsafe_allow_html=True)

    user_question = st.text_area("", key="chat_input", height=100, placeholder="type your question here" )

    # Session state variables
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input': message['human']}, {'output': message['AI']})

    groq_chat = ChatGroq(
        groq_api_key= groq_api_key,
        model_name = model
    )

    conversation = ConversationChain(
        llm = groq_chat,
        memory = memory
    )

    # Display chat history
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        st.write(f"**You:** {message['human']}")
        st.write(f"**ChatBot:** {message['AI']}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("↑") or user_question:
        if user_question:
            response = conversation(user_question)
            message = {"human": user_question, "AI": response['response']}
            st.session_state.chat_history.append(message)
            st.write(f"**ChatBot:** {response['response']}")

            
    # if user_question:
    #     response = conversation(user_question)
    #     message = {"human": user_question, "AI": response['response']}
    #     st.session_state.chat_history.append(message)
    #     st.write(f"**ChatBot:** {response['response']}")




if __name__ == "__main__":
    main()
