from utils import configure_openai_api_key, display_msg
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import SequentialChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate, MessagesPlaceholder
import time

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('LangoBot: Your Personal English Tutor')
my_openAI_key = "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"

class Basic:
    def __init__(self):
        configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"
        self.memory = ConversationBufferMemory()
        self.placeholder = "Type your response here..."
    
    def setup_chain(self):
        llm = ChatOpenAI(model_name=self.openai_model, temperature=1)
        proficiency = st.session_state.get('proficiency', 'beginner')

        system_prompt = "The following is a friendly conversation history between a user and you. You are a helpful English teacher, your goal is to interact with the users by simulating real-time conversations. \
        The user's English proficiency level is " + proficiency + """, please give personalized conversation based on user's input. Make sure to randomly choose an aspect related to the topic to discuss, don't ask user what he/she wants to talk too often, ask more specific questions instead. In the end, you should give feedback on user's English level.

        Current conversation:
        {history}
        Human: {input}
        AI:"""

        PROMPT = PromptTemplate(input_variables=["history", "input"], template=system_prompt)

        ##chain = SequentialChain()
        chain = ConversationChain(llm=llm, verbose=True, memory = self.memory, prompt=PROMPT)
        return chain


    def disable(self):
        time.sleep(0.2)
        st.session_state.disabled = True

    def main(self):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Hey there, welcome to our English practice session! I'm LangoBot, your English learning tutor📒. Let's start by getting to know you a bit better. What's your name?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

        if 'chain' not in st.session_state:
            st.session_state['chain'] = self.setup_chain()

        if not "stage" in st.session_state or ("stage" in st.session_state and st.session_state["stage"] != "chat"):
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
                    display_msg(f"Thanks for sharing that, {st.session_state['name']}! Now, could you tell me your English proficiency level?", "assistant")

            if "proficiency" not in st.session_state  and "native_language" in st.session_state:
                st.chat_input(placeholder="Wait for selection", key = "disable", disabled=True)
                proficiency_levels = ["Beginner", "Elementary", "Intermediate", "Advanced", "Fluent", "Proficient", "Expert"]
                if not "disabled" in st.session_state:
                    st.session_state["disabled"] = False
                with st.chat_message("user"):
                    proficiency = st.selectbox("Select your English proficiency level:", proficiency_levels, index=None, on_change=self.disable, disabled=st.session_state.disabled)
                if proficiency:
                    st.session_state['proficiency'] = proficiency
                    st.session_state.messages.append({"role": 'user', "content": "You selected " + proficiency})
                    display_msg(f"Great! You are at the {proficiency} level. Now, could you tell me about a topic you are interested in?", "assistant")
            
            if "proficiency" in st.session_state:
                topic = st.chat_input(placeholder="Enter a topic you are interested in here...")
                if topic:
                    display_msg(topic, "user")
                    st.session_state['topic'] = topic

            if "topic" in st.session_state:
                response = st.session_state['chain'].run("I want to talk about " + st.session_state['topic'] + ".")
                display_msg(response, "assistant")
                st.session_state["stage"] = "chat"
        
        if "stage" in st.session_state and st.session_state["stage"] == "chat":
            user_query = st.chat_input(placeholder=self.placeholder)
            if user_query:
                display_msg(user_query, 'user')
                with st.chat_message("assistant"):
                    response = st.session_state['chain'].run(user_query)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    obj = Basic()
    obj.main()