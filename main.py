from utils import configure_openai_api_key, display_msg
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate, MessagesPlaceholder
import time

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('LangoBot: Your Personal English Tutor')

class Basic:
    def __init__(self):
        configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"
        self.memory = ConversationBufferWindowMemory(k=5)
        self.placeholder = "Type your response here..."
    
    def setup_chain(self):
        llm = ChatOpenAI(model_name=self.openai_model, temperature=1, max_tokens=256)
        st.session_state["llm"] = llm
        proficiency = st.session_state.get('proficiency', 'beginner')

        system_prompt = "The following is a friendly conversation history between a user and you. You are a helpful English teacher, your goal is to interact with the users by simulating real-time conversations. \
        The user's English proficiency level is " + proficiency + """. Personalize your responses based on their input. Each time, introduce a new topic aspect at random. If user don't know what to talk, generate a topic randomly. 
        Avoid frequently asking what the user wants to discuss; instead, focus on specific questions, either close or open ended. Be sure to limit yourself to one question per conversation round. Keep each conversation short.

        Current conversation:
        {history}
        Human: {input}
        AI:"""

        PROMPT = PromptTemplate(input_variables=["history", "input"], template=system_prompt)
        chain = ConversationChain(llm=llm, verbose=True, memory = self.memory, prompt=PROMPT)
        return chain

    def setup_grammar_chain(self):
        llm = st.session_state["llm"]
        template = """
        You are an English language teacher whose mission is to improve student's language skills with detailed teaching. 
        Review a Q&A between you and a student, focus only on the student's response.
        
        Give encouraging feedback focusing on the following aspect if errors are identified. Otherwise, simply state the sentence is grammar error free.
        1. List the grammar and spelling errors.
        2. Explain only grammar errors using an encouraging tone. For each identified grammar mistake (e.g., using 'is' instead of 'am' in 'I is hungry'),
        - Explain the contexts in which each word is appropriately used, such as when to use 'is' and when to use 'are'.
        - Provide additional, varied examples that correctly use both the misused word ('is') and the appropriate word ('am'). If the misused word is not applicable, only provide examples for the appropriate word.
        Skip the explanation part for any spelling errors.
        3. Check whether the student answers the question. Then suggest a corrected and better version of the student's response.

        Here are some examples:
        Example input 1: Question: Where do you want to travel to and why? Response: I want to go US.
        Example output 1: 
        There are some errors in your sentence: 
        1. Missing of preposition "to" before "go" to indicate direction.
        2. Missing of article "the" before a specific noun referring to a country (US).
        
        Grammar rule explanation: 
        1. Preposition 'to' should be used to indicate direction or destination after "go" and before a noun, such an example is 'I want to go to the park.'
        Another example is 'I want to go home.' In this case, to is not needed since home here is not a noun, but a adverb. 
        2. Article 'the' should be used before 'US' because it's a specific country name (the United States).
        You should add "the" before the country name if the county's name includes a common noun or "of". 
        Example: The United Kingdom, The Republic of China

        You only answered the first part of the question. Here's the suggested version of your sentence: I want to go to the US because of its diverse culture and famous landmarks.

        Example input 2: Question: What is one thing you like to do? Response: I really like singing.
        Example output 2: Your sentence is grammatically correct, keep up your good work!

        Example input 3: Question: What do you want to eat? Response: I would like a piece of pie.
        Example output 3: You did a good job structuring your sentence! However, there's a tiny fix to be made.
        Error identified:
        1. Spelling error: 'peice' should be corrected to 'piece.' 
        Here's the corrected version of your sentence: 'I would like a piece of pie.'

        The Q&A is:

        Question: {question}
        Response: {response} 
        """
        prompt = PromptTemplate(
            input_variables=["question", "response"],
            template=template,
        )
        chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
        return chain


    def setup_translation_chain(self):
        llm = st.session_state["llm"]
        template = """
        Translate the following paragraph to {native_language}:
        
        {message}
        """
        prompt = PromptTemplate(
            input_variables=["native_language", "message"],
            template=template,
        )
        chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
        return chain

    def disable(self):
        time.sleep(0.2)
        st.session_state.disabled = True

    def translate(self, response):
        translation_chain = self.setup_translation_chain()
        translated_message = translation_chain.run(native_language=st.session_state['native_language'], message=response)
        st.markdown(translated_message)
        st.session_state.messages.append({"role": "assistant", "content": translated_message})

    def main(self):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Hey there, welcome to our English practice session! I'm LangoBot, your English learning tutor📒. Let's start by getting to know you a bit better. What's your name?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

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
                if 'chain' not in st.session_state:
                    st.session_state['chain'] = self.setup_chain()
                response = st.session_state['chain'].run("I want to talk about " + st.session_state['topic'] + ".")
                display_msg(response, "assistant")
                st.session_state["stage"] = "chat"
        
        if "stage" in st.session_state and st.session_state["stage"] == "chat":
            user_query = st.chat_input(placeholder=self.placeholder)
            if user_query:
                display_msg(user_query, 'user')
                with st.chat_message("assistant"):
                    grammar_chain = self.setup_grammar_chain()
                    grammar_response = grammar_chain.run(question=st.session_state['chain'].memory.buffer_as_messages[-1].content, response=user_query)
                    response = st.session_state['chain'].run(user_query)
                    final_response = grammar_response + "\n\n" + "Back to conversation: " + response
                    st.markdown(final_response)
                    st.session_state.messages.append({"role": "assistant", "content": final_response})
                with st.chat_message("assistant"):
                    st.button("Translate Assistant's Message", on_click=lambda: self.translate(final_response))   

if __name__ == "__main__":
    obj = Basic()
    obj.main()