// bot.js

// Set up the chat UI
const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
const chatSubmit = document.getElementById('chat-submit');

// Function to add a message to the chat
function addMessage(message, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender);
  messageDiv.textContent = message;
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to handle user input
async function handleUserInput() {
  const userInput = chatInput.value.trim();
  if (userInput) {
    addMessage(userInput, 'user');
    chatInput.value = '';

    try {
      const response = await fetch('/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
      });

      if (response.ok) {
        const botResponse = await response.json();
        addMessage(botResponse.response, 'bot');
      } else {
        const errorMessage = await response.text();
        addMessage(`There was an error processing your message: ${errorMessage}`, 'bot');
      }
    } catch (error) {
      console.error('Error fetching bot response:', error);
      addMessage('Sorry, there was a network error. Please try again later.', 'bot');
    }
  }
}

// Add event listeners
chatSubmit.addEventListener('click', handleUserInput);
chatInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    handleUserInput();
  }
});