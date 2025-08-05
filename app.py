import gradio as gr

def greet(name):
    return f"Hello, {name}!"

with gr.Blocks() as demo:
    gr.Markdown("# My App")
    input_text = gr.Textbox(label="Enter your name")
    output_text = gr.Textbox(label="Greeting")
    btn = gr.Button("Greet")
    btn.click(greet, inputs=input_text, outputs=output_text)

demo.launch()
