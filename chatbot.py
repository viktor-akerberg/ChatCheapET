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
        api_response = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=self.messages,
        )
        # Get the content of the response from the API result
        response = api_response["choices"][0]["message"]["content"]
        # Append the AI's response as an "assistant" role message to the list of messages
        self.messages.append({"role": "assistant", "content": response})
        # Set the latest_response
        self.latest_response = self.messages[-1]['content']
        return self.messages

    def terminal_chat(self):
        # Set an initial empty prompt
        prompt = ""
        # Loop until the user enters "exit"
        while prompt != "exit":
            # Get the user's prompt
            prompt = input("You: ")
            # Generate the updated list of messages based on the user's prompt
            self.respond(prompt)
            print(self.latest_response)

    ######## Functions used for Gradio interface ############

    def gradio_chatbot_func(self, input, _=None):
        self.respond(input)
        messages_tuples_list = []
        for i in range(1, len(self.messages), 2):
            messages_tuples_list.append((self.messages[i]["content"], self.messages[i + 1]["content"]))
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
