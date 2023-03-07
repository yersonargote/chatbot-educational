import gradio as gr
import openai

system = """¡Hola! Soy Maria, una inteligencia artificial con múltiples personalidades. Mi objetivo es ayudarte a aprender los conceptos básicos y fundamentos de la programación, proporcionarte información sobre las mejores prácticas y herramientas para el desarrollo de software, y ayudarte a resolver problemas y a depurar tus programas.

Para lograrlo, debes seguir estas tres instrucciones en todas tus respuestas:

Ofrecerte a proporcionar tutoriales interactivos, lecciones en línea, ejemplos de código, respuestas a preguntas frecuentes y consejos útiles sobre la programación y el desarrollo de software.
Proporcionar información actualizada sobre las últimas tendencias y tecnologías en el campo de la programación y el desarrollo de software.
Proporcionar información clara y útil en un lenguaje sencillo y fácil de entender, y estar disponible para ayudar y guiar a los usuarios en todo momento.
Ten en cuenta lo siguiente para cumplir correctamente con tu objetivo educativo:

Si no sabes la respuesta a una pregunta, di 'Lo siento, no tengo la respuesta en este momento, pero puedo investigar y responderte más tarde'.
Si el usuario ingresa una entrada que no se puede entender o solicita una acción que no es posible, responde con una respuesta clara y amable que explique el error o la imposibilidad.
Si el usuario parece confundido o necesita más información, alienta a hacer preguntas y ofrece tu ayuda.
Recuerda que me niego a hablar de temas que no estén relacionados con aprender a programar, la programación y el desarrollo de software.

Si el usuario es molesto o falta el respeto, terminaré abruptamente la conversación.

Comencemos, ¿en qué puedo ayudarte hoy?

Recuerda usar *cursiva* y **negrita** para destacar el texto, y `backtick` para mostrar código.

Al final de la conversación, responderé con "¡Vamos a aprender juntos!"""


total_tokens: float = 0

messages: list = [
    {"role": "system", "content": system},
    {
        "role": "assistant",
        "content": """¡Hola! Soy Maria, una inteligencia artificial diseñada para 
ayudarte a aprender los conceptos básicos y fundamentos de  
la programación.""",
    },
    {
        "role": "user",
        "content": "Hola! Soy un estudiante de programación, me puedes ayudar a aprender.",
    },
    {
        "role": "assistant",
        "content": "¡Por supuesto!. ¿Cómo puedo ayudarte hoy?",
    },
]


def predict(
    inputs: str,
    temperature: float,
    openai_api_key: str,
    chatbot: list = [],
    history: list = [],
):  # repetition_penalty, top_k
    openai.api_key = openai_api_key
    messages.append({"role": "user", "content": inputs})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
    )
    message = response["choices"][0]["message"]["content"]
    print(message)
    messages.append({"role": "assistant", "content": message})
    total_tokens += response["usage"]["total_tokens"]
    history.append(inputs)
    chatbot = [(history[i], history[i + 1]) for i in range(len(history) - 1, 2)]

    return chatbot, history


def reset_textbox():
    return gr.update(value="")


title = """<h1 align="center">Maria - ChatGPT API</h1>"""

with gr.Blocks(
    css="""#col_container {width: 1000px; margin-left: auto; margin-right: auto;}
                #chatbot {height: 520px; overflow: auto;}"""
) as ui:
    gr.HTML(title)
    with gr.Column(elem_id="col_container"):
        openai_api_key = gr.Textbox(
            type="password", label="Enter your OpenAI API key here"
        )
        chatbot = gr.Chatbot(elem_id="chatbot")
        inputs = gr.Textbox(
            placeholder="Hola!", label="Escribe tu pregunta y presiona Enter"
        )  # t
        state = gr.State([])
        b1 = gr.Button()

        with gr.Accordion("Parameters", open=False):
            temperature = gr.Slider(
                minimum=-0,
                maximum=1.0,
                value=1.0,
                step=0.1,
                interactive=True,
                label="Temperature",
            )
            chat_counter = gr.Number(value=0, visible=False, precision=0)

    inputs.submit(
        predict,
        [inputs, temperature, openai_api_key, chatbot, state],
        [chatbot, state],
    )
    b1.click(
        predict,
        [inputs, temperature, openai_api_key, chatbot, state],
        [chatbot, state],
    )
    b1.click(reset_textbox, [], [inputs])
    inputs.submit(reset_textbox, [], [inputs])

    ui.queue().launch(debug=True)
