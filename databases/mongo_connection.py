from pymongo import MongoClient
from config.config import MONGODB_URI

# Connexion à la BD mongoDB
def connect_mongodb():
    client = MongoClient(MONGODB_URI)
    db = client["entertainment"]
    collection = db["films"]
    return collection

