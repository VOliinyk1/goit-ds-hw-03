import json 
import requests
import os
import re

from bs4 import BeautifulSoup
from pymongo import MongoClient, errors

def append_to_json(file_path, new_data):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_data)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def get_quotes():
    for current_page in range(1, 11):
        quotes = {
    "tags": [],
    "author": "",
    "quote": ""
  }
        url = f'http://quotes.toscrape.com/page/{current_page}'
        page = requests.get(url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            
            

            all_quotes = soup.find_all("div", class_='quote')

            for quote in all_quotes:
                tags = quote.find_all("a", class_="tag")
                tags = [tag.get_text() for tag in tags]
                author = quote.find("small", class_="author").get_text()
                quote = quote.find("span", class_="text").get_text().strip()
                decoded_quote = quote.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
                quote_clean = re.sub(r'\s+', ' ', decoded_quote)
                quote_clean = re.sub(r'[^\w\s,.!?-]', '', quote_clean)
                quotes.update({"tags": tags,
                            "author": author,
                            "quote": quote_clean})
        
                append_to_json('quotes.json', quotes)

def get_unique_authors():
    unique_authors_href = []
    for current_page in range(1, 11):     
        url = f'http://quotes.toscrape.com/page/{current_page}'
        page = requests.get(url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            authors_on_page = soup.find_all("small", class_="author")
            authors_href = [author.find_next_sibling("a").get("href") for author in authors_on_page]
            # authors_href = [author.get_text() for author in authors_href]
            for author in authors_href:
                unique_authors_href.append(author) if author not in unique_authors_href else None
    return unique_authors_href
            

def get_authors(authors: list):
    for author in authors:
        authors_data = {
            "fullname": "",
            "born_date": "",
            "born_location": "",
            "description": ""
        }
        url = f'https://quotes.toscrape.com{author}/'
        page = requests.get(url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            fullname = soup.find("h3", class_="author-title").get_text()
            born_date = soup.find("span", class_="author-born-date").get_text()
            born_location = soup.find("span", class_="author-born-location").get_text()
            description = soup.find("div", class_="author-description").get_text()
            decoded_description = description.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
            description_clean = re.sub(r'\s+', ' ', decoded_description)
            description_clean = re.sub(r'[^\w\s,.!?-]', '', description_clean)
            if not fullname:
                print(author)
            authors_data.update({"fullname": fullname,
                                "born_date": born_date,
                                "born_location": born_location,
                                "description": description_clean})
            append_to_json('authors.json', authors_data)
    

            

unique_authors = get_unique_authors()
get_authors(unique_authors)
get_quotes()