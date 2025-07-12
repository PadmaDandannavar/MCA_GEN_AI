import streamlit as st
from utils import get_openai_response


st.set_page_config(page_title="GEN AI CHATBOT", page_icon="") #set page title
st.title("GENERATIVE AI CHATBOT")
#set title for page

#initialise session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 
if "input_key"  not in st.session_state:
    st.session_state.input_key =  0

 #display chat history first

if st.session_state.chat_history:
    st.subheader("Conversation History")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message['content'])
        else:
            with st.chat_message("assistant"):
                st.write(message['content'])
else:
    st.info("Welcome !! Start a conversation by typing a message below:")

#chat Interface with formto handle Submission properly

with st.form(key="chat_form",clear_on_submit=True):
    user_input = st.text_input("Type your message here:", placeholder="Ask me Anything....",key=f"input_{st.session_state.input_key}")
    submit_button = st.form_submit_button("SEND...")

if submit_button and user_input and user_input.strip():
    with st.spinner(" Thinking....."):
        try:
            response, updated_history = get_openai_response(user_input, st.session_state.chat_history)
            st.session_state.chat_history = updated_history
            st.session_state.input_key += 1  # Fixed this line
            st.rerun()  # Fixed this line
        except Exception as e:
            st.error(f" Error : {str(e)}")
            st.error("Please check your OpenAI Key and internet Connection")

