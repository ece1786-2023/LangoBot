import os
import streamlit as st

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)


def configure():
    openai_api_key = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        value=st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else '',
        placeholder="sk-..."
        )
    
    native_language = st.sidebar.text_input(
        label="Your Native Language",
        value=st.session_state['native_language'] if 'native_language' in st.session_state else '',
        placeholder="sk-..."
        )
    if openai_api_key and native_language:
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key
        st.session_state['native_language'] = native_language
    else:
        st.error("Please add your OpenAI API key and native language to continue.")
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
        st.stop()
    return openai_api_key