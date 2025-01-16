document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const messageForm = document.getElementById('messageForm');

    // Handle user registration
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const responseMessage = document.getElementById('responseMessage');

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `username=${encodeURIComponent(username)}`
                });
                const data = await response.json();

                if (response.ok) {
                    responseMessage.textContent = `Your link: ${data.link}`;
                } else {
                    responseMessage.textContent = data.error;
                }
            } catch (error) {
                responseMessage.textContent = 'An error occurred. Please try again.';
            }
        });
    }

    // Handle anonymous message submission
    if (messageForm) {
        messageForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const linkId = messageForm.getAttribute('data-link-id');
            const message = document.getElementById('message').value;
            const responseMessage = document.getElementById('responseMessage');

            try {
                const response = await fetch(`/send/${linkId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `message=${encodeURIComponent(message)}`
                });
                const data = await response.json();

                if (response.ok) {
                    responseMessage.textContent = data.message;
                    messageForm.reset();
                } else {
                    responseMessage.textContent = 'Failed to send the message.';
                }
            } catch (error) {
                responseMessage.textContent = 'An error occurred. Please try again.';
            }
        });
    }
});
