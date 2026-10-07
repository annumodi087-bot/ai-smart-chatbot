import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AI Smart Chatbot")
st.caption("Built with LangChain + Groq | By Annu")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Setup LLM and chain
@st.cache_resource
def get_chain():
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    llm = ChatGroq(api_key=api_key, model="openai/gpt-oss-120b", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant.
Keep responses concise — under 5 sentences.
Remember what the user tells you about themselves."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    return prompt | llm

chain = get_chain()

# Display chat history on screen
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    else:
        with st.chat_message("assistant"):
            st.write(msg.content)

# Chat input at the bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Add to history
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Get last 4 messages for context
    recent = st.session_state.messages[-4:] if len(st.session_state.messages) > 4 else st.session_state.messages

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke({
                "history": recent,
                "input": user_input
            })
            ai_reply = response.content
            st.write(ai_reply)

    # Save AI reply to history
    st.session_state.messages.append(AIMessage(content=ai_reply))

# Sidebar with info
with st.sidebar:
    st.header("Chat Info")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Memory window", "Last 4 messages")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Built during AI Development Course")
    st.caption("Day 8 — Streamlit UI")