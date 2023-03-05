# Importing required modules
import os
import openai

from chatbot import Chatbot

def main():
    # Setting up OpenAI API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Inititate the bot
    Bot = Chatbot(
        max_tokens=200,
        temperature=0.8,
        pre_prompt="""
        You are a helpful AI assistant.
        """
    )
    Bot.terminal_chat()

if __name__ == "__main__":
    main()
