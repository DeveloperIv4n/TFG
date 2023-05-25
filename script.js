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

    // Envía el mensaje a tu API
    const url = `https://6384-35-229-32-77.ngrok-free.app/generate-response/${encodeURIComponent(message)}`; //  la dirección de tu API
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question: message })
    });

    const data = await response.json();

    // Agrega la respuesta al chat
    const botMessage = document.createElement("div");
    botMessage.classList.add("message", "bot-message");
    botMessage.innerText = data.response;
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
