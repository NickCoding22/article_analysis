import requests 
import pandas as pd 
from bs4 import BeautifulSoup 

# Gets the website's text from url
def get_html(url): 
    headers = {"User-Agent":"Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    return r.text 

# Given a website url it returns the main text content
def parse_website(website_url):
    htmldata = get_html(website_url)
    soup = BeautifulSoup(htmldata, 'html.parser') 
    data = '' 
    full_article = ''
    for data in soup.find_all("p"): 
        if len(data.get_text()) > 10 and "\n" not in data.get_text():
            full_article += data.get_text()
    return(full_article)

# Testing Main Function
'''
#parsing_test = parse_website("https://www.defense.gov/News/News-Stories/Article/Article/3570190/dod-announces-up-to-150m-in-aid-for-ukraine/")
parsing_test = parse_website("https://www.sfchronicle.com/bayarea/article/sf-city-college-revive-18417567.php")
print(parsing_test)
'''