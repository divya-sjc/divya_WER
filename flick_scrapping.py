import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# Base URL of the website
base_url = 'https://www.flick.com.au/'

# Set to store visited URLs to avoid duplicates
visited_urls = set()

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scrape data from the page (customize this part according to what you want to scrape)
    title = soup.title.string if soup.title else "No Title"
    print(f"Scraping {url}: Title = {title}")
    
    # Extract all text or specific information here
    page_data = {"url": url, "title": title}
    
    return page_data

# Function to get all links from a page
def get_all_links(soup, base_url):
    links = set()
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        full_url = urljoin(base_url, href)
        if full_url.startswith(base_url):
            links.add(full_url)
    return links

# Recursive function to crawl the website
def crawl_website(url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    # Scrape the page
    page_data = scrape_page(url)
    scraped_data.append(page_data)
    
    # Get the page content and parse the links
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = get_all_links(soup, base_url)
    
    # Recursively crawl other pages
    for link in links:
        if link not in visited_urls:
            crawl_website(link)

# List to store scraped data
scraped_data = []

# Start crawling from the base URL
crawl_website(base_url)

# Save scraped data to a CSV file
with open('flick_website_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['url', 'title']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(scraped_data)

print("Crawling complete! Data saved to 'flick_website_data.csv'")
