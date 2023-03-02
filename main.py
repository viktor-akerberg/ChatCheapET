# Importing required modules
import os

import openai
import tiktoken

from chat_functions_module import in_terminal_chat

def main():
    # Setting up OpenAI API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Getting encoding for GPT-2 model from TikToken library
    encoder = tiktoken.get_encoding("gpt2")

    # Asserting that encoding and decoding using the encoding results in original string
    assert encoder.decode(encoder.encode("hello world")) == "hello world"

    # Defining a prompt to encourage short, AI-like answers
    pre_prompt = "Act like you are an AI. Answer short, just one sentence if possible."

    # Printing the prompt
    print(pre_prompt)

    # Creating a list with a single message containing the prompt as a "system" role message
    messages = [
        {"role": "system", "content": pre_prompt},
    ]

    # Encoding the prompt to generate the initial history tokens for the conversation
    history_tokens = encoder.encode(pre_prompt)
    # Call the in_editor_chat function with the initial list of messages
    in_terminal_chat(encoder, messages, history_tokens)


if __name__ == "__main__":
    main()