import gradio as gr
import openai

# Configura tu clave de API de OpenAI
openai.api_key = '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'

# Función para iniciar la historia
def start_story(word):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un narrador de historias interactivas. Crea una historia mágica basada en una palabra clave."},
            {"role": "user", "content": f"Usa la palabra '{word}' para crear una historia inicial de fantasía, con un punto de decisión al final."}
        ]
    )
    story = response['choices'][0]['message']['content']

    # Opciones iniciales (generadas automáticamente)
    options = ["1", "2"]
    return story, options

# Función para continuar la historia según la elección
def continue_story(current_story, choice):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un narrador de historias interactivas. Describe qué sucede después de una decisión del jugador."},
            {"role": "user", "content": f"Historia actual: {current_story}. Elige: {choice}. ¿Qué pasa después?"}
        ]
    )
    new_story = response['choices'][0]['message']['content']

    # Generar un prompt para la imagen
    image_prompt = f"Describe visualmente la escena siguiente: {new_story}"
    return new_story, image_prompt

# Interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("## Crea tu propia historia interactiva 🎮")
    gr.Markdown("Introduce una palabra para comenzar una historia mágica y toma decisiones en cada escena.")

    # Inputs y outputs
    word_input = gr.Textbox(label="Palabra inicial", placeholder="Introduce una palabra clave (ej. bosque, dragón, luna)")
    story_display = gr.Textbox(label="Historia actual", lines=5, interactive=False)
    choice_input = gr.Radio(choices=["1", "2"], label="Elige una opción", interactive=True)
    output_story = gr.Textbox(label="Nueva historia", lines=5, interactive=False)
    output_image_prompt = gr.Textbox(label="Descripción de la imagen", interactive=False)

    # Botones
    start_button = gr.Button("Iniciar historia")
    continue_button = gr.Button("Continuar")

    # Funciones conectadas
    start_button.click(
        fn=start_story,
        inputs=[word_input],
        outputs=[story_display, choice_input]
    )
    continue_button.click(
        fn=continue_story,
        inputs=[story_display, choice_input],
        outputs=[output_story, output_image_prompt]
    )

demo.launch()
