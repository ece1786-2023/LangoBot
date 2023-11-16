from openai import OpenAI
import streamlit as st
from utils import configure_openai_api_key, display_msg
import os

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
)

def get_openai_response(prompt):
    response = client.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def check_grammar_and_explain(text, native_language):
    grammar_check_prompt = f"Check this for English grammar errors: '{text}'"
    grammar_correction = get_openai_response(grammar_check_prompt)

    if "no errors" in grammar_correction.lower():
        return "No grammar errors detected.", ""
    
    explanation_prompt = f"Explain the grammar mistake in English and in {native_language}: '{text}'"
    explanation = get_openai_response(explanation_prompt)
    return grammar_correction, explanation

def translate_text(text, target_language):
    translation_prompt = f"Translate this into {target_language}: '{text}'"
    return get_openai_response(translation_prompt)

def main():
    placeholder = "Type your response here..."
    st.title("LangoBot: Your Personalized English Tutor")
    configure_openai_api_key()
    
    # Initialize the messages list if it's not already present in the session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hey there, welcome to our English practice session! I'm LangoBot, your English learning tutor📒. Let's start by getting to know you a bit better. What's your name?"}]
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
    
    user_name = st.chat_input(placeholder="Enter your name here...")
    if user_name:
        display_msg(user_name, "user")
        st.session_state['name'] = user_name
        display_msg(f"Great to meet you, {user_name}! What's your native language?", "assistant")

    if "name" in st.session_state:
        native_language = st.chat_input(placeholder="Enter your native language here...")
        if native_language:
            display_msg(native_language, "user")
            st.session_state['native_language'] = native_language
            display_msg(f"Thanks for sharing that, {st.session_state['name']}! Now, could you tell me about a topic you are interested in?", "assistant")

    if "native_language" in st.session_state:
        topic = st.chat_input(placeholder="Enter a topic you are interested in here:")
        if topic:
            display_msg(topic, "user")
            st.session_state['topic'] = topic
            st.session_state["stage"] = "chat"
            display_msg(f"Great, let's talk about {topic}.", "assistant")
        
     """
     if "stage" in st.session_state and st.session_state["stage"] == "chat":
        user_input = st.chat_input(placeholder=placeholder)
        if user_input:
            grammar_correction, explanation = check_grammar_and_explain(user_input, st.session_state["native_language"])
            if grammar_correction:
                st.write("Grammar Feedback:", grammar_correction)
                st.write("Explanation:", explanation)

            response = get_openai_response(user_input)

            display_msg(user_input, "user")
            display_msg(response, "assistant")

            # Translation feature remains the same
            for message in st.session_state["messages"]:
                with st.expander("See translation"):
                    st.write(translate_text(message["content"], st.session_state['native_language']))
    """
if __name__ == "__main__":
    main()