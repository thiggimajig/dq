# // script on gem website, slow to not be detected
# // find all instances of country
# // switch all html instances of country to country/area
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Base URL of the website
base_url = 'https://bachelornation.com/'

# String to search for
search_string = 'Jen' # Country, countries, Countries

# Set to store visited URLs to avoid loops
visited_urls = set()

# List to store found instances
found_instances = []

# Function to extract all links from a page
def extract_links(url, soup):
    links = []
    for a_tag in soup.find_all('a', href=True):
        # Construct full URL and add to the list
        full_url = urljoin(url, a_tag['href'])
        # Only add URLs that belong to the same base domain and haven't been visited
        if base_url in full_url and full_url not in visited_urls:
            links.append(full_url)
    return links

# Function to scrape a page and search for the string
def scrape_page(url):
    try:
        # Send GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text()

        # Check if the search string is in the page text
        if search_string in page_text:
            found_instances.append((url, page_text.count(search_string)))

        # Mark the URL as visited
        visited_urls.add(url)

        # Extract and return all links on this page
        return extract_links(url, soup)

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return []

# Start scraping from the main page
to_visit = [base_url]

# Loop through pages to visit
while to_visit:
    current_url = to_visit.pop(0)
    if current_url not in visited_urls:
        new_links = scrape_page(current_url)
        to_visit.extend(new_links)

# Output the results
for page_url, count in found_instances:
    print(f"Found '{search_string}' {count} times on: {page_url}")