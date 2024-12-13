import requests
from bs4 import BeautifulSoup

# URL where the lyrics are located
url = 'https://genius.com/Jeff-buckley-grace-lyrics'
# Send a request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Print the HTML to debug
print(soup.prettify())

# Assuming you find the correct class after inspection, update this line
lyrics_div = soup.find('div', class_='lyrics')

# Check if the lyrics_div is found and then extract text
if lyrics_div:
    lyrics_text = lyrics_div.get_text().strip()
    words = lyrics_text.split()
    print(words)
else:
    print("Lyrics section not found on the page.")
