# AI Smart Chatbot

A conversational chatbot with sliding window memory.
Remembers context across messages while staying within token limits.

## Features
- Remembers last 4 messages to manage tokens efficiently
- Custom system prompt for personality control
- Memory command to view conversation history
- Handles empty input and edge cases gracefully

## How to run

1. Install dependencies:
   pip install langchain langchain-groq python-dotenv

2. Create a .env file:
   GROQ_API_KEY=your-key-here

3. Run:
   python main.py

## Commands
- Type anything to chat
- 'memory' to see conversation history
- 'quit' to exit

## Author
Built by Anushka as part of an AI development learning journey.