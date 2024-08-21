document.addEventListener("DOMContentLoaded", function() {
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const messages = document.getElementById("messages");

    // Add event listener for send button
    sendBtn.addEventListener("click", function() {
        processMessage();
    });

    // Add event listener for Enter key press
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            processMessage();
        }
    });

    function processMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        // Display user's message
        addMessage(userMessage, "user-message");

        // Send message to backend for processing
        fetch("/api/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const botMessage = data.response;
            addMessage(botMessage, "bot-message");
        })
        .catch(error => {
            addMessage("Oops! Something went wrong.", "bot-message");
        });

        // Clear input field
        userInput.value = "";
    }

    function addMessage(message, className) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${className}`;
        messageDiv.textContent = message;
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight; // Auto-scroll to latest message
    }
});
