import os
import csv
from pymongo import MongoClient

os.chdir(os.path.abspath(os.path.dirname(__file__)))

HOST = 'cluster0.qmfz4.mongodb.net'
USER = 'user'
PASSWORD = 'user1234'
DATABASE_NAME = 'algae'
COLLECTION_NAME = 'algae'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

collection = database[COLLECTION_NAME]

with open('merge.csv', newline='') as f:
    
    reader = csv.DictReader(f)
    
    results = [i for i in reader]

data = [dict([col, float(val)] for col, val in result.items()) for result in results]

collection.insert_many(data)