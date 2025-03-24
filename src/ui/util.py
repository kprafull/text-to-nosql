import streamlit as st

def add_chat_message(role, content, placeholder=False, code=False, session_state=True):
    print("Adding chat \n", content)
    if(session_state):
        st.session_state.messages.append({"role": role, "content": content, "code": code})
    avatar = "🚀" if role == "debug" else None
    with st.chat_message(role, avatar=avatar):
        if code:
            exec(content)
        else:
            message_container = st.empty() if placeholder else None
            message_container.markdown(content) if message_container else st.markdown(content)
            return message_container
