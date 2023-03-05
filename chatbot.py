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

    def respond(self, prompt) -> list[dict[str, str]]:
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
        # Print warning if the bot ended its' response due to reaching max token length
        self.finish_reason = self.api_response["choices"][0]["finish_reason"]
        if self.finish_reason == "length":
            print("WARNING, The response stopped because max token length was reached")
        # Append the AI's response as an "assistant" role message to the list of messages
        self.messages.append({"role": "assistant", "content": self.latest_response})
        return self.messages

    def terminal_chat(self):
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

    def gradio_chatbot_func(self, input, _=None):
        self.respond(input)
        messages_tuples_list = []
        for i in range(1, len(self.messages), 2):
            messages_tuples_list.append(
                (self.messages[i]["content"], self.messages[i + 1]["content"])
            )
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
