import gradio as gr

from chat_functions_module import chat_response


def convert_to_tuples_list(messages):
    tuples_list = []
    for i in range(1, len(messages), 2):
        tuples_list.append((messages[i]["content"], messages[i + 1]["content"]))
    return tuples_list


def construct_messages_list(prompt, messages=[]):
    print(messages)
    if messages == []:
        # Defining a prompt which defines how the chatbot acts
        pre_prompt = (
            "Act like an aristrocratic cow."
        )
        # Printing the prompt
        print(pre_prompt)
        # Creating a list with a single message containing the prompt as a "system" role message
        messages = [
            {"role": "system", "content": pre_prompt},
        ]
    # Append the user's prompt as a "user" role message to the list of messages
    messages.append({"role": "user", "content": prompt})
    # Get the AI's response to the user's prompt and history of messages
    response = chat_response(messages)
    # Append the AI's response as an "assistant" role message to the list of messages
    messages.append({"role": "assistant", "content": response})
    # Return the updated list of messages and history tokens
    return messages


def chatbot_func(input, messages_dict=None):
    messages_dict = construct_messages_list(input, messages_dict)
    #print(messages_dict)
    messages_list = convert_to_tuples_list(messages_dict)
    #print(messages_list)
    return messages_list, messages_dict


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(
            show_label=False, placeholder="Enter text and press enter"
        ).style(container=False, clear_on_submit=True)

    txt.submit(chatbot_func, [txt, state], [chatbot, state])

demo.launch()
