import openai
import gradio as gr


class Chatbot:
    def __init__(
        self,
        model="gpt-3.5-turbo",
        max_tokens=200,
        temperature=0.8,
        pre_prompt="You are a helpful AI assistant.",
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.pre_prompt = pre_prompt
        print(pre_prompt)

    def chat_response(self, messages) -> str:
        """Calls OpenAIs API to get a chat response

        Arguments:
            messages: A list of dicts with the chat history

        Returns:
            content: The most recent response
        """
        # Use OpenAI's Chat API to generate a response to the prompt and history of messages
        response = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
        )
        # Get the content of the response from the API result
        content = response["choices"][0]["message"]["content"]
        # Return the response content
        print(content)
        return content

    def construct_messages_list(self, prompt, messages=[]) -> list[dict[str, str]]:
        if messages == []:
            # Defining a prompt which defines how the chatbot acts
            pre_prompt = self.pre_prompt
            # Creating a list with a single message containing the prompt as a "system" role message
            messages = [{"role": "system", "content": pre_prompt}]
        # Append the user's prompt as a "user" role message to the list of messages
        messages.append({"role": "user", "content": prompt})
        # Get the AI's response to the user's prompt and history of messages
        response = self.chat_response(messages)
        # Append the AI's response as an "assistant" role message to the list of messages
        messages.append({"role": "assistant", "content": response})
        # Return the updated list of messages and history tokens
        return messages

    def terminal_chat(self):
        # Set an initial empty prompt
        prompt = ""
        # Set an initial empty message list
        messages = []
        # Set an initial empty history tokens list
        history_tokens = []
        # Loop until the user enters "exit"
        while prompt != "exit":
            # Get the user's prompt
            prompt = input("You: ")
            # Generate the updated list of messages and history tokens for the conversation based on the user's prompt
            messages = self.construct_messages_list(prompt, messages)

        print("Total tokens this conversation:", len(history_tokens))
    
    def convert_to_tuples_list(self, messages) -> list[tuple[str, str]]:
        tuples_list = []
        for i in range(1, len(messages), 2):
            tuples_list.append((messages[i]["content"], messages[i + 1]["content"]))
        return tuples_list

    def gradio_chatbot_func(self, input, messages_dict=None):
        messages_dict = self.construct_messages_list(input, messages_dict)
        #print(messages_dict)
        messages_list = self.convert_to_tuples_list(messages_dict)
        #print(messages_list)
        return messages_list, messages_dict

    def gradio_chat(self):
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot()
            state = gr.State([])

            with gr.Row():
                txt = gr.Textbox(
                    show_label=False, placeholder="Enter text and press enter"
                ).style(container=False)

            txt.submit(self.gradio_chatbot_func, [txt, state], [chatbot, state])
        demo.launch()
