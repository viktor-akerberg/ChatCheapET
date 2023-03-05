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

    def respond(self, prompt: str) -> None:
        """
        Asks the OpenAI API for a response.

        Arguments:
            input: User input text
        """
        # Append the user's prompt as a "user" role message to the list of messages
        self.messages.append({"role": "user", "content": prompt})

        # Get a response from the OpenAI API
        self.api_response = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=self.messages,
        )

        # Get the content of the response from the API result
        self.latest_response = self.api_response["choices"][0]["message"]["content"]

        # Append the AI's response as an "assistant" role message to the list of messages
        self.messages.append({"role": "assistant", "content": self.latest_response})

        # Print warning if the bot ended its' response due to reaching max token length
        self.finish_reason = self.api_response["choices"][0]["finish_reason"]
        if self.finish_reason == "length":
            print("WARNING, The response stopped because max token length was reached")

    def terminal_chat(self) -> None:
        """
        Allows you to chat with the bot in the terminal. 
        Asks for input until the user writes "exit"
        """
        while True:
            # Get the users' prompt
            prompt = input("You: ")

            # Loop until the user enters "exit"
            if prompt == "exit":
                break

            # Respond and print the response
            self.respond(prompt)
            print(self.latest_response)

    ######## Functions used for Gradio interface ############

    def gradio_chatbot_func(self, input: str, messages=None):
        """
        Function that has the correct inputs and outputs for the Gradio interface.

        Arguments:
            input: User input text
            messages: The message history
        
        Returns:
            messages_tuples_list: List of tuples to be displayed in the gradio chat interface
            messages: The message history
        """
        self.respond(input)
        # Creates a list of tuples to be displayed in the Gradio chat interface
        # Starts at 1 to skip the pre-prompt ("system" role)
        messages_tuples_list = []
        for i in range(1, len(self.messages), 2):
            messages_tuples_list.append(
                (self.messages[i]["content"], self.messages[i + 1]["content"])
            )
        return messages_tuples_list, self.messages

    def gradio_chat(self):
        """
        Creates a Gradio interface that allows you to chat with the bot.
        """
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot()
            state = gr.State([])

            with gr.Row():
                txt = gr.Textbox(
                    show_label=False, placeholder="Enter text and press enter"
                ).style(container=False)

            txt.submit(self.gradio_chatbot_func, [txt, state], [chatbot, state])
        demo.launch()
