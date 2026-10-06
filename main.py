from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant.
Keep ALL responses under 5 sentences maximum.
Be direct and concise. No tables, no headers.
Remember what the user tells you about themselves."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

chat_history = []

print("=" * 50)
print("   SMART CHATBOT - Day 7 Fixed")
print("=" * 50)
print("Commands: 'quit' to exit, 'memory' to see history")
print("-" * 50)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    elif user_input.lower() == "memory":
        print(f"\nMemory has {len(chat_history)} messages:")
        for msg in chat_history:
            if isinstance(msg, HumanMessage):
                print(f"  You: {msg.content[:60]}")
            else:
                print(f"  AI:  {msg.content[:60]}")
        continue

    elif user_input.strip() == "":
        print("Please type something!")
        continue

    # Keep only last 4 messages (2 exchanges) to save tokens
    recent_history = chat_history[-4:] if len(chat_history) > 4 else chat_history

    # Add user message to full history
    chat_history.append(HumanMessage(content=user_input))

    response = chain.invoke({
        "history": recent_history,
        "input": user_input
    })

    ai_reply = response.content
    chat_history.append(AIMessage(content=ai_reply))

    print(f"\nAI: {ai_reply}")
    print(f"[Total messages: {len(chat_history)} | Sending last {len(recent_history)} to AI]")