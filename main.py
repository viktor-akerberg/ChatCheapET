# Importing required modules
import os
import gradio as gr
import openai
import tiktoken

# Setting up OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Getting encoding for GPT-2 model from TikToken library
enc = tiktoken.get_encoding("gpt2")

# Asserting that encoding and decoding using the encoding results in original string
assert enc.decode(enc.encode("hello world")) == "hello world"

# Defining a prompt to encourage short, AI-like answers
pre_prompt = "Act like you are an AI. Answer short, just one sentence if possible."

# Printing the prompt
print(pre_prompt)

# Creating a list with a single message containing the prompt as a "system" role message
messages = [
    {"role": "system", "content": pre_prompt},
]

# Encoding the prompt to generate the initial history tokens for the conversation
history_tokens = enc.encode(pre_prompt)


# Define a function to get the AI's response to a given prompt and history of messages
def chat_response(messages):
    # Use OpenAI's Chat API to generate a response to the prompt and history of messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", max_tokens=100, temperature=0.8, messages=messages
    )
    # Get the content of the response from the API result
    content = response["choices"][0]["message"]["content"]
    # Return the response content
    return content


# Define a function to construct the list of messages for a conversation given a user prompt and current list of messages
def construct_messages_list(prompt, messages=[]):
    # Append the user's prompt as a "user" role message to the list of messages
    messages.append({"role": "user", "content": prompt})
    # Encode the user's prompt and append the resulting tokens to the history of the conversation
    history_tokens.extend(enc.encode(prompt))
    # Get the AI's response to the user's prompt and history of messages
    response = chat_response(messages)
    # Print the AI's response
    print("Bot: ", response)
    # Append the AI's response as an "assistant" role message to the list of messages
    messages.append({"role": "assistant", "content": response})
    # Encode the AI's response and append the resulting tokens to the history of the conversation
    history_tokens.extend(enc.encode(response))
    # Return the updated list of messages and history tokens
    return messages, history_tokens


# Define a function for chatting within the terminal/editor
def in_editor_chat(messages):
    # Set an initial empty prompt
    prompt = ""
    # Loop until the user enters "exit"
    while prompt != "exit":
        # Get the user's prompt
        prompt = input("You: ")
        # Generate the updated list of messages and history tokens for the conversation based on the user's prompt
        construct_messages_list(prompt, messages)


# Call the in_editor_chat function with the initial list of messages
in_editor_chat(messages)

"""with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(
            show_label=False, placeholder="Enter text and press enter"
        ).style(container=False)

    txt.submit(construct_messages_list, [txt, state], [chatbot, state])

demo.launch()"""
