# Setting libraries and headers
import requests
from bs4 import BeautifulSoup
from time import sleep
import re
0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}


# In[12]:


# Amazon Link
def extract_prices_and_links_amazon(soup):
    items = []
    for item in soup.select('.s-result-item'):
        price_tag = item.select_one('.a-price-whole')
        if not price_tag:
            continue
        price = float(price_tag.text.replace(',', ''))
        link = 'https://www.amazon.com' + item.select_one('.a-link-normal')['href']
        items.append((price, link))
    return items

def find_lowest_price_amazon(item):
    base_url = "https://www.amazon.com"
    search_url = f"{base_url}/s?field-keywords={item}"
    
    items = []

    while search_url:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        items.extend(extract_prices_and_links_amazon(soup))

        next_page = soup.select_one('.s-pagination-item.s-pagination-disabled + .s-pagination-item')
        search_url = base_url + next_page['href'] if next_page else None

        sleep(1)  # To prevent overwhelming the server with requests
    
    return min(items, key=lambda x: x[0]) if items else (float('inf'), None)


# In[13]:


# Ebay Link
def extract_prices_and_links_ebay(soup):
    items = []
    for item in soup.select('.s-item'):
        price_tag = item.select_one('.s-item__price')
        if not price_tag:
            continue
        price = re.search(r'[\d,]+(\.\d{2})?', price_tag.text)
        if not price:
            continue
        price = float(price.group().replace(',', ''))
        link = item.select_one('.s-item__link')['href']
        items.append((price, link))
    return items

def find_lowest_price_ebay(item):
    search_url = f'https://www.ebay.com/sch/i.html?_nkw={item}'
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    items = extract_prices_and_links_ebay(soup)
    return min(items, key=lambda x: x[0]) if items else (float('inf'), None)


# In[14]:


# Walmart Link
def extract_prices_and_links_walmart(soup):
    items = []
    for item in soup.select('.search-result-gridview-item-wrapper'):
        price_tag = item.select_one('.price-group .price-characteristic')
        if not price_tag:
            continue
        price = float(price_tag['content'])
        link = 'https://www.walmart.com' + item.select_one('.search-result-productimage')['href']
        items.append((price, link))
    return items

def find_lowest_price_walmart(item):
    search_url = f'https://www.walmart.com/search/?query={item}'
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    items = extract_prices_and_links_walmart(soup)
    return min(items, key=lambda x: x[0]) if items else (float('inf'), None)


# In[15]:


# Target Link
def extract_prices_and_links_target(soup):
    items = []
    for item in soup.select('.h-padding-a-tight .h-display-flex'):
        price_tag = item.select_one('.h-text-bs .h-text-grayDark')
        if not price_tag:
            continue
        price = float(re.sub(r'[^\d.]+', '', price_tag.text))
        link = 'https://www.target.com' + item.select_one('.h-display-flex a')['href']
        items.append((price, link))
    return items

def find_lowest_price_target(item):
    search_url = f'https://www.target.com/s?searchTerm={item}'
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    items = extract_prices_and_links_target(soup)
    return min(items, key=lambda x: x[0]) if items else (float('inf'), None)



# Lowest Price
def find_lowest_price(item):
    lowest_amazon = find_lowest_price_amazon(item)
    lowest_ebay = find_lowest_price_ebay(item)
    lowest_walmart = find_lowest_price_walmart(item)
    lowest_target = find_lowest_price_target(item)

    lowest = min(lowest_amazon, lowest_ebay, lowest_walmart, lowest_target, key=lambda x: x[0])

    store = ''
    if lowest == lowest_amazon:
        store = 'Amazon'
    elif lowest == lowest_ebay:
        store = 'eBay'
    elif lowest == lowest_walmart:
        store = 'Walmart'
    elif lowest == lowest_target:
        store = 'Target'

    return lowest[0], lowest[1], store


