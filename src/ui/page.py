import streamlit as st
import agents.llm as llm
import ui.util as util

OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]

def display():
    # Main page
    st.title("NOSQL and Python Agent")
    st.write("This agent can help you with NOSQL queries and Python code for data analysis. Configure your Iceberg database connection.")

    st.sidebar.title("Database Configuration")
    selected_db = st.sidebar.selectbox(
        "Select NoSQL DB:",
        ["Iceberg", "Hudi", "Delta Lake", "AWS Glue"]
    )
    disabled_dbs = ["Hudi", "Delta Lake", "AWS Glue"]

    if selected_db in disabled_dbs:
        st.sidebar.warning(f"'{selected_db}' is disabled. Please choose another.")

    if st.sidebar.button("Configure"):
        st.sidebar.write(f"You selected: {selected_db}")

    # Sidebar subtitle
    st.sidebar.markdown("## Settings & Options")

    if st.sidebar.button("Clear Chat History"):
        st.session_state["messages"] = []

    debug_mode = st.sidebar.checkbox("Debug Mode!", value=True)

    # Display clear chat history and debug mode options
    #col1, col2 = st.columns([1,1])  # Adjust column ratios as needed
    #with col1:
    #    if st.button("Clear Chat History"):
    #        st.session_state["messages"] = []
    # with col2:
    #    debug_mode = st.checkbox("Debug Mode!", value=True)

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

        keywords = ["plot", "graph", "chart", "diagram", "visualize", "visualisation"]
        if any(keyword in prompt.lower() for keyword in keywords):
            # Generate plotly code to display
            cleaned_code = llm.call_python_llm(OPENAI_API_KEY, bot_response)
            util.add_chat_message("assistant", cleaned_code, code=True)
        else:
            # Display bot response
            # st.session_state.messages[-1] = {"role": "assistant", "content": bot_response}
            util.add_chat_message("assistant", bot_response)

