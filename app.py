import gradio as gr

from chat_functions_module import gradio_chat

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(
            show_label=False, placeholder="Enter text and press enter"
        ).style(container=False)

    txt.submit(gradio_chat, [txt, state], [chatbot, state])

demo.launch()