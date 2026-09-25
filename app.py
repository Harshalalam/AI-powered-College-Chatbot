import streamlit as st
from dialog_manager import get_response


# Page 

st.set_page_config(
    page_title="College Helpdesk Chatbot",
    page_icon="🎓",
    layout="centered"
)


# Title

st.title("🎓 College Helpdesk Chatbot")
st.markdown("Ask enquiries or register complaints related to college facilities.")
st.divider()


# Initialize Chat History

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Welcome to College Helpdesk. How can I assist you today?"}
    ]

# Display Previous Messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User Input

if prompt := st.chat_input("Type your message here..."):
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    response = get_response(prompt)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)
