const chatContainer = document.getElementById("chat-container");

async function sendMessage(message) {
  // Agrega el mensaje del usuario al chat
  const userMessage = document.createElement("div");
  userMessage.classList.add("message", "user-message");
  userMessage.innerText = message;
  // Crear el div contenedor del mensaje del usuario
  const userDiv = document.createElement("div");
  userDiv.setAttribute("id", "userM");

  // Añadir el mensaje del usuario al div contenedor
  userDiv.appendChild(userMessage);

  // Añadir el div contenedor al contenedor del chat
  chatContainer.appendChild(userDiv);


  // Envía el mensaje al modelo de Hugging Face
  const response = await fetch(
    "https://api-inference.huggingface.co/models/facebook/blenderbot-3B",
    {
      headers: { Authorization: "Bearer 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" },
      method: "POST",
      body: JSON.stringify({
        inputs: {
          past_user_inputs: ["Which movie is the best ?"],
          generated_responses: ["It's Die Hard for sure."],
          text: message,
        },
      }),
    }
  );
  const result = await response.json();

  // Agrega la respuesta del modelo al chat
  const botMessage = document.createElement("div");
  botMessage.classList.add("message", "bot-message");
  botMessage.innerText = result.generated_text;
  chatContainer.appendChild(botMessage);
}

// Escucha el evento submit del formulario de envío del mensaje
const messageForm = document.getElementById("message-form");
messageForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const messageInput = document.getElementById("message-input");
  const message = messageInput.value;
  if (message) {
    sendMessage(message);
    messageInput.value = "";
  }
});
