from models import Quote, Author
import connect
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

client = MongoClient(
    f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
    server_api=ServerApi('1'))

def json_to_db(file_name, db):
    with open(file_name) as file:
        file_data = json.load(file)

    if isinstance(file_data, list):
        db.insert_many(file_data)  
    else:
        db.insert_one(file_data)


aut = Author(fullname = 'Dimitri', born_date = '1.1.2021', born_location = 'In the middle of nowhere', description = 'The dude.').save()
tag = Quote(tags = ['123','222','44'], author=aut, quote='There were 3 goats. How many? You have 30 seconds - Jacques Fresko').save()
tag = Quote(tags = ['123','222','44'], author=aut, quote='"I didnt say that" - Jacques Fresko').save()

if __name__ == '__main__':
    json_to_db('authors.json', client.myFirstDatabase.author)
    json_to_db('quotes.json', client.myFirstDatabase.quote)