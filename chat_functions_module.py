import openai

# Define a function to get the AI's response to a given prompt and history of messages
def chat_response(messages) -> str:
    """Calls OpenAIs API to get a chat response

    Arguments:
        messages: A list of dicts with the chat history
    
    Returns:
        content: The most recent response
    """
    # Use OpenAI's Chat API to generate a response to the prompt and history of messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", max_tokens=200, temperature=0.8, messages=messages
    )
    # Get the content of the response from the API result
    content = response["choices"][0]["message"]["content"]
    # Return the response content
    return content


# Define a function to construct the list of messages for a conversation given a user prompt and current list of messages
def construct_messages_list(prompt, encoder, messages = [], history_tokens = []):
    # Append the user's prompt as a "user" role message to the list of messages
    messages.append({"role": "user", "content": prompt})
    # Encode the user's prompt and append the resulting tokens to the history of the conversation
    history_tokens.extend(encoder.encode(prompt))
    # Get the AI's response to the user's prompt and history of messages
    response = chat_response(messages)
    # Print the AI's response
    print("Bot: ", response)
    # Append the AI's response as an "assistant" role message to the list of messages
    messages.append({"role": "assistant", "content": response})
    # Encode the AI's response and append the resulting tokens to the history of the conversation
    history_tokens.extend(encoder.encode(response))
    # Return the updated list of messages and history tokens
    return messages, history_tokens

# Define a function to construct the list of messages for a conversation given a user prompt and current list of messages
def gradio_chat(prompt, messages = []):
    # Append the user's prompt as a "user" role message to the list of messages
    messages.append({"role": "user", "content": prompt})
    
    # Get the AI's response to the user's prompt and history of messages
    response = chat_response(messages)
    # Print the AI's response
    print("Bot: ", response)
    # Append the AI's response as an "assistant" role message to the list of messages
    messages.append({"role": "assistant", "content": response})

    # Return the updated list of messages and history tokens
    return messages


# Define a function for chatting within the terminal
def in_terminal_chat(encoder, messages, history_tokens) -> None:
    # Set an initial empty prompt
    prompt = ""
    # Loop until the user enters "exit"
    while prompt != "exit":
        # Get the user's prompt
        prompt = input("You: ")
        # Generate the updated list of messages and history tokens for the conversation based on the user's prompt
        messages, history_tokens = construct_messages_list(prompt, encoder, messages, history_tokens)
    #print(messages)
    print("Total tokens this conversation:", len(history_tokens))
