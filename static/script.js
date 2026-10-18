
const form = document.getElementById("form");
const input = document.getElementById("message");
const chat = document.getElementById("chat");
const send = document.getElementById("send");

function addMessage(text, role) {
  const bubble = document.createElement("div");
  bubble.className = "message " + role;
  bubble.textContent = text;
  chat.appendChild(bubble);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message || send.disabled) return;

  addMessage(message, "user");
  input.value = "";
  send.disabled = true;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.response || "Permintaan gagal.");
    }

    addMessage(data.response, "bot");
  } catch (error) {
    addMessage(
      "Gagal menghubungi chatbot: " + error.message,
      "bot"
    );
  } finally {
    send.disabled = false;
    input.focus();
  }
});
