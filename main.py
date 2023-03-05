# Importing required modules
import os

import openai
import tiktoken

from chatbot import Chatbot


def main():
    # Setting up OpenAI API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Getting encoding for GPT-2 model from TikToken library
    encoder = tiktoken.get_encoding("gpt2")

    # Asserting that encoding and decoding using the encoding results in original string
    assert encoder.decode(encoder.encode("hello world")) == "hello world"

    # Inititate the bot
    Bot = Chatbot(
        model="gpt-3.5-turbo",
        max_tokens=200,
        temperature=0.8,
        pre_prompt="You are a helpful AI assistant.",
    )
    Bot.terminal_chat()


if __name__ == "__main__":
    main()