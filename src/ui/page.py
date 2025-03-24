import streamlit as st
import agents.llm as llm
import ui.util as util

OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]

def display():
    # Main page
    st.title("NOSQL and Python Agent")
    st.write("This agent can help you with NOSQL queries and Python code for data analysis. Configure your Iceberg database connection.")

    # Display clear chat history and debug mode options
    col1, col2 = st.columns([1,1])  # Adjust column ratios as needed
    with col1:
        if st.button("Clear Chat History"):
            st.session_state["messages"] = []
    with col2:
        debug_mode = st.checkbox("Debug Mode!", value=True)

    # Initialize chat history in session state if not present
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display all messages stores in session state
    for message in st.session_state["messages"]:
        print("-------------", message)
        util.add_chat_message(message["role"], message["content"], code=message["code"], session_state=False)

    # Input for user messages
    prompt = st.chat_input("Ask your question...")

    if prompt:
        # Display user message
        util.add_chat_message("user", prompt)

        # Generate bot response
        bot_response = llm.call_llm_chain(OPENAI_API_KEY, prompt, debug_mode)
        print("=======bot_response========", bot_response)

        keywords = ["plot", "graph", "chart", "diagram", "visualize", "visualisation", "show"]
        if any(keyword in prompt.lower() for keyword in keywords):
            # Generate plotly code to display
            cleaned_code = llm.call_python_llm(OPENAI_API_KEY, bot_response)
            util.add_chat_message("assistant", cleaned_code, code=True)
        else:
            # Display bot response
            # st.session_state.messages[-1] = {"role": "assistant", "content": bot_response}
            util.add_chat_message("assistant", bot_response)

