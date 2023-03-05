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
        self.messages = [{"role": "system", "content": pre_prompt}]
        print(pre_prompt)

    def chat_response(self) -> str:
        # Use OpenAI's Chat API to generate a response to the prompt and history of messages
        response = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=self.messages,
        )
        # Get the content of the response from the API result
        content = response["choices"][0]["message"]["content"]
        # Return the response content
        print(content)
        return content

    def construct_messages_list(self, prompt) -> list[dict[str, str]]:
        # Append the user's prompt as a "user" role message to the list of messages
        self.messages.append({"role": "user", "content": prompt})
        # Get the AI's response to the user's prompt and history of messages
        response = self.chat_response()
        # Append the AI's response as an "assistant" role message to the list of messages
        self.messages.append({"role": "assistant", "content": response})
        return self.messages

    def terminal_chat(self):
        # Set an initial empty prompt
        prompt = ""
        # Loop until the user enters "exit"
        while prompt != "exit":
            # Get the user's prompt
            prompt = input("You: ")
            # Generate the updated list of messages and history tokens for the conversation based on the user's prompt
            self.construct_messages_list(prompt)

    ######## Functions used for Gradio interface ############
    def convert_to_tuples_list(self, messages) -> list[tuple[str, str]]:
        tuples_list = []
        for i in range(1, len(messages), 2):
            tuples_list.append((messages[i]["content"], messages[i + 1]["content"]))
        return tuples_list

    def gradio_chatbot_func(self, input, messages=None):
        self.construct_messages_list(input)
        messages_tuples_list = self.convert_to_tuples_list(self.messages)
        return messages_tuples_list, self.messages

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
