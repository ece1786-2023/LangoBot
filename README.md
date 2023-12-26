# LangoBot
## Introduction of the project:
LangoBot is an English learning chatbot that utilizes GPT-4 API. It aims to improve users' English skills through AI-driven, interactive conversations, customized to each user's proficiency level. In our application, the AI acts as a teacher, leading discussions on users’ topics of interest or guiding them through English practice sessions. Users benefit from instant grammar feedback, translation support, and comprehensive advice on their English skills.
<br>
<p align="center">
  <img src="https://github.com/ece1786-2023/LangoBot/assets/52727328/575f896a-a18d-4753-a349-e9ccdad02c1f" alt="General Illustration">
  <br>
  <br>
  Figure 1. General Illustration of LangoBot
</p>

## Architecture:
LangoBot utilizes Streamlit Framework for its user interface and GPT-4 API for interaction logic. The system is driven by four main prompts as shown in the *prompts.py* file and summarized below. 
1. **Conversation Prompt**: Begin by inquiring about the user's proficiency level and interests to tailor an educational dialogue. In cases of uncertainty, suggest random topics or practice sessions. Engage users through varied interactions, including role-play scenarios. All AI-user messages history is saved and repeatedly sent to GPT-4 with this prompt to generate context-aware AI conversation responses.
2.**Grammar Prompt** (Few Shot): Analyze an AI-message and user response pair to identify grammatical errors in the user’s response, provide grammar rule explanations and usage examples, determine response relevance to AI’s message, and suggest an improved version of the response.
3. **Translation Prompt**: Translate a message from an English instructor into the user’s native language.
4. **Evaluation Prompt**: Review conversation history to assess and provide feedback on the user’s overall English proficiency, focusing on aspects like vocabulary and grammar usage, reading comprehension, writing skills, and potential improvements.
<p align="center">
  <img src="https://github.com/ece1786-2023/LangoBot/assets/52727328/f9f97170-bb26-4ead-a780-5eaf34ce7552">
  <br>
  <br>
  Figure 2. Prompt Interactions in LangoBot
</p>

## Evaluation:
We manually generated three test datasets to evaluate our system's grammar correction, translation, and overall feedback performance. This evaluation process results can be found in the *test-data* folder. Detailed evaluation metrics and results are in the linked report (coming soon).

## Deployed Application
Deployed Website: https://applangobot-taoujboykmejputvjz43kr.streamlit.app/
