from bs4 import BeautifulSoup
import requests


def scrape_website(url):
    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant information from the website
    # You can customize this according to your requirements
    # For example:
    title = soup.title.text
    description = soup.find('meta', attrs={'name': 'description'})['content']

    return {'title': title, 'description': description}
