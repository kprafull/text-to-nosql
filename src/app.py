import streamlit as st

# Initialize chat history in session state if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display all messages stores in session state
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user messages
prompt = st.chat_input("Say something...")
# message = st.chat_message("assistant")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate bot response (dummy for now)
    bot_response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)

