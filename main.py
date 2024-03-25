import tkinter as tk
from tkinter import messagebox
from new import myAiBot 
from bs4 import BeautifulSoup
import requests

class ChatGUI:
    url = None
    def __init__(self, ai_bot):
        self.ai_bot = ai_bot
        self.chat_history = []

        # Create the main Tkinter window
        self.root = tk.Tk()
        self.root.title("Chatbot")
        
        # Enter Website URL Section
        url_label = tk.Label(self.root, text="Enter Website URL:")
        url_label.pack()

        entry = tk.Entry(self.root, width=50)
        entry.pack()

        def details(url):
            """Load documents from a website using BeautifulSoup."""
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract text content from paragraphs
                paragraphs = [p.text.strip() for p in soup.find_all('p')]
                # Extract text content from headings
                headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
                # Combine paragraphs and headings to form documents
                documents = paragraphs + headings
                return documents
            except Exception as e:
                print(f"Error loading documents from {url}: {e}")
                return []
        
        def get_website_details():
            global url 
            url = entry.get()
            website_info = details(url)
            print(website_info)
            if website_info:
                messagebox.showinfo("Website Details",
                                    f"Details : {website_info}")
            else:
                messagebox.showerror("Error", "Failed to fetch website details. Please check the URL.")

        details_button = tk.Button(self.root, text="Get Details", command=get_website_details)
        details_button.pack()

        # Chat history display
        self.chat_box = tk.Text(self.root, height=20, width=50)
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.pack(padx=10, pady=10)

        # User input field
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        # Bind <Return> key to send_message function
        self.root.bind('<Return>', self.send_message)

    def send_message(self, event=None):
        # Get user input
        user_input = self.entry.get()
        
        # Display user input in the chat history
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, "You: " + user_input + "\n")
        self.chat_box.config(state=tk.DISABLED)
        
        # Clear the input field
        self.entry.delete(0, tk.END)
        
        # Get AI response
        ai_response = self.ai_bot.start_conversation(user_input ,url)
        
        # Display AI response in the chat history
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, "Bot: " + ai_response + "\n")
        self.chat_box.config(state=tk.DISABLED)

    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

# Create an instance of the ConversationSystem class
ai = myAiBot("AIzaSyC9u1gjP_ZyGDuyYkv5gnkkOyaDX50aR7U")

# Create the chat GUI
chat_gui = ChatGUI(ai)

# Run the chat GUI
chat_gui.run()
