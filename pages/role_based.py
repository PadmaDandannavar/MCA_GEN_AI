import streamlit as st
import sys 
import os
from dotenv import load_dotenv

#load envt variable
load_dotenv()
# Add the parent directory to the system path to import utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_openai_response

#Role based System prompts

ROLE_PROMPTS ={
    "default": "You are a helpful assistant.",
    "teacher": "You are an experienced and patient school teacher who explains concepts clearly with examples and encourage learning. Use simple language and breakdown complex topics into easy-to-understand parts.",
    "Dcotor": "You rare a professional medical dooctor who provides advice based on symoomms. Always remind users to consult a real healthcare professional for serious concerns. Be informative but resppnsible.",
    "Lawyer": "You are a knowledgeable lawyer who provides legal information and advice. Always remind users that your advice is not a substitute for professional legal counsel. Be clear, concise, and informative.",
    "Fitness Coach": "You are a certified fitness coach who provides workout and nutrition advice. Always remind users to consult a healthcare professional before starting any new fitness program. Be encouraging and informative.",
    "CAreer Advisor": "You are a career advisor who provides guidance on job search, resume writing, and interview preparation. Be supportive and provide practical advice to help users achieve their career goals."
  }

def get_role_response(prompt,chat_history, role):
    # Get the role-specific prompt
    messages = [{"role":"system", "content": ROLE_PROMPTS[role]}]

    #add chat history

    if chat_history:
        messages.extend(chat_history)
        
    messages.append({"role": "user", "content": prompt})

    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages)
    
    reply = response.choices[0].message.content

    #updaate chat history

    update_history = chat_history if chat_history else []
    update_history.append({"role": "user", "content": prompt})
    update_history.append({"role": "assistant", "content": reply})  

    return reply, update_history

#streamlit
st.set_page_config(page_title="ROLE BASED AI ASSISTANT", page_icon="-",layout="wide")
                   
#Customise CSS for better styling

st.markdown("""initial_sidebar_state=
<style>
    .role-card { padding: 1rem;
                 border-radius: 10px;
                 border: 2px solid #e0e0e0;
                 margin: 0.5rem 0;
                 background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)    
            }   
    .selected-role {
            border-color: #4CSF50;
            background:  linear-gradient(135deg, #fa8edea 0%, #cfed6e32 100%) 
            }        
    .stSelectbox > div > div{
            background-color: #f0f2f6;
            }       
>/style>
""", unsafe_allow_html=True)

st.title("ROLE BASED AI ASSISTANT")
st.markdown("---")

#initialise the session state
if "role_chat_histrory" not in st.session_state:
    st.session_state.role_chat_history = []

if "selected_role" not in st.session_state:
    st.session_state.session_role = "Default"

if "role_input_key" not in st.session_state:
    st.session_state.role_input_key = 0

#sidebar for role selection

with st.sidebar:
    st.header("Choose Your AI Assistant Role")

   #Role Selection
    selected_role = st.selectbox(
        "Select a role:", 
        list(ROLE_PROMPTS.keys()),
        index=list(ROLE_PROMPTS.keys()).index(st.session_state.selected_role),
        key="role_selector"
    )

#if role chnaged
if selected_role != st.session_state.selected_role:
    st.session_state.role_chat_history = []
    st.session_state.selected_role = selected_role
    st.session_state.role_input_key += 1
    st.rerun

#display current role
st.markdown(f"""
            <div class="role-card selected-role:>
            <h4> Current Role: "selected_role </h4>
            <p><em> {ROLE_PROMPTS[selected_role]}</em></p>
            </div>
            """, unsafe_allow_html=True)

#Role description

st.markdown("Available Role")
for role, describtion in ROLE_PROMPTS.items():
    emoji = {
        "Default":"+",
        "Teacher":"T",
        "Doctor":"D",
        "Lawyer":"L",
        "Fitness Coach": "FC",
        "Careert Advisor": "CA",
    }.get(role,"--")

st.markdown(f"**{emoji} {role}**")

st.caption(describtion[:80] + "..." if len(describtion)>80 else describtion)
st.markdown("---")

#clear Conversaion Button

if st.button("Clear Conversation", type="secondary"):
    st.session_state.role_chat_history = []
    st.session_state.role_input_key += 1
    st.rerun()

#Main Chat Interface

col1, col2 = st.columns([3, 1])

with col1:
    #Display current role promiently
    role_emoji = {
        "Defualt" : "%",
        "Teacher" : "#",
        "Doctor" : "@",
        "Lawyer": "&",
        "Fitness Coach": "!",
        "Career Advisor": "|"
    }.get(selected_role, "++")

    st.markdown(f"###{role_emoji} Chatting with: **{selected_role}")

    #display chat history

    if st.session_state.role_chat_history:
        st.markdown(" ## CONVERSATION")

        for i, message in enumerate(st.session_state.role_chat_history):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message['content'])

            else:
                 with st.chat_message("assistant"):
                    st.write(message['content'])
    else:
        st.info(f"Hello ! I am your {selected_role} assistant. How can I help you today")