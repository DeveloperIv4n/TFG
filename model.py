from transformers import GPT2Tokenizer, GPT2LMHeadModel
from mtranslate import translate
import torch
from langdetect import detect
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/generate-response/<question>', methods=['POST'])

def generate_response(question):
    question = request.json['question']
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Detectar el idioma de la pregunta
    source_lang = detect(question)

    # Traducir la pregunta al inglés si no está en inglés
    if source_lang != "en":
        question = translate(question, "en")

    # Cargar el tokenizador
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.add_special_tokens({"pad_token": "<pad>", 
                                  "bos_token": "<startofstring>",
                                  "eos_token": "<endofstring>"})
    tokenizer.add_tokens(["<bot>:"])

    # Cargar el modelo preentrenado
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.resize_token_embeddings(len(tokenizer))
    model.load_state_dict(torch.load("psycho.pt", map_location=device))
    model.to(device)
    model.eval()

    # Preprocesar la pregunta
    input_text = "<startofstring> " + question + " <bot>: "
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    # Generar la respuesta
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Traducir la respuesta al idioma original de la pregunta si no está en inglés
    if source_lang != "en":
        output_text = translate(output_text, source_lang, "en")

    # Obtener el texto entre "<bot>:" eliminando el resto
    start_token = "<bot>:"
    end_token = "<bot>:"
    start_index = output_text.find(start_token)
    end_index = output_text.find(end_token, start_index + len(start_token))
    if start_index != -1 and end_index != -1:
        output_text = output_text[start_index + len(start_token):end_index].strip()

    return jsonify({'response': output_text})

if __name__ == '__main__':
    app.run(port=5000)

