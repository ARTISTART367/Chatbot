from bs4 import BeautifulSoup
import requests


def scrape_website(url):
    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant information from the website
    # You can customize this according to your requirements

    # Title and description
    title = soup.title.text
    description = soup.find('meta', attrs={'name': 'description'})['content']

    # Additional content
    # Extracting all links on the page
    links = [link.get('href') for link in soup.find_all('a')]

    # Extracting all paragraphs
    paragraphs = [p.text for p in soup.find_all('p')]

    # Extracting all image URLs
    images = [img.get('src') for img in soup.find_all('img')]

    return {
        'title': title,
        'description': description,
        'links': links,
        'paragraphs': paragraphs,
        'images': images
    }
