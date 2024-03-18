import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests


def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.text
        description = soup.find('meta', attrs={'name': 'description'})['content']
        # Additional content
        # Extracting all links on the page
        links = [link.get('href') for link in soup.find_all('a')]
        # Extracting all paragraphs
        paragraphs = [p.text for p in soup.find_all('p')]
        # Extracting all image URLs
        images = [img.get('src') for img in soup.find_all('img')]
        return {'title': title, 'description': description, 'links': links, 'paragraphs': paragraphs, 'images': images}
    except Exception as e:
        print(e)
        return None


def get_website_details():
    url = entry.get()
    website_info = scrape_website(url)
    if website_info:
        messagebox.showinfo("Website Details",
                            f"Title: {website_info['title']}\nDescription: {website_info['description']}")
    else:
        messagebox.showerror("Error", "Failed to fetch website details. Please check the URL.")


def send_message(event=None):
    message = user_input.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + message + "\n")
    chat_log.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)


root = tk.Tk()
root.title("Website Scraper & Chatbot")

# Website Details Section
url_label = tk.Label(root, text="Enter Website URL:")
url_label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

details_button = tk.Button(root, text="Get Details", command=get_website_details)
details_button.pack()

# Chat Section
chat_log = tk.Text(root, width=50, height=20)
chat_log.config(state=tk.DISABLED)
chat_log.pack()

user_input = tk.Entry(root, width=50)
user_input.pack()
user_input.bind("<Return>", send_message)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

root.mainloop()
