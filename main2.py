from utils import configure, display_msg
from openai import OpenAI
import streamlit as st
import time
import os
from prompts import CONVERSATION_PROMPT, GRAMMAR_PROMPT, TRANSLATE_PROMPT, INITIAL_PROMPT, NATIVE_LANGUAGE_PROMPT, EVALUATION_PROMPT

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('LangoBot: Your Personal English Tutor')

class Basic:
    def __init__(self):
        configure()
        self.openai_model = "gpt-3.5-turbo"
        self.placeholder = "Type your response here..."
        self.client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY']
        )
    
    def send_openai_request(self, messages, max_tokens=400):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
            return response.choices[0].message.content
        except Exception as e:
            st.error("Error in OpenAI request: " + str(e))
            return None
    
    def translate(self, response):
        translate_messages = [{"role": "user", "content": TRANSLATE_PROMPT.format(native_language = st.session_state["native_language"], message=response)}]
        translated_message = self.send_openai_request(messages=translate_messages, max_tokens=500)
        st.session_state.messages.append({"role": "assistant", "content": translated_message})
        

    def evaluation(self):
        conversation_history = ""
        messages = st.session_state["conv_messages"]
        for message in messages:
            if (message["role"] == "user"):
                conversation_history += "Student: " + message["content"] + "\n"
            else:
                conversation_history += "Teacher: " + message["content"] + "\n"
        feedback_messages = [{"role": "system", "content": EVALUATION_PROMPT}, 
                             {"role": "assistant", "content": conversation_history}]
        feedbacks = self.send_openai_request(messages=feedback_messages, max_tokens=600)
        st.session_state.messages.append({"role": "assistant", "content": feedbacks})

    def main(self):
        # record the whole chat memory in "messages"
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": INITIAL_PROMPT}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])
        # record the conversation memory in "conv_messages"
        if "conv_messages" not in st.session_state:
            st.session_state["conv_messages"] = [{"role": "system", "content": CONVERSATION_PROMPT}, 
                                                 {"role": "assistant", "content": INITIAL_PROMPT}]
                
        # get user response
        user_query = st.chat_input(placeholder=self.placeholder)
        if user_query:
            # display user response and store it in the conversation history
            display_msg(user_query, 'user')
            st.session_state.conv_messages.append({"role": "user", "content": user_query})
            with st.chat_message("assistant"):
                # get grammar correction feedback
                question_response = """
                The Q&A is:

                Question: {question}
                Response: {response} 
                """
                grammar_messages = [{"role": "system", "content": GRAMMAR_PROMPT}, 
                                    {"role": "user", "content": question_response.format(question=st.session_state["conv_messages"][-1]['content'], response=user_query)}]
                grammar_response = self.send_openai_request(messages=grammar_messages)
                # get conversation response
                conversation_response = self.send_openai_request(messages=st.session_state["conv_messages"], max_tokens=200)
                # concatenate two reponses and display on the interface
                final_response = grammar_response + "\n\n" + "Back to conversation: " + conversation_response
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                st.session_state.conv_messages.append({"role": "assistant", "content": conversation_response})
                st.button("Translate Assistant's Message", on_click=lambda: self.translate(final_response))  
                st.button("End", on_click=lambda: self.evaluation()) 

if __name__ == "__main__":
    obj = Basic()
    obj.main()
   