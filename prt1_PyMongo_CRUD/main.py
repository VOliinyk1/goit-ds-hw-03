from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

try:
    client = MongoClient(
        "mongodb+srv://vov2598:t5IYyaEiX00NQY4B@cluster0.krvck.mongodb.net/",
        server_api=ServerApi('1')
    )

    db = client.book
except errors.ConnectionFailure as conn_error:
    print(f'Не вдалося підключитись до бази даних: {conn_error}')
except errors.ConfigurationError as config_error:
    print(f'Помилка конфігурації підключення: {config_error}')
except Exception as e:
    print(f'Сталася несподівана помилка: {e}')

# Читання
def show_all_cats():
    try:
        # виведення всіх записів із колекції.
        result = db.cats.find({})

        for el in result:
            print(el)
    except errors.PyMongoError as query_error:
        print(f'Помилка під час виконання запиту: {query_error}')

def show_one_cat():
    try:
        # ввести ім'я кота та виводить інформацію про цього кота.
        input_cat = input("Введіть ім'я кота: ")
        result = db.cats.find_one({"name": input_cat})
        print(result) if result else print('Такого кота немає')
    except errors.PyMongoError as query_error:
        print(f'Помилка під час виконання запиту: {query_error}')

# Оновлення
def update_cats_age():
    try:
        # оновити вік кота за ім'ям.
        input_cat = input("Введіть ім'я кота для зміни віку: ")

        result = db.cats.find_one({"name": input_cat})
        if result:
            new_age_input = input('Введіть вік кота')
            db.cats.update_one({"name": input_cat}, {"$set": {"age": new_age_input}})
            result = db.cats.find_one({"name": input_cat})
            print(result)
        else:
            print('Такого кота немає')
    except errors.PyMongoError as query_error:
        print(f'Помилка під час виконання запиту: {query_error}')

def add_cats_feature():
    try:
        # додати нову характеристику до списку features кота за ім'ям.
        input_cat = input("Введіть ім'я кота для додавання особливостей: ")
        result = db.cats.find_one({"name": input_cat})
        if result:
            new_feature_input = input('Введіть нову особливість')
            db.cats.update_one({"name": input_cat}, {"$push": {"features": new_feature_input}})
            result = db.cats.find_one({"name": input_cat})
            print(result)
        else:
            print('Такого кота немає')
    except errors.PyMongoError as query_error:
        print(f'Помилка під час виконання запиту: {query_error}')

# Видалення
def delete_one_cat():
    try:
        # видалення запису з колекції за ім'ям тварини.
        input_cat = input("Введіть ім'я кота: ")
        result = db.cats.find_one({"name": input_cat})
        if result:
            db.cats.delete_one({"name": input_cat})
            print(f'Кота {result} видалено.')
        else:
            print('Такого кота немає')
    except errors.PyMongoError as query_error:
        print(f'Помилка під час виконання запиту: {query_error}')

def delete_all_cats():
    try:
        db.cats.delete_many({})
    except errors.PyMongoError as query_error:
        print(f'Помилка під час виконання запиту: {query_error}')

if __name__ == "__main__":
    show_all_cats()
    # show_one_cat()
    # update_cats_age()
    # add_cats_feature()
    # delete_one_cat()
