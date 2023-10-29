import requests 
import pandas as pd 
from bs4 import BeautifulSoup 
try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

def get_google_results(topic, amount):
    query = topic
    website_urls = []
    for j in search(query, tld="co.in", num=amount, stop=amount, pause=2):
        website_urls.append(j)
    return website_urls

# Test Main Function
'''
test_results = get_google_results("College tuition", 5)
print(test_results)
'''

