import tkinter as tk
from tkinter import scrolledtext
import threading
import requests
import json

# DeepSeek API configuration
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Replace with the actual API endpoint
DEEPSEEK_API_KEY = "your_api_key_here"   

# Headers for the API request
HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}

def get_deepseek_response(user_input):
    """
    Send the user's input to the DeepSeek API and get the response.
    """
    try:
        # Prepare the request payload
        payload = {
            "model": "deepseek-chat",  # Replace with the correct model name
            "messages": [{"role": "user", "content": user_input}],
            "max_tokens": 150,  # Adjust as needed
        }

        # Make the API request
        response = requests.post(DEEPSEEK_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the response
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to get response from DeepSeek. {str(e)}"

class DeepSeekChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepSeek Chat")
        self.root.geometry("600x500")

        # Chat history display
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input field
        self.user_input = tk.Entry(root, width=50,text="Welcome to DeepSeek Chat!\n\n",font=("Arial", 12), bg="#f0f0f0")
        self.user_input.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message,bg="blue",fg="white",font=("Arial", 12))
        self.send_button.pack(padx=10, pady=10, side=tk.RIGHT)

        # Bind Enter key to send message
        self.root.bind('<Return>', lambda event: self.send_message())

    def send_message(self):
        """Handle sending a message."""
        user_message = self.user_input.get().strip()
        if not user_message:
            return

        # Display user's message in the chat history
        self.update_chat_history(f"You: {user_message}\n")

        # Clear the input field
        self.user_input.delete(0, tk.END)

        # Get DeepSeek's response in a separate thread
        threading.Thread(target=self.get_and_display_response, args=(user_message,)).start()

    def get_and_display_response(self, user_message):
        """Get DeepSeek's response and display it in the chat history."""
        response = get_deepseek_response(user_message)
        self.update_chat_history(f"DeepSeek: {response}\n\n")

    def update_chat_history(self, message):
        """Update the chat history with a new message."""
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message)
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    app = DeepSeekChatApp(root)

    # Start the GUI event loop
    root.mainloop()