import requests
from bs4 import BeautifulSoup
import csv

# URL of the travel agents directory
base_url = 'https://www.yoururl.co.za'
url_template = f'{base_url}/category/accommodation/{{}}'

# Number of pages to scrape
num_pages = 50

# Send a GET request to the URL and get the HTML content
business_links = set()
for page in range(1, num_pages+1):
    url = url_template.format(page)
    response = requests.get(url)
    content = response.content
    print('moving onto page-', page)

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Find the element with the id attribute of 'listings'
    listings = soup.find('div', {'id': 'listings'})
    if listings:
        # Find all the business links on the page that contain the word "company"
        for link in listings.find_all('a'):
            href = link.get('href')
            if href and 'company' in href and 'review' not in href:
                business_links.add(f'{base_url}{href}')

# Scrape the data from each business page
data = []
for link in business_links:
    response = requests.get(link)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    # Scrape the business name
    name = soup.find('h1').text.strip()

    # Scrape the location, telephone number, mobile number, and contact person
    location = None
    tel_number = None
    mobile_number = None
    contact_person = None
    website_link = None
    contact_info = soup.find('div', {'class': 'cmp_details_in'})
    if contact_info:
        contact_info = contact_info.find_all('div', class_='info')
        for info in contact_info:
            if 'Address' in info.text:
                location = info.text.replace('Address', '').strip()
            elif 'Phone' in info.text:
                tel_number = info.text.replace('Number', '').strip()
            elif 'Mobile' in info.text:
                mobile_number = info.text.replace('phone', '').strip()
            elif 'Contact Person' in info.text:
                contact_person = info.text.replace('Contact Person', '').strip()
        # Get the website link if it's available
        website_link = soup.find('a', {'class': 'info'})
        if 'Weblinks' in info.text:
            website_link = info.text.replace('Website', '').strip()
    # Add the data to the list
    data.append([name, location, tel_number, mobile_number, contact_person, website_link])

# Save the data to a CSV file
with open('travel_agents.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Business Name', 'Location', 'Tel Number', 'Mobile Number', 'Contact Person', 'Website Link'])
    writer.writerows(data)
