from pymongo import MongoClient
from datetime import datetime

class Open_DB_Connection():
    
    def __init__(self, db_url, db_name, db_collection_name):
        self.db_url = db_url
        self.db_name = db_name
        self.db_collection_name = db_collection_name

    def connect_db(self, db_url: str, db_name: str, db_collection_name:str):
        print(f'Opening a DB Connection to - {db_name} / {db_collection_name}')
        cluster = MongoClient(db_url)
        database = cluster[db_name]
        collection = database[db_collection_name]
        return {
            'cluster': cluster,
            'database': database,
            'collection': collection
        }

    def disconnect_db(self, cluster) -> None:
        try:
            cluster.close()
            print('DB connection Terminated!!')
        except Exception as error:
            print('Problem in Disconnecting the DB connection')
            print(f'{error = }')

    def __enter__(self, *args):
        resp = self.connect_db(
            db_url = self.db_url,
            db_name = self.db_name,
            db_collection_name = self.db_collection_name
            )
        self.db_cluster = resp['cluster']
        self.db_database = resp['database']
        self.db_collection = resp['collection']
        return resp

    def __exit__(self, *args):
        self.disconnect_db(cluster = self.db_cluster)

# Outside-Class Functions

def format_document(id, url, name, user, date, anon, pd):
    return {
        '_id': int(id),
        'url': str(url),
        'name': str(name),
        'user': int(user),
        'date': date,
        'anon': str(anon),
        'pd': str(pd)
    }

def insert_document(collection, id, url, name, user, anon, pd):
    final_doc = format_document(
        id = id,
        url = url,
        name = name,
        user = user,
        date = round(datetime.timestamp(datetime.today())),
        anon = anon,
        pd = pd
        )
    collection.insert_one(document = final_doc)

def find_document(id, collection):
    cursor = collection.find({'_id': id})
    try:
        cursor[0]
        return cursor
    except IndexError:
        return None    

def is_duplicate(id, collection) -> bool:
    resp = find_document(
        id = id,
        collection = collection
        )
    if resp:
        print(f'ID already exist in the DB')
        print(f'{resp[0] = }')
        return True
    else:
        return False