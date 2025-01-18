import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError

client = MongoClient(
    "mongodb+srv://vov2598:t5IYyaEiX00NQY4B@cluster0.krvck.mongodb.net/",
    server_api=ServerApi('1'))
db = client.quote_scrap

def export_authors():
    try:
        with open('authors.json', 'r') as authors_file:
            quotes_dict = json.load(authors_file)
            db.authors.insert_many(quotes_dict)
        print("Authors exported successfully!")
    except FileNotFoundError:
        print("Error: 'authors.json' file not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from 'authors.json'.")
    except PyMongoError as e:
        print(f"MongoDB error while exporting authors: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while exporting authors: {e}")

def export_quotes():
    try:
        with open('quotes.json', 'r') as quotes_file:
            quotes_dict = json.load(quotes_file)
            db.quotes.insert_many(quotes_dict)
        print("Quotes exported successfully!")
    except FileNotFoundError:
        print("Error: 'quotes.json' file not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from 'quotes.json'.")
    except PyMongoError as e:
        print(f"MongoDB error while exporting quotes: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while exporting quotes: {e}")

# Виклики функцій
export_authors()
export_quotes()
