import streamlit as st
import anthropic

# 1. App Page Configuration
st.set_page_config(page_title="Free Claude AI Chatbot", page_icon="🤖")
st.title("🤖 Claude AI Assistant")

# 2. Sidebar for Secure Key Entry (Keeps hosting free for you!)
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Anthropic API Key", type="password", help="Get a key from console.anthropic.com")
    st.markdown("[Get an Anthropic API Key](https://anthropic.com)")

# 3. Initialize chat history session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display historical chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if prompt := st.chat_input("What is on your mind?"):
    if not api_key:
        st.info("Please add your Anthropic API key in the sidebar to continue.")
        st.stop()
        
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Call Anthropic Claude API & Stream Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = anthropic.Anthropic(api_key=api_key)
            
            # Using standard streaming API syntax
            with client.messages.stream(
                model="claude-3-5-sonnet-latest",
                max_tokens=1024,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
