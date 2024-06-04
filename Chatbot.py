from dataclasses import dataclass
from typing import Literal
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

def load_css():
    with open("C:\\Users\\acer\\OneDrive - Trường ĐH CNTT - University of Information Technology\\Tài liệu\\Chatbot_AI_model\\First chatbot\\static\\styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "conversation" not in st.session_state:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", 
            google_api_key="AIzaSyBEn3bjgKA8cQC12bw89PdR0ySjuta-gow"
            )
        
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationSummaryMemory(llm=llm),
        )

def on_click_callback():
    with get_openai_callback() as cb:
        human_prompt = st.session_state.human_prompt
        llm_response = st.session_state.conversation.run(
            human_prompt
        )
        st.session_state.history.append(
            Message("human", human_prompt)
        )
        st.session_state.history.append(
            Message("ai", llm_response)
        )
        st.session_state.token_count += cb.total_tokens
        
        # Clear the text input value after sending message
        st.session_state.human_prompt = ""
        

# Loading CSS styling file and initializing the session state
load_css()
initialize_session_state()


# Creating the title
st.markdown("""
<div style="display: flex; align-items: center;">
    <h1 style="margin-left: 10px;">Chatbot by Hoàng Minh Thái</h1>
    <div style="border: 2px solid black; border-radius: 10px; padding: 5px;">
        <img src="https://cdn-icons-png.flaticon.com/128/897/897219.png" width="60" height="60">
</div>
""", unsafe_allow_html=True)

# Creating the sidebar storing two buttons including: Account Status and Support Service
with st.sidebar:
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    if st.button("Account Status", key="account_status"):
        st.session_state.selected_option = "Account Status"
        st.info("Active!")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    if st.button("Support Service", key="support_service"):
        st.session_state.selected_option = "Support Service"
        st.info("""Contact us at: \n
                Email: thaihm2014@gmail.com
    Phone: 0818380406 """)

for _ in range(1):
    st.markdown("")    

# Creating chat history for storing messages exchanged with the chatbot
with st.container(height = 400, border=True):
    chat_placeholder = st.container()
    
    with chat_placeholder:
        for chat in st.session_state.get('history', []):
            div = f"""
    <div class="chat-row 
        {'' if chat.origin == 'ai' else 'row-reverse'}">
        <img class="chat-icon" src="app/static/{
            'chatbot.png' if chat.origin == 'ai' 
                        else 'profile.png'}"
            width=32 height=32>
        <div class="chat-bubble
        {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
            &#8203;{chat.message}
        </div>
    </div>
            """
            st.markdown(div, unsafe_allow_html=True)
    
for _ in range(1):
    st.markdown("")

# Creating the input text field for entering the requests or prompts and "Send" button
prompt_placeholder = st.form("chat-form")
with prompt_placeholder:
    st.markdown("**Chatbox**")
    cols = st.columns((8, 1))
    cols[0].text_input(
        "Chatbox",
        value="",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "🤖",
        type="secondary", 
        on_click=on_click_callback, 
    )


credit_card_placeholder = st.empty()
credit_card_placeholder.caption(f"""
Author: Hoàng Minh Thái From UIT-VNU\n
Debug Langchain conversation: 
{st.session_state.conversation.memory.buffer}
""")

components.html("""
<script>
const streamlitDoc = window.parent.document;

const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === '🤖'
);

streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'Enter':
            submitButton.click();
            break;
    }
});
</script>
""", 
    height=0,
    width=0,
)
