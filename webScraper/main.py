from bs4 import BeautifulSoup
import requests
import re

# Basic user input for search term which used in target url
search_term = input('What product do you searching for?  ')

#defining of link for scraping
url = f"https://www.newegg.com/p/pl?d={search_term}&n=8000"
page = requests.get(url).text

# Bs4 instance with target page(url) and output type
doc = BeautifulSoup(page, 'html.parser')

# procesing information for paginator
page_text = doc.find(class_='list-tool-pagination-text').strong.text.split('/')[1]
pages = int(page_text)
found_items={}

# #search GPU for each web page separately
for page in range(1, pages+1):
    url = f"https://www.newegg.com/p/pl?d={search_term}&n=8000&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')
    div = doc.find(class_='item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell')
    items = div.find_all(text=re.compile(search_term))
    
    for item in items:
        parent=item.parent
        if parent.name != 'a':
            continue

        link = parent['href']
        next_parent = item.find_parent(class_='item-container')
        try:
            price = next_parent.find(class_='price-current').find("strong").string
            found_items[item] = {"price": int(price.replace(",","")), "link": link}
        except:
            pass

sorted_items=sorted(found_items.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("---------------------------------------------------------------------------------")
        
