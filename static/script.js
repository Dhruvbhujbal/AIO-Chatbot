document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;

    if (userInput.trim() === '') {
        return; // Don't send an empty message
    }

    // Display the user's message in the chat window
    const chatWindow = document.getElementById('chat-window');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = userInput; // Ensure user input doesn't contain HTML
    chatWindow.appendChild(userMessage);

    // Add the user's message to the search history
    const searchHistoryList = document.getElementById('history-list'); // Accessing the <ul> element
    const historyItem = document.createElement('li'); // Create a new list item
    historyItem.textContent = userInput; // Set the text content to the user input
    searchHistoryList.appendChild(historyItem); // Append the item to the list

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Send the message to the Flask backend
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: userInput
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Format the bot's response to display properly
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');
        
        // Format response into HTML (add line breaks, headings, etc.)
        const formattedResponse = formatBotResponse(data.response);
        
        // Start typing animation with the formatted response
        chatWindow.appendChild(botMessage); // Append the bot message container first
        simulateTyping(botMessage, formattedResponse, 2); // Adjust delay for typing speed

        // Scroll the chat window to the bottom
        chatWindow.scrollTop = chatWindow.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to simulate typing effect
function simulateTyping(element, text, delay) {
    let index = 0;
    let htmlContent = "";  // We will accumulate the content here

    function addChar() {
        if (index < text.length) {
            htmlContent += text.charAt(index);  // Add character to accumulated HTML
            element.innerHTML = htmlContent;  // Update the HTML content in one go
            index++;
            setTimeout(addChar, delay);
        }
    }

    addChar();
}

// Function to format bot response (with proper HTML formatting)
function formatBotResponse(response) {
    // Replace new lines with <br> for line breaks
    response = response.replace(/\n/g, "<br>");
    
    // Bold text with **...**
    response = response.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");

    // H3 headers with ### header text
    response = response.replace(/### (.*?)\n/g, "<h3>$1</h3>");

    // Convert numbered list to unordered list (for simplicity, we use <ul> tags here)
    response = response.replace(/\d+\.\s(.*?)(?=\n|$)/g, "<ul><li>$1</li></ul>");

    return response;
}

// Optional: Make the Enter key send the message as well
document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        document.getElementById('send-btn').click();
    }
});
