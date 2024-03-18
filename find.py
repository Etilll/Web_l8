
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.cursor import Cursor
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

class DBOperations:
    db = client.myFirstDatabase.quote
        
    def find_by_name(self, name):
        return client.myFirstDatabase.quote.find_one({'author':name}, {'quote':1, '_id':0})

    def find_by_tag(self, tag):
        return self.db.find({'tags':{'$in':[tag,]}}, {'quote':1, '_id':0})

    def find_by_tags(self, tags:str):
        tt = []
        tags = tags.split(',')
        for item in tags:
            tt.append(str(item).strip())
        print(tt)
        return self.db.find({'tags':{'$in':tt}}, {'quote':1, '_id':0})

    def start(self):
        go_on = True
        while go_on:
            command = input()
            if command != "":
                if command.find(':') != -1:
                    command = command.split(':')
                    ref = {'name':self.find_by_name,'tag':self.find_by_tag,'tags':self.find_by_tags}
                    if command[0].strip() in ref.keys():
                        result = ref[command[0]](command[1].strip())
                        if type(result) == Cursor:
                            for item in result:
                                print(item['quote'].encode('utf-8'))
                        else:
                            print(result['quote'].encode('utf-8'))
                    else:
                        print('No such command exists')
                elif command.strip() == 'exit':
                    break
                else:
                    print('Incorrect command format')
                command = ""

if __name__ == '__main__':
    oper = DBOperations()
    oper.start()