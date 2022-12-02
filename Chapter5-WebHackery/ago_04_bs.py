from bs4 import BeautifulSoup as bs
import requests

url = 'http://localhost'
resp = requests.get(url=url)

tree = bs(resp.text, 'html.parser')
for link in tree.find_all('a'):
    print(f"{link.get('href')} -> {link.text}")
